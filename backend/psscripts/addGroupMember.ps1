$userAndGroup = $args[0] | ConvertFrom-Json

try {
    Add-ADGroupMember -Identity $userAndGroup.group -Members $userAndGroup.user
    $response = Get-ADGroupMember -Identity $userAndGroup.group |`
    Select-Object distinguishedName
}
catch {
    $response = @{}
    $response | Add-Member Noteproperty status $Error[0].Exception.Message
}
finally {
    $response | ConvertTo-Json
}