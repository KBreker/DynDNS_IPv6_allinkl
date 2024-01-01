#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#  dyndns_ipv6_allinkl.py                                                     #
#  ~~~~~~~~~~~~~~~~~~~~~~                                                     #
#                                                                             #
#  Ermittelt die vorherige IPv6-Adresse und vergleicht diese mit der vor-     #
#  herigen. Wenn sich diese geändert hat, wird der DynDNS-Service vom An-     #
#  bieter allinkl.com über die neue IPv6-Adresse informiert.                  #
#                                                                             #
#  Kai Breker, Version 1.1.4 vom 01.01.2024                                   #
#                                                                             #
###############################################################################

import configparser
import logging
import utils.event_logger as event_logger
import os
import sys
from datetime import datetime
from subprocess import run

import requests


def detect_ipv6():
    """
    Ermittelt die IPv6-Adresse über den ip-Befehl; das Interface wird aus der Config-Datei ermittelt

    :return: IPv6-Adresse
    """
    logger.debug("Versuche eine neue IPv6-Adresse zu ermitteln.")
    ipv6 = ""
    command_string = ["ip", "-6", "ad", "sh", f"{interface}"]
    ipv6_addresses = run(command_string, capture_output=True)
    if ipv6_addresses.returncode > 0:
        logger.critical(f"FEHLER: bitte überprüfe die Bezeichnung des Netzwerkadapters '{interface}'")
        sys.exit()

    ipv6_addresses = str(ipv6_addresses).split(sep="\\n")

    for line in ipv6_addresses:
        if "inet6 2" in line and "global dynamic" in line:
            ipv6 = line.strip().split(" ")[1][:-3]

    return ipv6


def send_new_ipv6(ipv6_new):
    """
    Übermittelt die neue IPv6-Adresse an den DynDNS-Service von allinkl.com
    :param ipv6_new: die neue IPv6-Adresse

    :return:
    """
    logger.debug("Neue IPv6-Adresse wird übermittelt.")
    dyndns_string = f"https://{dyndns_username}:{dyndns_password}@{dyndns_url}/?myip6={ipv6_new}"

    result = requests.get(dyndns_string)
    if str(result) == "<Response [200]>":
        logger.info(f"Die IPv6-Adresse hat sich geändert; die neue Adresse {ipv6_new} wurde übermittelt.")
    else:
        logger.error(f"FEHLER: die neue IPv6-Adresse {ipv6_new} konnte nicht übermittelt werden.")
    return


def write_config(script_path, script_name):
    """
    Schreibt die ermittelte IPv6-Adresse und einen Zeitstempel in die Config-Datei
    :param script_path: Pfad dieses Skriptes zur Lokalisierung der Config-Datei
    :param script_name: Dateiname der Config-Datei
    :return:
    """
    logger.debug("Neue IPv6-Adresse und Zeitstempel werden in die Konfigurationsdatei geschrieben.")
    with open(script_path + "/" + script_name + ".cfg", "w") as configfile:
        config_p.set("IP", "IPv6", str(ipv6_actual))
        config_p.set("IP", "timestamp", str(datetime.now()))
        config_p.write(configfile)


def init_logging_system():
    """
    Initialisiert das Logging-System
    :return: init_logger
    :rtype: logging-Klasse
    """

    # Logging initialisieren
    init_logger = event_logger.init_logger(fullpath=os.path.join(os.path.split(os.path.abspath(__file__))[0],
                                                                 os.path.basename(__file__).split(".")[0] + ".log"),
                                           console_level=logging.DEBUG,
                                           log_level=logging.DEBUG)
    init_logger.info(75 * "-")

    return init_logger


if __name__ == "__main__":

    ipv6_saved = ""
    script_path = os.path.split(os.path.abspath(__file__))[0]
    script_name = os.path.basename(__file__).split(".")[0]

    # Logging initalisieren
    logger = init_logging_system()

    try:
        # Einstellungen für die Config-Datei
        logger.debug("Konfigurationsdatei wird ausgelesen.")
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
        logger.critical(f"Die Konfigurationsdatei '{script_name}.cfg' konnte nicht "
                        "gefunden werden. Bitte überprüfe, ob Sie den gleichen Dateinamen "
                        "wie dieses Skript hat und im gleichen Verzeichnis liegt.")
        sys.exit()

    except configparser.NoSectionError:
        logger.critical(f"Die Konfigurationsdatei '{script_name}.cfg' konnte nicht "
                        "gelesen werden. Bitte überprüfe, ob die Struktur dem Beispiel "
                        "entspricht.")
        sys.exit()

    # IP-Adresse überprüfen
    ipv6_actual = detect_ipv6()

    if ipv6_actual == "":
        logger.error("IPv6-Adresse konnte nicht ermittelt werden.")
    elif ipv6_saved != ipv6_actual:
        logger.debug(f"Die aktuelle IPv6-Adresse lautet: {ipv6_actual}")
        send_new_ipv6(ipv6_actual)
        write_config(script_path, script_name)
    else:
        logger.debug("Keine Aktualisierung der IPv6-Adresse erforderlich.")
