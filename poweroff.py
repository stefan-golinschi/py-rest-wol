import paramiko

def poweroff_endpoint(hostname:str, username:str = "root", port:int = 22):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(
        hostname=hostname,
        port=port,
        username=username
    )

    return client.exec_command("systemctl poweroff")
