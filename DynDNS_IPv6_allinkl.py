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
#  Kai Breker, Version 1.1.0 (14.08.2023)                                     #
#                                                                             #
###############################################################################

import configparser
import os
import sys
from subprocess import run
from datetime import datetime

import requests


def detect_ipv6():

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
    dyndns_string = f"https://{dyndns_username}:{dyndns_password}@{dyndns_url}/?myip6={ipv6_new}"

    result = requests.get(dyndns_string)
    if str(result) == "<Response [200]>":
        print(f"Die neue IPv6-Adresse {ipv6_new} wurde übermittelt.")
    else:
        print(f"FEHLER: die neue IPv6-Adresse {ipv6_new} konnte nicht übermittelt werden.")
    return


def write_config(script_path, script_name):
    with open(script_path + "/" + script_name + ".cfg", "w") as configfile:
        config_p.set("IP", "IPv6", str(ipv6_actual))
        config_p.set("IP", "timestamp", str(datetime.now()))
        config_p.write(configfile)


if __name__ == "__main__":

    script_path = os.path.split(os.path.abspath(__file__))[0]
    script_name = os.path.basename(__file__).split(".")[0]

    try:
        # Einstellungen für die Config-Datei
        config_file = os.path.join(script_path, script_name + ".cfg")
        config_p = configparser.ConfigParser()
        config_p.read(config_file)

        if not os.path.isfile(config_file):
            raise FileNotFoundError

        # Parameter anpassen
        interface = config_p.get("General", "interface")
        dyndns_username = config_p.get("Credentials", "dyndns_username")
        dyndns_password = config_p.get("Credentials", "dyndns_password")
        dyndns_url = config_p.get("Credentials", "dyndns_url")
        ipv6_saved = config_p.get("IP", "ipv6")

    except FileNotFoundError:
        print(f"Die Konfigurationsdatei '{script_name}.cfg' konnte nicht "
              "gefunden werden. Bitte überprüfe, ob Sie den gleichen Dateinamen "
              "wie dieses Skript hat und im gleichen Verzeichnis liegt.")

    except configparser.NoSectionError:
        print(f"Die Konfigurationsdatei '{script_name}.cfg' konnte nicht "
              "gelesen werden. Bitte überprüfe, ob die Struktur dem Beispiel "
              "entspricht.")
        sys.exit()

    # IP-Adresse überprüfen
    ipv6_actual = detect_ipv6()
    print(f"Die aktuelle IPv6-Adresse lautet: {ipv6_actual}")

    if ipv6_saved != ipv6_actual:
        send_new_ipv6(ipv6_actual)
        write_config(script_path, script_name)
