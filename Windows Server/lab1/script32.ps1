$mode = read-host "Enter 0 for auto ethernet configuration, 1 - for manual: "

if ($mode -eq "0") {
    Set-NetIPInterface -InterfaceAlias Ethernet -Dhcp Enabled
    Set-DnsClientServerAddress -InterfaceAlias Ethernet -ResetServerAddresses
    echo "Ethernet configured in auto mode"
}
elseif ($mode -eq "1") {
    New-NetIPAddress -InterfaceAlias Ethernet -IPAddress 192.168.1.10 -PrefixLength 24 -DefaultGateway 192.168.1.1
    Set-DnsClientServerAddress -InterfaceAlias Ethernet -ServerAddresses 8.8.8.8
    echo "Ethernet configured in manual mode"
}
else {
    echo "Incorrect input"
}

pause