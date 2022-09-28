import paramiko
import logging as log
import socket
from config import ssh_private_key_location, ssh_known_hosts_location


def poweroff_endpoint(hostname: str, username: str = "root", port: int = 22):
    """Returns True if the poweroff command can be executed via SSH on the remote host."""
    stderr = None
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_host_keys(ssh_known_hosts_location)
        client.connect(
            hostname=hostname,
            port=port,
            username=username,
            key_filename=ssh_private_key_location
        )
        stdin, stdout, stderr = client.exec_command(
            "sudo systemctl poweroff")

    except paramiko.ssh_exception.AuthenticationException as e:
        log.critical(e)
    except paramiko.ssh_exception.NoValidConnectionsError as e:
        log.critical(e)
    except paramiko.ssh_exception.BadHostKeyException as e:
        log.critical(e)
    except paramiko.ssh_exception.ChannelException as e:
        log.critical(e)
    except paramiko.ssh_exception.IncompatiblePeer as e:
        log.critical(e)
    except socket.gaierror as e:
        log.critical(f"{e.strerror} '{hostname}'.")

    if stderr:
        error = stderr.readlines()
        if error:
            error = error[0].strip()
            log.warning(f"Cannot exec command. Reason: '{error}'")
            return False

    return True
