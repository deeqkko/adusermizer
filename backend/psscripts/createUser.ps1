$user = $args[0] | ConvertFrom-Json 
$newUser = New-Object -TypeName PSObject

try { 
   $pw = ConvertTo-SecureString $user.account_password -AsPlainText -Force;
   New-ADUser -Name $user.sam_account_name `
    -SamAccountName $user.sam_account_name `
    -UserPrincipalName $user.user_principal_name `
    -GivenName $user.given_name `
    -Surname $user.surname `
    -AccountPassword $pw `
    -ChangePasswordAtLogon 1 `
    -Enabled 1; 
    $newUser = Get-ADUser -Identity $user.sam_account_name | `
    Select-Object `
     @{N='id';E={$_.ObjectGUID.Guid}}, `
     @{N='user_principal_name';E={$_.UserPrincipalName}}, `
     @{N='distinguished_name';E={$_.DistinguishedName}}, `
     @{N='sam_account_name';E={$_.SamAccountName}}
    }
catch [ Microsoft.ActiveDirectory.Management.ADIdentityAlreadyExistsException ] {
    $newUser | Add-Member Noteproperty status "User already exists"
    $newUser | Add-Member Noteproperty user $user.user_principal_name;
}
finally {
    $newUser | ConvertTo-Json
}