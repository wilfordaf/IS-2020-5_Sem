function Configure-DHCP {
	# Install DHCP
    Install-WindowsFeature DHCP -IncludeManagementTools
    Get-WindowsFeature -Name *DHCP*| Where Installed
	
	# Authorize and create security groups
	$hostname = hostname
	Import-Module DHCPServer
	Add-DhcpServerInDC -DnsName "${hostname}.ysn.local"
	Add-DhcpServerSecurityGroup

	# Disable notification and reboot
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\ServerManager\Roles\12" -Name "ConfigurationState" -Value 2
    Restart-Service -Name DHCPServer -Force
	
    if ($hostname -ne "ad-srv") {
        return
    }

	# Configure scope and failover
    Import-Csv -Path ./DhcpServerScope.csv | Add-DhcpServerv4Scope
    Import-Csv -Path ./DhcpExclusionRange.csv | Add-DhcpServerv4ExclusionRange
    Import-Csv -Path ./DhcpFailover.csv | Add-DhcpServerv4Failover -Force -AutoStateTransition 1
}

Configure-DHCP
pause