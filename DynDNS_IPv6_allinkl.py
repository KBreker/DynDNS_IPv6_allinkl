#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#  DynDNS_IPv6_allinkl.py                                                     #
#  ~~~~~~~~~~~~~~~~~~~~~~                                                     #
#                                                                             #
#  Ermittelt die vorherige IPv6-Adresse und vergleicht diese mit der vor-     #
#  herigen. Wenn sich diese geändert hat, wird der DynDNS-Service vom An-     #
#  bieter allinkl.com über die neue IPv6-Adresse informiert.                  #
#                                                                             #
#  Kai Breker, Version 1.0.0 (14.08.2023)                                     #
#                                                                             #
###############################################################################

from subprocess import run
import requests
import time
import sys

# Parameter anpassen
interface = "eth0"
dyndns_username = "insert_username_here"
dyndns_password = "insert_password_here"
dyndns_url = "dyndns.kasserver.com"
sleep_timer = 5
ipv6 = ""


def detect_ipv6():
    global ipv6
    command_string = ["ip", "-6", "ad", "sh", f"{interface}"]
    ipv6_addresses = run(command_string, capture_output=True)
    if ipv6_addresses.returncode > 0:
        print(f"FEHLER: bitte überprüfe die Bezeichnung des Netzwerkadapters '{interface}'")
        sys.exit()

    ipv6_addresses = str(ipv6_addresses).split(sep="\\n")

    for line in ipv6_addresses:
        if "global dynamic" in line:
            ipv6 = line.strip().split(" ")[1][:-3]

    return ipv6


def send_new_ipv6(ipv6_new):
    dyndns_string = f"https://{dyndns_username}:{dyndns_password}@{dyndns_url}/?myip6={ipv6}"

    result = requests.get(dyndns_string)
    if str(result) == "<Response [200]>":
        print(f"Die neue IPv6-Adresse {ipv6_new} wurde übermittelt.")
    else:
        print(f"FEHLER: die neue IPv6-Adresse {ipv6_new} konnte nicht übermittelt werden.")
    return


if __name__ == "__main__":

    ipv6_actual = detect_ipv6()
    print(f"Die aktuelle IPv6-Adresse lautet: {ipv6_actual}")

    while True:
        ipv6_new = detect_ipv6()

        if ipv6_new != ipv6_actual:
            send_new_ipv6(ipv6_new)
            ipv6_actual = ipv6_new
            time.sleep(sleep_timer)
