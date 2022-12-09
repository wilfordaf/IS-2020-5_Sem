Write-Output "Available disks in system:"
$disks = Get-Disk
$disks

$diskNumbers = $disks.Number
$selectedDisk = Read-Host "`nSelect the disk number to create NTFS volume"
if ($diskNumbers -notcontains $selectedDisk) {
    Write-Error -Message "Disk $diskNumber does not exist" -ErrorAction 'Stop'
}

Write-Host "`nWarning, all data on the volume will be lost! You sure you wish to continue?"
$reply = Read-Host "Type [Y / N] to continue / refuse"

if ($reply -eq "y") {
    Set-Disk $selectedDisk -IsOffline $false
    Set-Disk $selectedDisk -IsReadOnly $false
    New-Partition -DiskNumber $selectedDisk -DriveLetter T -Size 1GB | Out-Null
    Format-Volume -DriveLetter T -FileSystem NTFS -Confirm: $false | Out-Null
    Write-Host "`nVolume T successfully created. Checking for corruption..."
    Repair-Volume -DriveLetter T
    Write-Host "`nInformation about volume T:"
    Get-Volume -DriveLetter T
}

pause