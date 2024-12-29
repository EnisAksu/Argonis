# Get the current script's directory and set up the log file path
$CurrentDir = $PSScriptRoot
$EventLogPath = Join-Path -Path $CurrentDir -ChildPath "Microsoft-Windows-PowerShell%4Operational.evtx"

# Suspicious patterns to monitor
$SuspiciousTerms = @{
    Commands = @("invoke-expression", "iex", "invoke-webrequest", "invoke-restmethod", "downloadstring")
    Techniques = @("bypass", "hidden", "encoded", "compress")
    ScriptCreation = @(
        'New-ScriptBlock',
        'Invoke-ScriptBlock',
        'Enter-PSSession',
        'Invoke-Command -ComputerName'
    )
}

# Initialize output preparation
$TimeStamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ResultsFile = Join-Path -Path $CurrentDir -ChildPath "EventAnalysis_${TimeStamp}.txt"

# Display banner
$Banner = @"
 __  __                                        _     
|  \/  | ___ _ __ __ _  ___ _ __ __ _  ___  _ __ (_)___
| |\/| |/ _ \ '__/ _' |/ _ \ '__/ _' |/ _ \| '_ \| / __|
| |  | |  __/ | | (_| |  __/ | | (_| | (_) | | | | \__ \
|_|  |_|\___|_|  \__, |\___|_|  \__, |\___/|_| |_|_|___/
                 |___/           |___/
"@

Write-Host $Banner -ForegroundColor Cyan
Write-Host "PowerShell Event Log Analysis Tool" -ForegroundColor White
Write-Host "Starting analysis at: $(Get-Date)" -ForegroundColor White
Write-Host "----------------------------------------" -ForegroundColor White

function Write-AnalysisLog {
    param (
        [string]$Message,
        [string]$Type = "Info",
        [switch]$Silent
    )
    
    $ColorMap = @{
        "Info" = "White"
        "Success" = "Green"
        "Warning" = "Yellow"
        "Error" = "Red"
    }
    
    # Only write to console if not silent and it's a specific type of message
    if (-not $Silent -and $Type -in @("Error", "Warning")) {
        Write-Host $Message -ForegroundColor $ColorMap[$Type]
    }
    Add-Content -Path $ResultsFile -Value $Message
}

function Get-UniqueScriptBlockIDs {
    param (
        [System.Diagnostics.Eventing.Reader.EventLogRecord[]]$Events
    )
    
    $ScriptBlockInfo = @()
    foreach ($Event in $Events) {
        if ($Event.Message -match 'ScriptBlock ID: ([a-fA-F0-9-]+)') {
            $ScriptBlockInfo += [PSCustomObject]@{
                ID = $matches[1]
                TimeCreated = $Event.TimeCreated.ToUniversalTime()
            }
        }
    }
    
    # Get unique IDs with their most recent timestamp
    $UniqueBlocks = $ScriptBlockInfo | Group-Object ID | ForEach-Object {
        $LatestTime = ($_.Group | Sort-Object TimeCreated -Descending)[0].TimeCreated
        [PSCustomObject]@{
            ID = $_.Name
            TimeCreated = $LatestTime
        }
    }
    
    # Sort by timestamp descending (newest first)
    return $UniqueBlocks | Sort-Object TimeCreated -Descending
}

function Write-ReducedCodeContent {
    param (
        [string]$Content,
        [string]$SearchTerm
    )
    
    $Lines = $Content -split "`n"
    $MatchingLines = @()
    $LineNumber = 0
    
    foreach ($Line in $Lines) {
        $LineNumber++
        if ($Line -match [regex]::Escape($SearchTerm)) {
            # Get context (2 lines before and after)
            $StartLine = [Math]::Max(0, $LineNumber - 3)
            $EndLine = [Math]::Min($Lines.Count - 1, $LineNumber + 2)
            
            for ($i = $StartLine; $i -le $EndLine; $i++) {
                $MatchingLines += $Lines[$i]
            }
            $MatchingLines += "---"  # Separator between contexts
        }
    }
    
    # Take first 5 sections
    $Output = $MatchingLines | Select-Object -First 15 | ForEach-Object { "$_`n" }
    
    if ($MatchingLines.Count -gt 15) {
        $Output += "`n[Content redacted - showing first 5 matches]`n"
    }
    
    return -join $Output
}

function Search-SuspiciousEvents {
    param (
        [string]$SearchIdentifier = ""
    )
    
    try {
        $StartTime = Get-Date
        Write-Host "`nScanning the EVTX file... " -NoNewline
        
        # Create a synchronized hashtable to share data with the background job
        $SharedData = [hashtable]::Synchronized(@{
            StartTime = $StartTime
            Continue = $true
        })
        
        # Start background job for timer
        $Runspace = [runspacefactory]::CreateRunspace()
        $Runspace.Open()
        $Runspace.SessionStateProxy.SetVariable('SharedData', $SharedData)
        
        $PowerShell = [powershell]::Create().AddScript({
            while ($SharedData.Continue) {
                $Elapsed = (Get-Date) - $SharedData.StartTime
                Write-Host "`rScanning the EVTX file... $($Elapsed.TotalSeconds.ToString('0.0')) seconds" -NoNewline
                Start-Sleep -Milliseconds 100
            }
        })
        
        $PowerShell.Runspace = $RunSpace
        $Handle = $PowerShell.BeginInvoke()
        if (-not (Test-Path $EventLogPath)) {
            throw "PowerShell operational log file not found at: $EventLogPath"
        }

        $EventFilter = @{
            Path = $EventLogPath
            ProviderName = "Microsoft-Windows-PowerShell"
            Id = 4104
        }

        $LogEvents = Get-WinEvent -FilterHashtable $EventFilter -ErrorAction Stop
        
        # Stop the timer
        $SharedData.Continue = $false
        $PowerShell.EndInvoke($Handle)
        $PowerShell.Dispose()
        $Runspace.Dispose()
        
        $ScanDuration = ((Get-Date) - $StartTime).TotalSeconds
        Write-Host "`rScanning the EVTX file... Done ($($ScanDuration.ToString('0.0')) seconds)" -ForegroundColor Green
        
        Write-Host "Analyzing events... 0%" -NoNewline
        $Total = $LogEvents.Count
        $Current = 0
        
        # Get and write summary of ScriptBlock IDs
        $UniqueIDs = Get-UniqueScriptBlockIDs -Events $LogEvents
        Write-AnalysisLog "`nScriptBlock ID Summary" -Silent
        Write-AnalysisLog "--------------------" -Silent
        Write-AnalysisLog "Total ScriptBlock IDs found: $($UniqueIDs.Count)" -Silent
        Write-AnalysisLog "`nList of ScriptBlock IDs (sorted by creation time - newest first):" -Silent
        Write-AnalysisLog "TimeCreated (UTC)           | ScriptBlock ID" -Silent
        Write-AnalysisLog "--------------------------- | --------------" -Silent
        $UniqueIDs | ForEach-Object { 
            $TimeStr = $_.TimeCreated.ToString("yyyy-MM-dd HH:mm:ss")
            Write-AnalysisLog "$TimeStr UTC | $($_.ID)" -Silent 
        }
        Write-AnalysisLog "`n" -Silent
        
        foreach ($Event in $LogEvents) {
            $Current++
            $ProgressPercentage = [math]::Round(($Current / $Total) * 100)
            if ($ProgressPercentage % 2 -eq 0) {  # Update every 2%
                Write-Host "`rAnalyzing events... ${ProgressPercentage}%" -NoNewline
            }
            $EventContent = $Event.Message
            $ScriptID = if ($EventContent -match 'ScriptBlock ID: ([a-fA-F0-9-]+)') {
                $matches[1]
            } else {
                "ID_NOT_FOUND"
            }

            # Skip if identifier is provided but not found in event
            if ($SearchIdentifier -and $EventContent -notlike "*$SearchIdentifier*") {
                continue
            }

            $DetectedPatterns = @()
            
            # Check for suspicious patterns
            foreach ($Category in $SuspiciousTerms.Keys) {
                $Matches = $SuspiciousTerms[$Category] | Where-Object { $EventContent -match [regex]::Escape($_) }
                if ($Matches) {
                    $DetectedPatterns += "[$Category] $($Matches -join ', ')"
                }
            }

            if ($DetectedPatterns -or $SearchIdentifier) {
                Write-AnalysisLog "`nSuspicious Activity Detected" -Silent
                Write-AnalysisLog "------------------------" -Silent
                Write-AnalysisLog "Timestamp: $($Event.TimeCreated)" -Silent
                Write-AnalysisLog "ScriptBlock ID: $ScriptID" -Silent
                
                if ($DetectedPatterns) {
                    Write-AnalysisLog "Detected Patterns:`n$($DetectedPatterns | ForEach-Object { "  - $_" })" -Silent
                }
                
                if ($SearchIdentifier) {
                    Write-AnalysisLog "Specified Identifier Found: $SearchIdentifier" -Silent
                    $ReducedContent = Write-ReducedCodeContent -Content $EventContent -SearchTerm $SearchIdentifier
                    Write-AnalysisLog "`nRelevant Event Content:`n$ReducedContent" -Silent
                } else {
                    Write-AnalysisLog "`nEvent Details:`n$EventContent`n" -Silent
                }
            }
        }
    }
    catch {
        Write-AnalysisLog "Analysis Error: $_" "Error"
        return $false
    }
        Write-Host "`rAnalyzing events... 100%" -ForegroundColor Green
        Write-Host "Analysis complete! Results have been saved to:`n$ResultsFile" -ForegroundColor Green
        Write-Host "----------------------------------------" -ForegroundColor White
        return $true
}

function Combine-ScriptBlockContent {
    param (
        [Parameter(Mandatory=$true)]
        [string]$TargetScriptBlockID
    )
    
    try {
        Write-Host "`nSearching for ScriptBlock events... " -NoNewline
        
        $AllRelatedEvents = Get-WinEvent -FilterHashtable @{
            Path = $EventLogPath
            ProviderName = "Microsoft-Windows-PowerShell"
        } | Where-Object { $_.Message -like "*ScriptBlock ID: $TargetScriptBlockID*" }

        # Separate creation and execution events
        $CreationLog = $AllRelatedEvents | Where-Object { $_.Id -eq 4104 }
        $ExecutionLog = $AllRelatedEvents | Where-Object { $_.Id -eq 4103 }

        if (-not $CreationLog) {
            Write-Host "Not Found" -ForegroundColor Yellow
            Write-Host "No creation events found for ScriptBlock: $TargetScriptBlockID" -ForegroundColor Yellow
            return
        }

        Write-Host "Found" -ForegroundColor Green
        Write-Host "Processing ScriptBlock... 0%" -NoNewline

        # Sort and combine script content
        $OrderedEvents = $CreationLog | Sort-Object { $_.Properties[0].Value }
        $ExpectedParts = $OrderedEvents[0].Properties[0].Value
        $FoundParts = $OrderedEvents.Count

        $OutputPath = Join-Path -Path $CurrentDir -ChildPath "ScriptBlock_${TargetScriptBlockID}.ps1"
        
        # Process events with progress
        $CompleteScript = ""
        $Current = 0
        
        foreach ($Event in $OrderedEvents) {
            $Current++
            $ProgressPercentage = [math]::Round(($Current / $FoundParts) * 100)
            Write-Host "`rProcessing ScriptBlock... $ProgressPercentage%" -NoNewline
            $CompleteScript += $Event.Properties[2].Value
        }
        
        Write-Host "`rProcessing ScriptBlock... 100%" -ForegroundColor Green
        
        $CompleteScript | Out-File $OutputPath

        # Generate analysis report
        Write-AnalysisLog "`nScriptBlock Analysis Results" "Info"
        Write-AnalysisLog "-------------------------" "Info"
        Write-AnalysisLog "ScriptBlock ID: $TargetScriptBlockID" "Info"
        Write-AnalysisLog "Created: $($OrderedEvents[0].TimeCreated)" "Info"
        Write-AnalysisLog "Expected Parts: $ExpectedParts" "Info"
        Write-AnalysisLog "Found Parts: $FoundParts" "Info"
        Write-AnalysisLog "Execution Events: $($ExecutionLog.Count)" "Info"
        Write-AnalysisLog "Output Location: $OutputPath" "Info"

        # Integrity checks
        if ($FoundParts -lt $ExpectedParts) {
            Write-AnalysisLog "Warning: Script appears incomplete - missing parts detected" "Warning"
        }

        if (-not $ExecutionLog) {
            Write-AnalysisLog "Note: No execution events found for this ScriptBlock" "Warning"
        }
        else {
            Write-AnalysisLog "First Execution: $($ExecutionLog[0].TimeCreated)" "Success"
        }

        # Security analysis
        $RiskyPatterns = @(
            "Net.WebClient",
            "DownloadString",
            "Invoke-Expression",
            "IEX",
            "Start-Process",
            "-EncodedCommand",
            "Invoke-Command"
        )

        $FoundRisks = $RiskyPatterns | Where-Object { $CompleteScript -match $_ }
        if ($FoundRisks) {
            Write-AnalysisLog "`nSecurity Alert: High-risk patterns detected:" "Warning"
            $FoundRisks | ForEach-Object { Write-AnalysisLog "  • $_" "Warning" }
        }

        Write-Host "`nScript has been successfully created and saved to:`n$OutputPath" -ForegroundColor Green
        Write-Host "----------------------------------------" -ForegroundColor White
        
        if ($FoundRisks) {
            Write-Host "`nWARNING: High-risk patterns were detected in this script!" -ForegroundColor Yellow
            Write-Host "Review the analysis results file for details." -ForegroundColor Yellow
            Write-Host "----------------------------------------" -ForegroundColor White
        }

        Write-AnalysisLog "Analysis completed successfully" "Success"
    }
    catch {
        Write-AnalysisLog "Error during script analysis: $_" "Error"
    }
}

# Main execution flow
Write-Host "`nStarting PowerShell Event Log Analysis..." -ForegroundColor Cyan
$UseSearchTerm = Read-Host "Would you like to search for a specific term? (Y/N)"
$SearchTerm = ""
if ($UseSearchTerm -eq 'Y' -or $UseSearchTerm -eq 'y') {
    $SearchTerm = Read-Host "Enter your search term"
}

if (Search-SuspiciousEvents -SearchIdentifier $SearchTerm) {
    do {
        $CombineResponse = Read-Host "Would you like to create the entire script out of a ScriptBlock ID? (Y/N)"
        if ($CombineResponse -eq 'Y' -or $CombineResponse -eq 'y') {
            $BlockID = Read-Host "Enter the ScriptBlock ID"
            Combine-ScriptBlockContent -TargetScriptBlockID $BlockID
        }
    } while ($CombineResponse -eq 'Y' -or $CombineResponse -eq 'y')
}

Write-Host "`nAnalysis completed - Results saved to: $ResultsFile" -ForegroundColor Green