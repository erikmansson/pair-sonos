#!/usr/bin/python3

from sys import argv
import requests
import soco

usage_text = """\
commands:
    list [<interface address>]
    pair <left/master> <right/slave>
    unpair <left/master>\
"""

request_address_format = "http://{}:1400/DeviceProperties/Control"

pair_payload_format = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
    '<s:Body>'
    '<u:AddBondedZones xmlns:u="urn:schemas-upnp-org:service:DeviceProperties:1">'
    '<ChannelMapSet>{}:LF,LF;{}:RF,RF</ChannelMapSet>'
    '</u:AddBondedZones>'
    '</s:Body>'
    '</s:Envelope>'
)

unpair_payload_format = (
    '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
    '<s:Body>'
    '<u:RemoveBondedZones xmlns:u="urn:schemas-upnp-org:service:DeviceProperties:1">'
    '<ChannelMapSet></ChannelMapSet>'
    '</u:RemoveBondedZones>'
    '</s:Body>'
    '</s:Envelope>'
)

pair_soap_action = "urn:schemas-upnp-org:service:DeviceProperties:1#AddBondedZones"
unpair_soap_action ="urn:schemas-upnp-org:service:DeviceProperties:1#RemoveBondedZones"

def main_cli():
    num_args = len(argv)

    if num_args < 2:
        print(usage_text)
        return

    cmd = argv[1]

    if cmd == "list":
        if num_args == 2:
            list_socos()
        elif num_args == 3:
            list_socos(argv[2])
        else:
            print("invalid arguments")
    elif cmd == "pair":
        if num_args == 4:
            pair_socos(argv[2], argv[3])
        else:
            print("invalid arguments")
    elif cmd == "unpair":
        if num_args == 3:
            unpair_socos(argv[2])
        else:
            print("invalid arguments")
    else:
        print(usage_text)

def list_socos(interface_addr=None):
    devs = soco.discover(interface_addr=interface_addr)
    for dev in devs:
        ip = dev.ip_address
        name = dev.player_name
        print("{:<15}  {}".format(ip, name))

def pair_socos(l_ip, r_ip):
    l_soco = soco.SoCo(l_ip)
    r_soco = soco.SoCo(r_ip)

    l_uid = l_soco.uid
    r_uid = r_soco.uid

    req_addr = request_address_format.format(l_ip)
    req_headers = {
        "Content-Type": "application/xml",
        "SOAPAction": pair_soap_action,
    }
    req_payload = pair_payload_format.format(l_uid, r_uid)

    response = requests.post(req_addr, data=req_payload, headers=req_headers)

    if response.status_code != 200:
        print("failed to pair")


def unpair_socos(master_ip):
    req_addr = request_address_format.format(master_ip)
    req_headers = {
        "Content-Type": "application/xml",
        "SOAPAction": unpair_soap_action,
    }
    req_payload = unpair_payload_format

    response = requests.post(req_addr, data=req_payload, headers=req_headers)

    if response.status_code != 200:
        print("failed to unpair")

if __name__ == "__main__":
    main_cli()
