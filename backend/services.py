from fabric import Connection
import socket
import json
import re

def connect(host, user, password):
    conn = Connection(host=host, user=user, connect_timeout=5,connect_kwargs={'password': password})
    return conn

def get_users(connection, sam_account_name):
    """
    Returns a json formatted string of Active Directory designated user. Returns empty object
    if user is not found
    """
    cmd = '''powershell scripts\getUsers.ps1 %s''' %(sam_account_name)
    users = connection.run(cmd, hide="both").stdout
    connection.close()
    users = json.loads(users)
    return users

def connect_domain(connection):
    """
    Connect to domain controller. Returns an object of domain controller properties
    """
    try:    
        dc = connection.run('powershell "Get-ADDomainController -Filter * | ConvertTo-Json"', hide="out").stdout
        dc = json.loads(dc)
    except socket.timeout:
        dc = None
    connection.close()
    return dc

def create_user(connection, user):
    """
    Creates a new Active Directory user
    """ 
    user = json.dumps(user)
    user = "'"+re.sub(r"\s+","",user)+"'"
    user = re.sub(r'"','\\"', user)
    cmd = '''powershell scripts\createUser.ps1 %s''' %(user)
    new_user = connection.run(cmd, hide="out").stdout
    new_user = json.loads(new_user)
    return new_user

    

def delete_user(connection, sam_account_name):
    """
    Deletes Active Directory user. 
    """
    cmd = '''powershell "Remove-ADUser -Identity '%s' -Confirm:$False"'''%(sam_account_name)
    cmd = re.sub(r"\s+"," ",cmd)
    result = connection.run(cmd, hide="both").stdout
    return result