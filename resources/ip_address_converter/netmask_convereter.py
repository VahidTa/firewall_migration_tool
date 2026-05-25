from ipaddress import IPv4Network


def netmasker(prefix):
    net = IPv4Network(prefix, strict=False)
    return f"{net.network_address} {net.netmask}"


def nethost(prefix):
    return str(IPv4Network(prefix, strict=False).network_address)


def sub_mask(prefix):
    return str(IPv4Network(prefix, strict=False).netmask)


def prefixer(prefix):
    net = IPv4Network(prefix, strict=False)
    return f"{net.network_address}/{net.prefixlen}"
