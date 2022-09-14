$mode = read-host "Enter 0 for auto ethernet configuration, 1 - for manual: "

if ($mode -eq "0") {
    Set-NetIPInterface -InterfaceAlias Ethernet -Dhcp Enabled
    Set-DnsClientServerAddress -InterfaceAlias Ethernet -ResetServerAddresses
    Write-Host "Ethernet configured in auto mode"
}
elseif ($mode -eq "1") {
	Remove-NetRoute -InterfaceAlias Ethernet | Out-Null
    New-NetIPAddress -InterfaceAlias Ethernet -IPAddress 192.168.1.10 -PrefixLength 24 -DefaultGateway 192.168.1.1
    Set-DnsClientServerAddress -InterfaceAlias Ethernet -ServerAddresses 8.8.8.8
    Write-Host "Ethernet configured in manual mode"
}
else {
    Write-Host "Incorrect input"
}

pause