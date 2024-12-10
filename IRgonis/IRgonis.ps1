# IRgonis.ps1
function Show-Banner {
    $banner = @"
    _____ _____                  _     
   |_   _|  __ \                (_)    
     | | | |__) |__ _ ___  _ __  _ ___ 
     | | |  _  // _` / _ \| '_ \| / __|
    _| |_| | \ \ (_| | (_) | | | | \__ \
   |_____|_|  \_\__, \___/|_| |_|_|___/
                 __/ |                  
                |___/                   
   Incident Response Automation Tool
   Execution Time: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@
    Write-Host $banner -ForegroundColor Cyan
}

function Get-Category {
    $categories = @{
        1 = "Actions against Users"
        2 = "Actions against Files"
        3 = "Actions against Processes"
        4 = "Actions against External Entities"
        5 = "Actions against Persistence"
    }
    
    Write-Host "`nAvailable Categories:" -ForegroundColor Yellow
    $categories.GetEnumerator() | Sort-Object Name | ForEach-Object {
        Write-Host "$($_.Key). $($_.Value)"
    }
    
    do {
        $selection = Read-Host "`nSelect a category (1-5)"
    } while ($selection -notmatch '^[1-5]$')
    
    return $selection
}

function Get-UserActions {
    $actions = @{
        1 = @{
            Name = "Disable User Account"
            Command = 'net user "{0}" /active:no'
            Variable = "username"
            Description = "Disables the specified user account to prevent further access"
        }
        2 = @{
            Name = "Force Logout User"
            Command = 'query session "{0}" | ForEach-Object {{ if($_ -match "{0}"){{ $sessionId=$_.Substring(19,9).Trim(); logoff $sessionId }} }}'
            Variable = "username"
            Description = "Forces logout of all sessions for the specified user"
        }
        3 = @{
            Name = "Reset User Password"
            Command = 'net user "{0}" "{1}"'
            Variable = "username,newpassword"
            Description = "Resets the password for the specified user account"
        }
    }
    return $actions
}

function Get-FileActions {
    $actions = @{
        1 = @{
            Name = "Delete File"
            Command = 'Remove-Item -Path "{0}" -Force'
            Variable = "filepath"
            Description = "Forcefully deletes the specified file"
        }
        2 = @{
            Name = "Calculate File Hash"
            Command = 'Get-FileHash -Path "{0}" -Algorithm SHA256'
            Variable = "filepath"
            Description = "Calculates SHA256 hash of the specified file"
        }
        3 = @{
            Name = "Quarantine File"
            Command = 'Move-Item -Path "{0}" -Destination "C:\Quarantine"'
            Variable = "filepath"
            Description = "Moves the specified file to quarantine location"
        }
    }
    return $actions
}

function Get-ProcessActions {
    $actions = @{
        1 = @{
            Name = "Kill Process by Name"
            Command = 'Stop-Process -Name "{0}" -Force'
            Variable = "processname"
            Description = "Forcefully terminates all processes with the specified name"
        }
        2 = @{
            Name = "Kill Process by ID"
            Command = 'Stop-Process -Id "{0}" -Force'
            Variable = "processid"
            Description = "Forcefully terminates the process with the specified ID"
        }
        3 = @{
            Name = "Get Process Details"
            Command = 'Get-Process -Name "{0}" | Select-Object *'
            Variable = "processname"
            Description = "Retrieves detailed information about the specified process"
        }
    }
    return $actions
}

function Get-ExternalActions {
    $actions = @{
        1 = @{
            Name = "Block IP Address"
            Command = @'
            netsh advfirewall firewall add rule name="Block IP - {0}" dir=in action=block remoteip="{0}"
            netsh advfirewall firewall add rule name="Block IP - {0}" dir=out action=block remoteip="{0}"
'@
            Variable = "ipaddress"
            Description = "Blocks all inbound and outbound traffic for the specified IP address"
        }
        2 = @{
            Name = "Disable Network Adapter"
            Command = 'Disable-NetAdapter -Name "{0}" -Confirm:$false'
            Variable = "adaptername"
            Description = "Disables the specified network adapter"
        }
        3 = @{
            Name = "Clear DNS Cache"
            Command = "Clear-DnsClientCache"
            Variable = "none"
            Description = "Clears the DNS resolver cache"
        }
    }
    return $actions
}

