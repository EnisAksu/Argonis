# IRgonis.ps1
# Author: Enis Aksu
# Version: 2.0
# License: Unlicense (Public Domain)

# Initialize Global Variables
$script:logPath = "IRgonis_$(Get-Date -Format 'yyyyMMdd').log"
$script:quarantinePath = "C:\Quarantine"
$script:backupPath = "C:\IRgonis\Backup"
$script:resultPath = "C:\IRgonis\Results"

# Basic Functions
function Write-Log {
    param(
        [string]$Message,
        [ValidateSet('Info', 'Warning', 'Error', 'Success')]
        [string]$Type = 'Info'
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logColors = @{
        'Info' = 'White'
        'Warning' = 'Yellow'
        'Error' = 'Red'
        'Success' = 'Green'
    }
    
    Write-Host "[$timestamp] " -NoNewline
    Write-Host $Message -ForegroundColor $logColors[$Type]
    "[$timestamp] [$Type] $Message" | Out-File -FilePath $logPath -Append
}

function Show-Banner {
    Clear-Host
    $banner = @"
    _____ _____                  _     
   |_   _|  __ \                (_)    
     | | | |__) |__ _ ___  _ __  _ ___ 
     | | |  _  // _` / _ \| '_ \| / __|
    _| |_| | \ \ (_| | (_) | | | | \__ \
   |_____|_|  \_\__, \___/|_| |_|_|___/
                 __/ |                  
                |___/                   
   Incident Response Automation Tool v2.0
   By: Enis Aksu
   Execution Time: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@
    Write-Host $banner -ForegroundColor Cyan
}

function Initialize-Environment {
    $dirs = @($quarantinePath, $backupPath, $resultPath)
    foreach ($dir in $dirs) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Log "Created directory: $dir" -Type Info
        }
    }
}

function Get-Categories {
    return [ordered]@{
        "1" = @{
            "Name" = "Pre-Response Analysis"
            "Description" = "Gather information before taking action"
        }
        "2" = @{
            "Name" = "User Actions"
            "Description" = "Account and access management"
        }
        "3" = @{
            "Name" = "Process Actions"
            "Description" = "Process and service control"
        }
        "4" = @{
            "Name" = "Network Actions"
            "Description" = "Network and connection management"
        }
        "5" = @{
            "Name" = "File Actions"
            "Description" = "File system operations"
        }
        "6" = @{
            "Name" = "Registry Actions"
            "Description" = "Registry management"
        }
        "7" = @{
            "Name" = "Persistence Actions"
            "Description" = "Remove persistence mechanisms"
        }
        "8" = @{
            "Name" = "System Hardening"
            "Description" = "Enhance system security"
        }
        "9" = @{
            "Name" = "WMI Analysis"
            "Description" = "Windows Management Instrumentation analysis"
        }
        "10" = @{
            "Name" = "Shell Extension Analysis"
            "Description" = "Analyze shell extensions and handlers"
        }
        "11" = @{
            "Name" = "Shadow Copy Analysis"
            "Description" = "Volume Shadow Copy Service operations"
        }
        "12" = @{
            "Name" = "DLL Analysis"
            "Description" = "Dynamic Link Library analysis"
        }
        "13" = @{
            "Name" = "Advanced Task Analysis"
            "Description" = "Detailed scheduled task investigation"
        }
    }
}

function Get-PreResponseActions {
    return @{
        "1" = @{
            "Name" = "Show Logged Users"
            "Command" = "query user"
            "Description" = "Display all logged-in users"
            "RequiresParameters" = $false
        }
        "2" = @{
            "Name" = "Active Network Connections"
            "Command" = "netstat -nabo"
            "Description" = "Show all active network connections and owning processes"
            "RequiresParameters" = $false
        }
        "3" = @{
            "Name" = "Running Processes"
            "Command" = "tasklist /v"
            "Description" = "List all running processes with details"
            "RequiresParameters" = $false
        }
        "4" = @{
            "Name" = "System Information"
            "Command" = "systeminfo"
            "Description" = "Display detailed system information"
            "RequiresParameters" = $false
        }
        "5" = @{
            "Name" = "Running Services"
            "Command" = "net start"
            "Description" = "List all running services"
            "RequiresParameters" = $false
        }
        "6" = @{
            "Name" = "Open Shares"
            "Command" = "net share"
            "Description" = "List all network shares"
            "RequiresParameters" = $false
        }
        "7" = @{
            "Name" = "Scheduled Tasks"
            "Command" = "schtasks /query /fo LIST"
            "Description" = "List all scheduled tasks"
            "RequiresParameters" = $false
        }
        "8" = @{
            "Name" = "DNS Cache"
            "Command" = "ipconfig /displaydns"
            "Description" = "Display DNS resolver cache"
            "RequiresParameters" = $false
        }
        "9" = @{
            "Name" = "Network Adapters"
            "Command" = "ipconfig /all"
            "Description" = "Show detailed network adapter information"
            "RequiresParameters" = $false
        }
        "10" = @{
            "Name" = "ARP Cache"
            "Command" = "arp -a"
            "Description" = "Display ARP cache"
            "RequiresParameters" = $false
        }
    }
}

