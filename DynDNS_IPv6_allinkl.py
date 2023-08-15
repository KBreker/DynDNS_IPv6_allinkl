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
#  Kai Breker, Version 1.1.2 (15.08.2023)                                     #
#                                                                             #
###############################################################################

import configparser
import logging
import os
import sys
from datetime import datetime
from subprocess import run

import requests


def detect_ipv6():
    ipv6 = ""
    command_string = ["ip", "-6", "ad", "sh", f"{interface}"]
    ipv6_addresses = run(command_string, capture_output=True)
    if ipv6_addresses.returncode > 0:
        print(f"FEHLER: bitte überprüfe die Bezeichnung des Netzwerkadapters '{interface}'")
        sys.exit()

    ipv6_addresses = str(ipv6_addresses).split(sep="\\n")

    for line in ipv6_addresses:
        if "inet6 2" in line and "global dynamic" in line:
            ipv6 = line.strip().split(" ")[1][:-3]

    return ipv6


def send_new_ipv6(ipv6_new):
    dyndns_string = f"https://{dyndns_username}:{dyndns_password}@{dyndns_url}/?myip6={ipv6_new}"

    result = requests.get(dyndns_string)
    if str(result) == "<Response [200]>":
        logging.info(f"Die IPv6-Adresse hat sich geändert; die neue Adresse {ipv6_new} wurde übermittelt.")
    else:
        print(f"FEHLER: die neue IPv6-Adresse {ipv6_new} konnte nicht übermittelt werden.")
    return


def write_config(script_path, script_name):
    with open(script_path + "/" + script_name + ".cfg", "w") as configfile:
        config_p.set("IP", "IPv6", str(ipv6_actual))
        config_p.set("IP", "timestamp", str(datetime.now()))
        config_p.write(configfile)


if __name__ == "__main__":

    ipv6_saved = ""
    script_path = os.path.split(os.path.abspath(__file__))[0]
    script_name = os.path.basename(__file__).split(".")[0]

    # Logging-Einstellungen
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        encoding="utf-8",
                        handlers=[logging.FileHandler(os.path.join(script_path,
                                                      script_name +
                                                      ".log")),
                                  logging.StreamHandler()]
                        )

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
        sys.exit()

    except configparser.NoSectionError:
        print(f"Die Konfigurationsdatei '{script_name}.cfg' konnte nicht "
              "gelesen werden. Bitte überprüfe, ob die Struktur dem Beispiel "
              "entspricht.")
        sys.exit()

    # IP-Adresse überprüfen
    ipv6_actual = detect_ipv6()
    logging.debug(f"Die aktuelle IPv6-Adresse lautet: {ipv6_actual}")

    if ipv6_saved != ipv6_actual:
        send_new_ipv6(ipv6_actual)
        write_config(script_path, script_name)
