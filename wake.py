import logging as log
import wakeonlan


def wake_endpoint(ethaddr: str) -> bool:
    """Sends a wake-on-lan magic packet to the specified ``ethaddr``"""
    try:
        wakeonlan.send_magic_packet(ethaddr)
    except ValueError:
        log.critical(
            f"Cannot send magic packet. Ethernet address in wrong format: '{ethaddr}'")
        return False

    return True