function Get-UserActions {
    return @{
        "1" = @{
            "Name" = "Disable User Account"
            "Command" = 'net user "{0}" /active:no'
            "Description" = "Disable specified user account"
            "RequiresParameters" = $true
            "Parameters" = @("username")
        }
        "2" = @{
            "Name" = "Force User Logout"
            "Command" = 'query session "{0}" | ForEach-Object { if($_ -match "{0}"){{ $sessionId=$_.Substring(19,9).Trim(); logoff $sessionId }} }'
            "Description" = "Force logout all sessions of specified user"
            "RequiresParameters" = $true
            "Parameters" = @("username")
        }
        "3" = @{
            "Name" = "Reset User Password"
            "Command" = 'net user "{0}" "{1}"'
            "Description" = "Reset user password"
            "RequiresParameters" = $true
            "Parameters" = @("username", "new password")
        }
        "4" = @{
            "Name" = "Remove Admin Rights"
            "Command" = 'net localgroup administrators "{0}" /delete'
            "Description" = "Remove user from administrators group"
            "RequiresParameters" = $true
            "Parameters" = @("username")
        }
        "5" = @{
            "Name" = "Show User Details"
            "Command" = 'net user "{0}"'
            "Description" = "Show detailed user information"
            "RequiresParameters" = $true
            "Parameters" = @("username")
        }
    }
}

function Get-ProcessActions {
    return @{
        "1" = @{
            "Name" = "Kill Process by Name"
            "Command" = 'taskkill /F /IM "{0}"'
            "Description" = "Force terminate process by name"
        }
        "2" = @{
            "Name" = "Kill Process by PID"
            "Command" = 'taskkill /F /PID {0}'
            "Description" = "Force terminate process by PID"
        }
        "3" = @{
            "Name" = "Stop Service"
            "Command" = 'net stop "{0}"'
            "Description" = "Stop specified service"
        }
        "4" = @{
            "Name" = "Process Details"
            "Command" = 'tasklist /v /fi "IMAGENAME eq {0}"'
            "Description" = "Show detailed process information"
        }
        "5" = @{
            "Name" = "Service Details"
            "Command" = 'sc queryex "{0}"'
            "Description" = "Show detailed service information"
        }
    }
}

function Get-NetworkActions {
    return @{
        "1" = @{
            "Name" = "Block IP Address"
            "Command" = 'netsh advfirewall firewall add rule name="Block IP - {0}" dir=in action=block remoteip="{0}"'
            "Description" = "Block specified IP address"
        }
        "2" = @{
            "Name" = "Disable Network Adapter"
            "Command" = 'netsh interface set interface "{0}" disable'
            "Description" = "Disable specified network adapter"
        }
        "3" = @{
            "Name" = "Clear DNS Cache"
            "Command" = "ipconfig /flushdns"
            "Description" = "Clear DNS resolver cache"
        }
        "4" = @{
            "Name" = "Remove Network Share"
            "Command" = 'net share "{0}" /delete'
            "Description" = "Remove specified network share"
        }
        "5" = @{
            "Name" = "Block URL in Hosts"
            "Command" = 'Add-Content -Path "$env:windir\System32\drivers\etc\hosts" -Value "127.0.0.1 {0}"'
            "Description" = "Block URL via hosts file"
        }
    }
}

function Get-FileActions {
    return @{
        "1" = @{
            "Name" = "Delete File"
            "Command" = 'Remove-Item -Path "{0}" -Force'
            "Description" = "Delete specified file"
        }
        "2" = @{
            "Name" = "Calculate File Hash"
            "Command" = 'Get-FileHash -Path "{0}" -Algorithm SHA256'
            "Description" = "Calculate SHA256 hash of file"
        }
        "3" = @{
            "Name" = "Move to Quarantine"
            "Command" = 'Move-Item -Path "{0}" -Destination "$quarantinePath"'
            "Description" = "Move file to quarantine"
        }
        "4" = @{
            "Name" = "Show File Details"
            "Command" = 'Get-Item -Path "{0}" | Select-Object *'
            "Description" = "Show detailed file information"
        }
        "5" = @{
            "Name" = "Find Similar Files"
            "Command" = 'Get-ChildItem -Path C:\ -Recurse -Filter "{0}" -ErrorAction SilentlyContinue'
            "Description" = "Find files with similar names"
        }
    }
}

