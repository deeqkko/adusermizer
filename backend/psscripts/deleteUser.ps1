$user = $args[0] | ConvertFrom-Json
$response = @{}

try {
    Remove-ADUser -Identity $user.id -Confirm:$false
    $response | Add-Member Noteproperty status "Deleted"
    $response | Add-Member Noteproperty user $user.distinguished_name
}
catch {
    $response | Add-Member Noteproperty status $Error[0].Exception.Message
}

finally {
    $response | ConvertTo-Json
}