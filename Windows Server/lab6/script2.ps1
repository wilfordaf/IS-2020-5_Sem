$currentDateTime = Get-Date

$processList = Get-Process -IncludeUserName | Select-Object ID, Name, Path, UserName, CPU, WS 

Write-Host "Current time ${currentDateTime}"
Write-Host "Running processes list:"
$processList

$path = "C:\lab6"
try {
    $name = Get-ChildItem -Path $path -Filter *.csv | Where-Object {$_Name -match ${ProcessMonitoringLog[0-9]+}} | Select-Object Name -Last 1
    $number = $name -replace "[^0-9]" , ''
    $number = [int]$number
} catch {
    $number = 0
}

$number += 1
$filename = "C:\lab6\ProcessMonitoringLog${number}.csv"
try {
    $processList | Export-Csv .\ProcessMonitoring.csv -ErrorAction Stop
    Import-Csv .\ProcessMonitoring.csv | Select-Object *, @{n="Date";e={$currentDateTime}} | Export-Csv $filename -NoTypeInformation -ErrorAction Stop
    Remove-Item -Path .\ProcessMonitoring.csv

    Write-EventLog -LogName ProcessMonitoringLog -Source YSN -EventId 0 -EntryType SuccessAudit -Message "Created log file"
} catch {
    Write-EventLog -LogName ProcessMonitoringLog -Source YSN -EventId 1 -EntryType FailureAudit -Message "Failed to create log file"
}
