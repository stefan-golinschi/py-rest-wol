import paramiko
import logging as log
import socket


class RemoteCmd:
    def __init__(self, hostname: str, username: str = "root", port: int = 22) -> None:
        self.hostname = hostname
        self.username = username
        self.port = port

        self._ssh_private_key_location = "/ssh/id_rsa"
        self._ssh_known_hosts_location = "/ssh/known_hosts"
        self.__connect()

    def __connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.load_host_keys(self._ssh_known_hosts_location)
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                key_filename=self._ssh_private_key_location
            )
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
            log.critical(f"{e.strerror} '{self.hostname}'.")

    def suspend(self):
        stderr = None

        try:
            stdin, stdout, stderr = self.client.exec_command(
                "sudo systemctl suspend")
        except:
            log.critical("Cannot suspend.")

        if stderr:
            error = stderr.readlines()
            if error:
                error = error[0].strip()
                log.warning(f"Reason: '{error}'")
                return False
        return True

    def poweroff(self):
        stderr = None

        try:
            stdin, stdout, stderr = self.client.exec_command(
                "sudo systemctl poweroff")
        except:
            log.critical("Cannot poweroff.")

        if stderr:
            error = stderr.readlines()
            if error:
                error = error[0].strip()
                log.warning(f"Reason: '{error}'")
                return False
        return True
