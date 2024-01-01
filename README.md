Dieses Programm ermittelt die aktuelle IPv6-Adresse und vergleicht diese mit der vorherigen. Wenn sich diese geändert hat, wird der DynDNS / DDNS-Service vom Anbieter [all-inkl.com](https://all-inkl.com/) über die neue IPv6-Adresse informiert, damit auch eine Erreichbarkeit mittels IPv4 sichergestellt ist.

Es werden die Module 'requests' und 'configparser' benötigt, die mittels 
`python -m pip install requests`
und
`python -m pip install configparser`
installiert werden können.

In einer Konfigurationsdatei müssen noch Einstellungen vorgenommen werden. Die Datei *'DynDNS_IPv6_allinkl_example.cfg'* kann entsprechend angepasst werden. Die Konfigurationsdatei muss den gleichen Namen tragen, wie das Skript. Folgende Einstellungen sind erforderlich:

**Abschnitt [General]**  
- **interface**: hier ist die Bezeichnung des abzufragenden Netzwerk-Adapters einzutragen, z.B: *eth0* oder *enp4s0*.

**Abschnitt [Credentials]**  
Das Skript ist speziell für Kunden des Anbieters [all-inkl.com](https://all-inkl.com/) erstellt. Sofern es der dortige Tarif des eigenen DDNS-Dienstes unterstützt, können unter *Tools*, *DDNS-Einstellungen* die erforderlichen Einstellungen entnommen werden.
- **dyndns_username**: der Benutzername beginnt üblicherweise mit dyn...
- **dyndns_password**: das Passwort kann ebenfalls dem KAS entnommen werden.
- **dyndns_url**:  der Server ist unter `dyndns.kasserver.com` zu erreichen und muss in der Regel nicht angepasst werden.

**Abschnitt [IP]**  
Diese Eintragungen bleiben leer - hier werden die ermittelte IP und der Zeitstempel eingetragen.

Das Skript sollte dann über die Crontab ausgeführt werden, in diesem Beispiel jede Minute:

`*/1 * * * *   python3 /pfad_zum_skript/DynDNS_IPv6_allinkl.py`
