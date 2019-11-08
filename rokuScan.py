import click
import concurrent.futures
import ipaddress
import os
import pprint
import re
import urllib3
import xml.etree.ElementTree as eTree

from urllib3.exceptions import NewConnectionError, ConnectTimeoutError

device_pool = []


@click.command()
def scan():
    """
    Scans LAN using address resolution protocol for any available devices then .
    :return: List - an list of device dictionaries, removes any "Nones" before returning
    """
    click.echo('Scanning network for devices')
    network_ping_results = os.popen('arp -a').read()
    ip_list = [parse_ip_from_output(i) for i in network_ping_results.split('?')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        {executor.submit(query_ip_address_for_device_info, ip): ip for ip in ip_list}

    if __name__ == '__main__':
        pprint.pprint([device for device in device_pool if device is not None])
    else:
        return [device for device in device_pool if device is not None]


def parse_ip_from_output(output_string):
    """
    Parses ip address out from arp output
    :param output_string - String -
    :return: String, None - either none if device didn't respond or timed out
    """
    if output_string != '':
        ip_address = re.split(' ', output_string.lstrip(), 2)[0][1:-1]

        try:
            if ipaddress.ip_address(ip_address):
                return ip_address
        except ValueError:
            click.echo(f'got {ip_address} instead of ip')


def query_ip_address_for_device_info(ip_address):
    """
    Pings each ip address to see with roku query device,
    checks for response back then will parse device data xml
    :param ip_address: String - ip address IPV4 to ping with device query
    :return: Dictionary - dict is formatted for PyInquirer's choices, and contains available device info
    """
    timeout = urllib3.Timeout(connect=2.0, read=7.0)
    http = urllib3.PoolManager(timeout=timeout)
    if isinstance(ip_address, str):
        url = f'http://{ip_address}:8060/query/device-info'
        try:
            response = http.request('GET', url, retries=False)
            if response.status == 200:
                data = response.data
                if isinstance(data, bytes):
                    tree = eTree.fromstring(data)
                    device = dict()
                    for child in tree:
                        device[child.tag] = child.text
                    device_pool.append(device)
        except NewConnectionError:
            click.echo(f'Unable to establish connection with {ip_address}')
            return None
        except ConnectTimeoutError:
            click.echo(f'Connection timed out connecting to {ip_address}')
            return None


if __name__ == '__main__':
    scan()
