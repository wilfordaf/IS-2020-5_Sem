$logName = "ProcessMonitoringLog"
try {
    New-EventLog -Source YSN -LogName $logName -ErrorAction Stop
    Write-Host "EventLog ${logName} successfully created"
} catch [System.InvalidOperationException]{
    Write-Error "EventLog ${logName} already exists"
}