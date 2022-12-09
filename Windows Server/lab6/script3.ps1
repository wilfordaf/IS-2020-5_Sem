$taskName = "ProcessMonitoringLog"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\lab6\script2.ps1"

$repetitionInterval = New-TimeSpan -Minutes 3
$repetitionDuration = [timeSpan]::MaxValue
$taskTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(5) -RepetitionInterval $repetitionInterval -RepetitionDuration $repetitionDuration


try{
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $taskTrigger
} catch {
    Write-Error "Scheduled task is already exist"
}