function Get-PersistenceActions {
    $actions = @{
        1 = @{
            Name = "Remove Scheduled Task"
            Command = 'Unregister-ScheduledTask -TaskName "{0}" -Confirm:$false'
            Variable = "taskname"
            Description = "Removes the specified scheduled task"
        }
        2 = @{
            Name = "Stop and Disable Service"
            Command = @'
            Stop-Service -Name "{0}" -Force
            Set-Service -Name "{0}" -StartupType Disabled
'@
            Variable = "servicename"
            Description = "Stops and disables the specified service"
        }
        3 = @{
            Name = "Remove Registry AutoRun"
            Command = 'Remove-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -Name "{0}"'
            Variable = "valuename"
            Description = "Removes the specified autorun entry from the registry"
        }
    }
    return $actions
}

function Execute-Action {
    param (
        $ActionInfo,
        $Variables
    )
    
    Write-Host "`nExecuting: $($ActionInfo.Name)" -ForegroundColor Yellow
    Write-Host "Description: $($ActionInfo.Description)" -ForegroundColor Cyan
    
    try {
        $command = $ActionInfo.Command
        
        if ($Variables -is [array]) {
            for ($i = 0; $i -lt $Variables.Count; $i++) {
                # Ensure variables are properly quoted if they contain spaces
                $Variables[$i] = $Variables[$i].ToString().Trim('"')  # Remove existing quotes if any
                $command = $command -f $Variables
            }
        } else {
            $Variables = $Variables.ToString().Trim('"')  # Remove existing quotes if any
            $command = $command -f $Variables
        }
        
        Write-Host "`nExecuting command:" -ForegroundColor Yellow
        Write-Host $command -ForegroundColor Gray
        
        $output = Invoke-Expression $command
        
        Write-Host "`nCommand Output:" -ForegroundColor Green
        if ($output) {
            $output | Format-Table -AutoSize
        } else {
            Write-Host "Command executed successfully with no output." -ForegroundColor Green
        }
    }
    catch {
        Write-Host "`nError executing command:" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
}

# Main script
Clear-Host
Show-Banner

# Check for admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "`nThis script requires administrator privileges. Please run as administrator.`n" -ForegroundColor Red
    exit
}

# Create quarantine directory if it doesn't exist
if (-not (Test-Path "C:\Quarantine")) {
    New-Item -ItemType Directory -Path "C:\Quarantine" | Out-Null
}

while ($true) {
    # Get category selection
    $categoryNum = Get-Category

    # Get actions based on category
    $actions = switch ($categoryNum) {
        1 { Get-UserActions }
        2 { Get-FileActions }
        3 { Get-ProcessActions }
        4 { Get-ExternalActions }
        5 { Get-PersistenceActions }
    }

    # Display available actions
    Write-Host "`nAvailable Actions:" -ForegroundColor Yellow
    $actions.GetEnumerator() | Sort-Object Name | ForEach-Object {
        Write-Host "$($_.Key). $($_.Value.Name)"
    }

    # Get action selection
    do {
        $actionNum = Read-Host "`nSelect an action number"
    } while (-not $actions.ContainsKey([int]$actionNum))

    $selectedAction = $actions[[int]$actionNum]

    # Get required variables
    if ($selectedAction.Variable -ne "none") {
        $variables = @()
        $variableNames = $selectedAction.Variable -split ','
        foreach ($var in $variableNames) {
            $input = Read-Host "Enter $var"
            $variables += $input
        }
    } else {
        $variables = $null
    }

    # Execute the action
    Execute-Action -ActionInfo $selectedAction -Variables $variables

    # Ask if user wants to continue
    $continue = Read-Host "`nDo you want to perform another action? (Y/N)"
    if ($continue -notmatch '^[Yy]') {
        break
    }
    Clear-Host
    Show-Banner
}