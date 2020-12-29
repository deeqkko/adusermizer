from fabric import Connection
import socket
import json
import re
from os import getcwd, listdir

script_path = '/backend/psscripts/'
script_source = getcwd() + script_path
hide_stdout = "out"

def connect(host, user, password):
    conn = Connection(host=host, user=user, connect_timeout=5,connect_kwargs={'password': password})
    return conn

def copy_psscripts(connection):
    home = connection.run('''powershell "Test-Path .\scripts"''', hide=hide_stdout).stdout
    
    if "False" in home:
        connection.run('mkdir scripts')

    script_files = listdir(script_source)

    for file in script_files:
        connection.put(script_source + file, "scripts/")

def delete_psscripts(connection):
    connection.run('rd /s /q scripts')
    # Return-lauseke

#### User methods ####

def get_users(connection):
    """
    Returns a python dict of all users in domain
    """
    cmd = '''powershell scripts\getUsers.ps1'''
    result = connection.run(cmd, hide=hide_stdout).stdout
    result = json.loads(result)
    return result

def get_user(connection, sam_account_name):
    """
    Returns a python dict of Active Directory designated user. Returns empty object
    if user is not found
    """
    cmd = '''powershell scripts\getUser.ps1 %s''' %(sam_account_name)
    users = connection.run(cmd, hide=hide_stdout).stdout
    connection.close()
    users = json.loads(users)
    return users

def create_user(connection, user):
    """
    Creates a new Active Directory user
    """
    user = json.dumps(user)
    user = "'"+re.sub(r"\s+","",user)+"'"
    user = re.sub(r'"','\\"', user)
    cmd = '''powershell scripts\createUser.ps1 %s''' %(user)
    new_user = connection.run(cmd, hide=hide_stdout).stdout
    new_user = json.loads(new_user)
    return new_user

    

def delete_user(connection, sam_account_name):
    """
    Deletes Active Directory user. 
    """
    cmd = '''powershell "Remove-ADUser -Identity '%s' -Confirm:$False"'''%(sam_account_name)
    cmd = re.sub(r"\s+"," ",cmd)
    result = connection.run(cmd, hide=hide_stdout).stdout
    return result

#### Group methods ####

def get_groups(connection):
    cmd = '''powershell scripts\getGroups.ps1'''
    result = connection.run(cmd, hide=hide_stdout).stdout
    groups = json.loads(result)

    if isinstance(groups, dict):
        groups = [groups]
    return groups

def create_group(connection, group):
    group = json.dumps(group)
    group = "'"+re.sub(r"\s+","",group)+"'"
    group = re.sub(r'"','\\"', group)
    cmd = '''powershell scripts\createGroup.ps1 %s''' %(group)
    result = connection.run(cmd, hide=hide_stdout).stdout
    result = json.loads(result)
    return result

def delete_group(connection, group):
    group = "'" + group + "'"
    cmd = '''powershell scripts\deleteGroup.ps1 %s''' %(group)
    result = connection.run(cmd, hide=hide_stdout).stdout
    result = json.loads(result)
    return result

#### Organizational Unit methods ####

def get_organizational_units(connection):
    cmd = '''powershell scripts\getOus.ps1'''
    result = connection.run(cmd, hide=hide_stdout).stdout
    organizational_units = json.loads(result)

    if isinstance(organizational_units, dict):
        organizational_units = [organizational_units]
    return organizational_units

def create_organizational_unit(connection, ou):
    ou = json.dumps(ou)
    ou = "'"+re.sub(r"\s+","",ou)+"'"
    ou = re.sub(r'"','\\"', ou)
    cmd = '''powershell scripts\createOu.ps1 %s''' %(ou)
    print(cmd)
    result = connection.run(cmd, hide=hide_stdout).stdout
    result = json.loads(result)
    return result

def delete_organizational_unit(connection, name):
    name = "'" + name + "'"
    cmd = '''powershell scripts\deleteOu.ps1 %s''' %(name)
    result = connection.run(cmd, hide=hide_stdout).stdout
    result = json.loads(result)
    return result

#### Domain connection methods ####


def connect_domain(connection):
    """
    Connect to domain controller. Returns an object of domain controller properties
    """
    try:    
        dc = connection.run('powershell "Get-ADDomainController -Filter * | ConvertTo-Json"', hide=hide_stdout).stdout
        dc = json.loads(dc)
        copy_psscripts(connection)
    except socket.timeout:
        dc = None
    connection.close()
    return dc

def remove_domain(connection):
    delete_psscripts(connection)
    #Return-lauseke