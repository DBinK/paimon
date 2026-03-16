from ping3 import ping
from tcping import Ping as tcping

def ping_host(host):
    delay = ping(host, timeout=1)
    
    if delay is None:
        return None
        
    return delay * 1000


def tcp_ping(host, port=80):
    p = Ping(host, port, timeout=1)
    p.ping(1)
    
    if p.result.raw:
        # 返回毫秒
        return p.result.raw[0].time * 1000
    return None