Get-ADGroup -filter * | `
Select-Object `
 @{N='id';E={$_.ObjectGUID.Guid}},`
 @{N='name';E={$_.Name}},`
 @{N='sam_account_name';E={$_.SamAccountName}},`
 @{N='group_category';E={$_.GroupCategory}},`
 @{N='group_scope';E={$_.GroupScope}},`
 @{N='display_name';E={$_.DisplayName}},`
 @{N='distinguished_name';E={$_.DistinguishedName}},`
 @{N='description';E={$_.Description}} | ConvertTo-Json