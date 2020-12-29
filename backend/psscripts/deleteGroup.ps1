$identity = $args[0]
$response = @{}

try {
    Remove-ADGroup -Identity $identity -Confirm:$false
    $response | Add-Member Noteproperty status "$identity deleted"
}

catch {
    $response | Add-Member Noteproperty error $Error[0].Exception.Message
    $response | Add-Member Noteproperty group $identity
}

finally {
    $response | ConvertTo-Json
}