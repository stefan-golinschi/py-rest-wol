import wakeonlan


def wake_endpoint(ethaddr: str):
    wakeonlan.send_magic_packet(ethaddr)
