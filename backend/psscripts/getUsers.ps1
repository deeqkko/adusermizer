$user = $args[0]

try {
    $users = Get-ADUser -Filter * | `
    Select-Object `
     @{N='id';E={$_.ObjectGUID.Guid}}, `
     @{N='user_principal_name';E={$_.UserPrincipalName}}, `
     @{N='distinguished_name';E={$_.DistinguishedName}}, `
     @{N='sam_account_name';E={$_.SamAccountName}}
}
catch [ Microsoft.ActiveDirectory.Management.ADIdentityNotFoundException ] {
    $users = New-Object -TypeName PSObject
}
finally {
    $users | ConvertTo-Json
}