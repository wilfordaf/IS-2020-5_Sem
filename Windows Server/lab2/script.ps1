function Get-Value-By-Key-Csv {
    param([PSCustomObject]$csv, [string]$key)
    $csv.$key
}

# Global Variables
$default_partition = (Get-ADDomainController).DefaultPartition
$domain_controller_name = (Get-ADDomainController).Name
$domain_name = $default_partition -replace "DC="
$domain_name = $domain_name.split(",")[0]

# Arrays for report
$html = @()
$organization_units = @()
$new_groups = @()
$logins = @()
$home_directories = @()

# Check if input file exists
$input_filename = Read-Host "Enter a path to .csv file: "
if (!(Test-Path -Path $input_filename -PathType Leaf)) {
    throw "File with this name does not exist"
}

$input = Import-Csv -Path $input_filename
foreach ($item in $input) {
    # Parse input data
    $full_name = Get-Value-By-Key-Csv -csv $item -key full_name
    $full_name_split = $full_name.Split(" ")

    $post = Get-Value-By-Key-Csv -csv $item -key post

    $department_name = Get-Value-By-Key-Csv -csv $item -key department_name

    $email = Get-Value-By-Key-Csv -csv $item -key email

    $phone = Get-Value-By-Key-Csv -csv $item -key phone

    $login = Get-Value-By-Key-Csv -csv $item -key login

    $password = Get-Value-By-Key-Csv -csv $item -key password
    $password_secure = ConvertTo-SecureString $password -asplaintext -force

    $organization_unit = Get-Value-By-Key-Csv -csv $item -key organization_unit

    $home_dir_path = Get-Value-By-Key-Csv -csv $item -key home_dir_path
    $home_dir_path = "\UsersHome$home_dir_path"

    $roaming_profile_path = Get-Value-By-Key-Csv -csv $item -key roaming_profile_path
    $roaming_profile_path = "\\$domain_controller_name\SharedProfiles$roaming_profile_path"

    $groups = Get-Value-By-Key-Csv -csv $item -key groups 
    $groups = $groups.Split(";")

    # Check if username exists
    if (Get-ADUser -Filter "sAMAccountName -eq '$login'") {
        continue
    }

    # Creating Organization Unit
    if (!(Get-ADOrganizationalUnit -Filter "Name -like '$organization_unit'")) {
        New-ADOrganizationalUnit -Name $organization_unit -Path $default_partition
        Write-Host "Successfully created organizational unit $organization_unit!"
        $organization_units += $organization_unit
    }

    # Creating User with roaming path
    $full_path = "OU=$organization_unit,$default_partition"
    New-ADUser -Name $login -GivenName $full_name_split[1] -Surname $full_name_split[0] -OtherName $full_name_split[2] -DisplayName $full_name -Department $department_name -EmailAddress $email -MobilePhone $phone -Path $full_path -AccountPassword $password_secure -Enabled $true
    Set-ADUser -Identity $login -Profilepath $roaming_profile_path
    Write-Host "Sucessfully added user $login!"
    $logins += $login

    # Creating home directory and mapping it to disk X
    $dir_local_path = "C:$home_dir_path"
    $dir_remote_path = "\\$domain_controller_name\$login$"
    if (!(Test-Path -Path $dir_local_path)) {
        New-Item -Path $dir_local_path -itemType Directory | out-null
        Write-Host "Sucessfully created directory $dir_local_path!"
    }
    $home_directories += $dir_local_path

    New-SmbShare -Name $login$ -Path $dir_local_path -ChangeAccess "$domain_name\$login" | out-null
    Set-ADUser -Identity $login -HomeDirectory $dir_remote_path -HomeDrive X;

    # Creating groups and adding user to them
    foreach ($group in $groups) {
        if (!(Get-ADGroup -Filter "sAMAccountName -eq '$group'" -SearchBase $full_path)) {
            New-ADGroup -Name $group -GroupScope DomainLocal -Path $full_path
            Write-Host "Successfully created group $group!"
            $new_groups += $group
        }
        Add-ADGroupMember $group $login
        Write-Host "Successfully added $login to $group!"
    }
}

# Generate HTML report
$html += $organization_units | ConvertTo-Html -As Table -Fragment -Property @{ l='OU Names'; e={ $_ } } -PreContent "<h2>Organization units total: $($organization_units.Length)</h2>"
$html += $new_groups | ConvertTo-Html -As Table -Fragment -Property @{ l='Group Names'; e={ $_ } } -PreContent "<h2>Groups total: $($new_groups.Length)</h2>"
$html += $logins | ConvertTo-Html -As Table -Fragment -Property @{ l='User Names'; e={ $_ } } -PreContent "<h2>Users total: $($logins.Length)</h2>"
$html += $home_directories | ConvertTo-Html -As Table -Fragment -Property @{ l='Directory paths'; e={ $_ } } -PreContent "<h2>Directories total: $($home_directories.Length)</h2>"
$html | Out-File .\report.html