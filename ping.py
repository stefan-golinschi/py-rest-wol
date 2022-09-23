import subprocess

def ping_endpoint(hostname: str, ping_count: int = 1, ping_timeout:int = 3):

    response = subprocess.run(
        ["ping", "-c", str(ping_count), "-W", str(ping_timeout), hostname],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return response.returncode

