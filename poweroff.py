from remotecmd import RemoteCmd


def poweroff_endpoint(hostname: str, username: str, port: int):
    """Returns True if the poweroff command can be executed via SSH on the remote host."""

    cmd = RemoteCmd(hostname, username, port)

    return cmd.poweroff()
