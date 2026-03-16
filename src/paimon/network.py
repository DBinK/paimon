import time
import socket

import httpx
import dns.resolver
from ping3 import ping

from paimon.schema import NetResult


def icmp_ping(host, timeout=2):
    """
    ICMP ping
    """

    try:

        delay = ping(host, timeout=timeout)

        if delay is None:
            return NetResult(False, None, "timeout")

        latency = round(delay * 1000, 2)

        return NetResult(True, latency, "ok")

    except Exception:

        return NetResult(False, None, "error")


def tcp_ping(host, port=80, timeout=2):
    """
    TCP ping
    """

    start = time.perf_counter()

    try:

        sock = socket.create_connection(
            (host, port),
            timeout=timeout
        )

        sock.close()

        latency = (time.perf_counter() - start) * 1000

        return NetResult(True, round(latency, 2), "ok")

    except socket.timeout:

        return NetResult(False, None, "timeout")

    except Exception:

        return NetResult(False, None, "error")


def http_ping(url, timeout=3):
    """
    HTTP ping
    """

    start = time.perf_counter()

    try:

        with httpx.Client(timeout=timeout) as client:

            r = client.head(url)

        latency = (time.perf_counter() - start) * 1000

        if r.status_code >= 400:
            return NetResult(False, round(latency, 2), "http_error")

        return NetResult(True, round(latency, 2), "ok")

    except httpx.TimeoutException:

        return NetResult(False, None, "timeout")

    except Exception:

        return NetResult(False, None, "error")


def dns_ping(domain, dns_server="8.8.8.8"):
    """
    DNS 查询延迟
    """

    resolver = dns.resolver.Resolver()

    resolver.nameservers = [dns_server]

    start = time.perf_counter()

    try:

        resolver.resolve(domain)

        latency = (time.perf_counter() - start) * 1000

        return NetResult(True, round(latency, 2), "ok")

    except dns.resolver.NXDOMAIN:

        return NetResult(False, None, "nxdomain")

    except dns.resolver.Timeout:

        return NetResult(False, None, "timeout")

    except Exception:

        return NetResult(False, None, "error")


if __name__ == "__main__":

    print(icmp_ping("www.baidu.com"))
    print(tcp_ping("www.baidu.com"))
    print(http_ping("https://www.baidu.com"))
    print(dns_ping("www.google.com"))