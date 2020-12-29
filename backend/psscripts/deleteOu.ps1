$identity = $args[0]
$response = @{}

try {
    Set-ADOrganizationalUnit -Identity $identity `
    -ProtectedFromAccidentalDeletion $false
    Remove-ADOrganizationalUnit -Identity $identity -Confirm:$false
    $response | Add-Member Noteproperty status "$identity deleted"
}
catch {
    $response | Add-Member Noteproperty error $Error[0].Exception.Message
    $response | Add-Member Noteproperty identity $identity
}
finally {
    $response | ConvertTo-Json
}