#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#  event_logger.py                                                            #
#  ~~~~~~~~~~~~~~~                                                            #
#                                                                             #
#  Sets up the logging system.                                                #
#                                                                             #
#  Kai Breker, Version 1.0.0 vom 01.01.2024                                   #
#                                                                             #
###############################################################################

import logging
import logging.handlers


def init_logger(fullpath, console_level, log_level):
    """
    Konfiguriert das Logging-System
    :param fullpath: vollständiger Pfad für die anzulegende Logdatei
    :type fullpath: string
    :param console_level: Protokollierungs-Level auf Konsolen-Ebene (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    :type console_level: integer
    :param log_level: Protokollierungs-Level auf Logdatei-Ebene (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    :type log_level: integer
    :return: logger
    :rtype: logging-Klasse
    """
    logger = logging.getLogger("event_logger")
    logger.setLevel(log_level)

    log_handler = logging.handlers.RotatingFileHandler(filename=fullpath, maxBytes=512000, backupCount=1)
    log_handler.setLevel(log_level)
    formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    console = logging.StreamHandler()
    console.setLevel(console_level)
    formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger


if __name__ == "__main__":

    print("This is a module and should be imported.\n")