function Get-RegistryActions {
    return @{
        "1" = @{
            "Name" = "Delete Registry Key"
            "Command" = 'Remove-ItemProperty -Path "{0}" -Name "{1}" -Force'
            "Description" = "Delete specified registry key"
        }
        "2" = @{
            "Name" = "Query Registry Value"
            "Command" = 'Get-ItemProperty -Path "{0}" -Name "{1}"'
            "Description" = "Query registry value"
        }
        "3" = @{
            "Name" = "Export Registry Key"
            "Command" = 'reg export "{0}" "$backupPath\reg_backup_$(Get-Date -Format "yyyyMMddHHmmss").reg"'
            "Description" = "Export registry key to file"
        }
        "4" = @{
            "Name" = "Remove AutoRun"
            "Command" = 'Remove-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -Name "{0}" -Force'
            "Description" = "Remove autorun entry"
        }
        "5" = @{
            "Name" = "List Run Keys"
            "Command" = 'Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"'
            "Description" = "List all run keys"
        }
    }
}

function Get-PersistenceActions {
    return @{
        "1" = @{
            "Name" = "Remove Scheduled Task"
            "Command" = 'schtasks /delete /tn "{0}" /f'
            "Description" = "Remove specified scheduled task"
        }
        "2" = @{
            "Name" = "Disable Service"
            "Command" = 'sc config "{0}" start= disabled'
            "Description" = "Disable specified service"
        }
        "3" = @{
            "Name" = "Remove Startup Item"
            "Command" = 'Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "{0}"'
            "Description" = "Remove user startup item"
        }
        "4" = @{
            "Name" = "Clear Startup Folder"
            "Command" = 'Remove-Item -Path "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\*" -Force'
            "Description" = "Clear user startup folder"
        }
        "5" = @{
            "Name" = "List WMI Persistence"
            "Command" = 'Get-WmiObject -Namespace root\subscription -Class __EventFilter'
            "Description" = "List WMI event filters"
        }
    }
}

function Get-SystemHardeningActions {
    return @{
        "1" = @{
            "Name" = "Enable Windows Firewall"
            "Command" = "netsh advfirewall set allprofiles state on"
            "Description" = "Enable Windows Firewall for all profiles"
        }
        "2" = @{
            "Name" = "Disable Remote Desktop"
            "Command" = 'reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 1 /f'
            "Description" = "Disable Remote Desktop connections"
        }
        "3" = @{
            "Name" = "Enable UAC"
            "Command" = 'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 1 /f'
            "Description" = "Enable User Account Control"
        }
        "4" = @{
            "Name" = "Disable Guest Account"
            "Command" = "net user guest /active:no"
            "Description" = "Disable built-in guest account"
        }
        "5" = @{
            "Name" = "Enable SMB Signing"
            "Command" = 'reg add "HKLM\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters" /v RequireSecuritySignature /t REG_DWORD /d 1 /f'
            "Description" = "Enable SMB signing"
        }
    }
}

function Get-WMIActions {
    return @{
        "1" = @{
            "Name" = "List WMI Consumers"
            "Command" = "Get-WmiObject -Namespace root\subscription -Class __EventConsumer"
            "Description" = "Show WMI event consumers"
        }
        "2" = @{
            "Name" = "Remove WMI Consumer"
            "Command" = 'Get-WmiObject -Namespace root\subscription -Class __EventConsumer -Filter "Name=''{0}''" | Remove-WmiObject'
            "Description" = "Remove specified WMI consumer"
        }
        "3" = @{
            "Name" = "List WMI Bindings"
            "Command" = "Get-WmiObject -Namespace root\subscription -Class __FilterToConsumerBinding"
            "Description" = "Show WMI filter bindings"
        }
        "4" = @{
            "Name" = "List WMI Filters"
            "Command" = "Get-WmiObject -Namespace root\subscription -Class __EventFilter"
            "Description" = "Show WMI event filters"
        }
        "5" = @{
            "Name" = "Check WMI Repository"
            "Command" = "Get-ChildItem $env:SystemRoot\System32\wbem\Repository -Recurse | Measure-Object -Property Length -Sum"
            "Description" = "Check WMI repository size"
        }
    }
}

function Get-ShellExtensionActions {
    return @{
        "1" = @{
            "Name" = "List Context Menu"
            "Command" = "Get-ItemProperty 'Registry::HKEY_CLASSES_ROOT\*\shell\*'"
            "Description" = "Show context menu extensions"
        }
        "2" = @{
            "Name" = "Remove Shell Extension"
            "Command" = 'Remove-Item "Registry::HKEY_CLASSES_ROOT\*\shell\{0}" -Recurse'
            "Description" = "Remove specified shell extension"
        }
        "3" = @{
            "Name" = "List BHOs"
            "Command" = 'Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Browser Helper Objects\*"'
            "Description" = "List browser helper objects"
        }
        "4" = @{
            "Name" = "Remove BHO"
            "Command" = 'Remove-Item "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Browser Helper Objects\{0}" -Recurse'
            "Description" = "Remove specified BHO"
        }
        "5" = @{
            "Name" = "Check Shell Extensions"
            "Command" = 'Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved"'
            "Description" = "List approved shell extensions"
        }
    }
}

