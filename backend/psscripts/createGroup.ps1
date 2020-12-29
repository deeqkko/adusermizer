$group = $args[0] | ConvertFrom-Json
$name = $group.name

$groups = @{}

# Selvitä miksi display_nameen ei tule mitään
try {
    New-ADGroup `
    -GroupScope $group.group_scope `
    -Name $group.name `
    -SamAccountName $group.sam_account_name `
    -GroupCategory $group.group_category `
    -DisplayName $group.display_name `
    -Path $group.distinguished_name `
    -Description $group.description
    $groups = Get-ADGroup -filter 'Name -like $name' | `
    Select-Object `
     @{N='id';E={$_.ObjectGUID.Guid}},`
     @{N='name';E={$_.Name}},`
     @{N='sam_account_name';E={$_.SamAccountName}},`
     @{N='group_category';E={$_.GroupCategory}},`
     @{N='group_scope';E={$_.GroupScope}},`
     @{N='display_name';E={$_.DisplayName}},`
     @{N='distinguished_name';E={$_.DistinguishedName}},`
     @{N='description';E={$_.Description}}
}
catch {
    $groups | Add-Member Noteproperty status $Error[0].Exception.Message
    $groups | Add-Member Noteproperty group $group
}
finally {
    $groups | ConvertTo-Json
}
