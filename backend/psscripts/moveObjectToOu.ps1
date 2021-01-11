$props = $args[0] | ConvertFrom-Json
$name = $props.name
$ou = @{}

try {
    Move-ADObject -Identity $props.identity -TargetPath $props.targetpath
    $ou = Get-ADObject -Identity $props.identity |`
    Select-Object `
    @{N='id';E={$_.ObjectGUID.Guid}},`
    @{N='name';E={$_.Name}},`
    @{N='distinguished_name';E={$_.DistinguishedName}}
}
catch {
    $ou | Add-Member Noteproperty status $Error[0].Exception.Message
}
finally {
    $ou | ConvertTo-Json
}
