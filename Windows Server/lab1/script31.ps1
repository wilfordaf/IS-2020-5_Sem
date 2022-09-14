$STR = read-host "Please enter 4 letter string: "

if (-not ($STR -match "^\w{4}$")) {
    echo "Incorrect input"
    exit 1
}

$username = "UPart3$STR"
$groupname = "GPart3$STR"

$userAmount = Get-LocalUser | ? Name -eq $username | measure-object | Select-Object -expand count

if ($userAmount -gt 0){
    Write-Host "User with this name already exists"
    exit 1
}

$groupAmount = Get-LocalGroup | ? Name -eq $groupname | measure-object | Select-Object -expand count

if ($groupAmount -gt 0){
    Write-Host "Group with this name already exists"
    exit 1
}

New-LocalUser -Name $username -NoPassword
Write-Host "Successfully created new user ${username}"

New-LocalGroup -Name $groupname
Write-Host "Successfully created new group ${groupname}"

Add-LocalGroupMember -Group $groupname -Member $username
Write-Host "Successfully added user ${username} to group ${groupname}"

Enable-LocalUser -Name $username
Write-Host "Successfully activated user ${username}"

pause