import ipaddress

LOCAL_SUBNETS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("fe80::/10"),
    ipaddress.ip_network("fc00::/7"),
    # my cox assigned network - make this configurable or discoverable
    ipaddress.ip_network("2600:8800:7480:f000::/56"),
]


def is_local(ip_str):
    ip_obj = ipaddress.ip_address(ip_str)
    return any(ip_obj in subnet for subnet in LOCAL_SUBNETS)


def get_direction(src_ip, dst_ip):
    src_local = is_local(src_ip)
    dst_local = is_local(dst_ip)

    if src_local and dst_local:
        return "internal"
    elif src_local and not dst_local:
        return "upload"
    elif not src_local and dst_local:
        return "download"
    else:
        return "external"  # NAT weirdness
