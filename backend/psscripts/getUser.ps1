$user = $args[0]

try {
    $users = Get-ADUser -Identity $user
}
catch [ Microsoft.ActiveDirectory.Management.ADIdentityNotFoundException ] {
    $users = New-Object -TypeName PSObject
}
finally {
    $users | ConvertTo-Json
}