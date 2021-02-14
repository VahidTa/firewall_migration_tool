from ipaddress import IPv4Network

def netmasker(prefix):
    return str(IPv4Network(prefix).network_address) + ' ' + str(IPv4Network(prefix).netmask)

def nethost(prefix):
    return str(IPv4Network(prefix).network_address)

def sub_mask(prefix):
    return str(IPv4Network(prefix).netmask)

def prefixer(prefix):
    return str(IPv4Network(prefix).network_address) + '/' +str(IPv4Network(prefix).prefixlen)