function Show-CategoryMenu {
    $categories = Get-Categories
    Write-Host "`nAvailable Categories:" -ForegroundColor Yellow
    $categories.GetEnumerator() | Sort-Object {[int]$_.Key} | ForEach-Object {
        Write-Host "$($_.Key). $($_.Value.Name) - $($_.Value.Description)"
    }
    
    do {
        $selection = Read-Host "`nSelect a category (1-$($categories.Count))"
        $validSelection = $selection -in $categories.Keys
        if (-not $validSelection) {
            Write-Host "Invalid selection. Please choose between 1 and $($categories.Count)" -ForegroundColor Red
        }
    } while (-not $validSelection)
    
    return $selection
}

function Show-ActionMenu {
    param([string]$Category)
    
    $actionFunction = switch ($Category) {
        "1" { Get-PreResponseActions }
        "2" { Get-UserActions }
        "3" { Get-ProcessActions }
        "4" { Get-NetworkActions }
        "5" { Get-FileActions }
        "6" { Get-RegistryActions }
        "7" { Get-PersistenceActions }
        "8" { Get-SystemHardeningActions }
        "9" { Get-WMIActions }
        "10" { Get-ShellExtensionActions }
        default { @{} }
    }
    
    Write-Host "`nAvailable Actions:" -ForegroundColor Yellow
    $actionFunction.GetEnumerator() | Sort-Object {[int]$_.Key} | ForEach-Object {
        Write-Host "$($_.Key). $($_.Value.Name) - $($_.Value.Description)"
    }
    
    do {
        $selection = Read-Host "`nSelect an action number"
        $validSelection = $selection -in $actionFunction.Keys
        if (-not $validSelection) {
            Write-Host "Invalid selection. Please choose a valid action number" -ForegroundColor Red
        }
    } while (-not $validSelection)
    
    return $actionFunction[$selection]
}

function Execute-Command {
    param(
        [string]$Command,
        [string]$Description,
        [array]$Parameters = $null
    )
    
    try {
        Write-Log "Executing: $Description" -Type Info
        Write-Log "Command: $Command" -Type Info
        
        # Only format if we have parameters and the command needs them
        if ($null -ne $Parameters -and $Parameters.Count -gt 0 -and $Command.Contains("{0}")) {
            $Command = $Command -f $Parameters
        }
        
        $output = Invoke-Expression $Command
        
        Write-Log "Command executed successfully" -Type Success
        return $output
    }
    catch {
        Write-Log "Error executing command: $_" -Type Error
        return $null
    }
}
# Main script execution
try {
    # Check for admin privileges
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
        Write-Host "This script requires administrator privileges. Please run as administrator.`n" -ForegroundColor Red
        exit
    }
    
    Show-Banner
    Initialize-Environment
    
    Write-Log "IRgonis started successfully" -Type Success
    
    while ($true) {
        $categorySelection = Show-CategoryMenu
        $selectedAction = Show-ActionMenu -Category $categorySelection
        
        if ($selectedAction.RequiresParameters) {
    $parameters = @()
    $paramCount = ($selectedAction.Command.ToCharArray() | Where-Object {$_ -eq '{'} | Measure-Object).Count
    
    for ($i = 0; $i -lt $paramCount; $i++) {
        $paramPrompt = if ($selectedAction.Parameters -and $selectedAction.Parameters[$i]) {
            $selectedAction.Parameters[$i]
        } else {
            "parameter $($i + 1)"
        }
        $parameters += Read-Host "Enter $paramPrompt"
    }
    
    $output = Execute-Command -Command $selectedAction.Command -Description $selectedAction.Description -Parameters $parameters
}
else {
    $output = Execute-Command -Command $selectedAction.Command -Description $selectedAction.Description
}
        
        if ($output) {
            Write-Host "`nCommand Output:" -ForegroundColor Green
            $output | Format-Table -AutoSize
        }
        
        $continue = Read-Host "`nDo you want to perform another action? (Y/N)"
        if ($continue -notmatch '^[Yy]') {
            break
        }
        
        Clear-Host
        Show-Banner
    }
}
catch {
    Write-Log "An error occurred: $_" -Type Error
}
finally {
    Write-Log "IRgonis session ended" -Type Info
}