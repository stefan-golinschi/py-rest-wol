import paramiko
import logging as log
import socket


def poweroff_endpoint(hostname: str, username: str = "root", port: int = 22) -> bool:
    """Returns True if the poweroff command can be executed via SSH on the remote host."""
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(
            hostname=hostname,
            port=port,
            username=username
        )
        stdin, stdout, stderr = client.exec_command("systemctl poweroff")

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
    except:
        log.critical(
            f"Unhandled exception when attempting to exec commands on remote host '{username}@{hostname}:{port}'")

    error = stderr.readlines()
    if error:
        error = error[0].strip()
        log.warning(f"Cannot exec command. Reason: '{error}'")
        return False

    return True
