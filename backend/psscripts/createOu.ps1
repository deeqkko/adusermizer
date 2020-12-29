$newOu = $args[0] | ConvertFrom-Json
$name = $newOu.name


try {
    New-ADOrganizationalUnit -Name $newOu.name -Path $newOu.path
    $ou = Get-ADOrganizationalUnit -Filter 'Name -like $name' |`
    Select-Object `
    @{N='id';E={$_.ObjectGUID.Guid}},`
    @{N='name';E={$_.Name}},`
    @{N='distinguished_name';E={$_.DistinguishedName}}
}

#catch-lohkoon tarvis saada jotakin
catch {
    $ou = @{}
    $ou | Add-Member Noteproperty error $Error[0].Exception.Message
    $ou | Add-Member Noteproperty name $newOu.name
    $ou | Add-Member Noteproperty path $newOu.path
}
finally {
    $ou | ConvertTo-Json
}