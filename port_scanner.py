import socket
import ipaddress

from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose=False):
    ip = None

    # ¿Es IP válida?
    try:
        ipaddress.ip_address(target)
        ip = target
    except ValueError:
        # Si no es IP, intentar resolver como hostname
        try:
            ip = socket.gethostbyname(target)
        except socket.gaierror:
            return "Error: Invalid hostname"

    start_port, end_port = port_range[0], port_range[1]
    open_ports = []

    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
        finally:
            s.close()

    if not verbose:
        return open_ports

    lines = [
        f"Open ports for {target} ({ip})",
        "PORT     SERVICE"
    ]

    for port in open_ports:
        service = ports_and_services.get(str(port), "unknown")
        lines.append(f"{port:<9}{service}")

    return "\n".join(lines)
