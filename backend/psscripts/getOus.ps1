Get-ADOrganizationalUnit -filter * | `
Select-Object `
 @{N='id';E={$_.ObjectGUID.Guid}},`
 @{N='name';E={$_.Name}},`
 @{N='distinguished_name';E={$_.DistinguishedName}} | ConvertTo-Json