#!/usr/bin/python3
import re
import json
import argparse
import logging
import subprocess as sb
import requests


def setup_logging():
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("subprocess").setLevel(logging.WARNING)


def get_url_compatible_ip(ip):
    if ':' in ip:  # ipv6
        ip = ip.replace("%", "%25")  # url encode %
        return f"[{ip}]"             # add brackets
    return ip      # ipv4


def _ping6_multicast(src_interface_index):
    cmd = (
        f"ping -6 -I {src_interface_index} ff02::1 -c 4 | grep \"DUP!\" | "
        "awk '{print $4}' | sed 's/.$//' | sort -u"
    )
    try:
        ping_replies = sb.check_output(
            cmd, shell=True, stderr=sb.DEVNULL)
    except sb.CalledProcessError as e:
        ping_replies = e.output
    return ping_replies.decode().splitlines()


def print_info(info):
    print(
        "{:<20} {:>20}".format(
            *['ROBOT TYPE:',
              info['robot-type']]
        )
    )
    print(

        "{:<20} {:>20}".format(
            *['PLATFORM:',
                info['LELY_ROOTFS_PLATFORM']]
        )
    )
    print(
        "{:<20} {:>20}".format(
            *['LINUX DISTRIBUTION:',
                info['LELY_ROOTFS_DISTRO']]
        )
    )


def log_endpoint_info_via_api(ip):
    try:
        url = f"http://{get_url_compatible_ip(ip)}:8084/identify"
        response = requests.get(url)
        info = response.json()
        print(f"Found robot with IP: {ip}")
        print_info(info)
    except Exception as e:
        print(f"Couldn't get info for IP: {ip}")
        print('It\'s probably missing the updater service...')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=(
        "Find all robots for the selected interface "
        "and try to get information for them."
        )
    )
    parser.add_argument(
        'interface',
        type=str,
        help='The interface you want to scan'
    )
    args = parser.parse_args()
    interface = args.interface

    print(f'Finding all robots on interface: {interface}')

    # Get all IPv6 addresses for the specified interface
    ips = _ping6_multicast(interface)

    for ip in ips:
        print()
        log_endpoint_info_via_api(ip)
