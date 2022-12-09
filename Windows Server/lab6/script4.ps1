param (
    [string] $input_filename = $null
)

if (!$input_filename) {
    throw "You haven't entered a path!"
}

if (Test-Path -Path $input_filename -PathType Leaf) {
    throw "File with this name already exists"
}

Get-EventLog System | Where-Object {$_.EventID -contains "6009"} | Select -First 10 > $input_filename
Get-HotFix | Sort InstalledOn -Descending | Select-Object HotFixID, InstalledOn -First 5 >> $input_filename

$eventNames = Get-WinEvent -ListLog * | Where-Object {$_.LastWriteTime -GE (Get-Date).AddDays(-1)}

foreach ($name in $eventNames) {
    $name.LogName >> $input_filename
    Get-WinEvent -LogName $name.LogName | Group-Object -Property LevelDisplayName |
    Select-Object Name, Count | Sort-Object -Property Name | Select-Object -First 2 >> $input_filename
}