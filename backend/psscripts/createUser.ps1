$user = $args[0] | ConvertFrom-Json
$newUser = New-Object -TypeName PSObject

$pw = ConvertTo-SecureString $user.account_password -AsPlainText -Force;
try { 
   New-ADUser -Name $user.sam_account_name `
    -SamAccountName $user.sam_account_name `
    -UserPrincipalName $user.user_principal_name `
    -GivenName $user.given_name `
    -Surname $user.surname `
    -AccountPassword $pw `
    -ChangePasswordAtLogon 1 `
    -Enabled 1; 
    $newUser | Add-Member Noteproperty status "User created";
    $newUser | Add-Member Noteproperty user $user.user_principal_name;
    }
catch [ Microsoft.ActiveDirectory.Management.ADIdentityAlreadyExistsException ] {
    $newUser | Add-Member Noteproperty status "User already exists"
    $newUser | Add-Member Noteproperty user $user.user_principal_name;
}
finally {
    $newUser | ConvertTo-Json
}