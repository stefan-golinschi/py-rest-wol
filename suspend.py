from remotecmd import RemoteCmd


def suspend_endpoint(hostname: str, username: str, port: int):
    """Returns True if the suspend command can be executed via SSH on the remote host."""

    cmd = RemoteCmd(hostname, username, port)

    return cmd.suspend()
