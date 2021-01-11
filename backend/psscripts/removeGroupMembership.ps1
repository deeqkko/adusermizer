$userAndGroup = $args[0] | ConvertFrom-Json
$response = @{}

try {
    Remove-ADGroupMember -Identity $userAndGroup.group -Members $userAndGroup.user -Confirm:$false
    $user = Get-ADUser -Identity $userAndGroup.user | Select-Object DistinguishedName
    $group = Get-ADGroup -Identity $userAndGroup.group | Select-Object DistinguishedName
    $response | Add-Member Noteproperty status "Removed"
    $response | Add-Member Noteproperty user $user
    $response | Add-Member Noteproperty group $group
}
catch {
    
    $response | Add-Member Noteproperty status $Error[0].Exception.Message
}
finally {
    $response | ConvertTo-Json
}