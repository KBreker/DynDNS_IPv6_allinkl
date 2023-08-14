Dieses Programm ermittelt die vorherige IPv6-Adresse und vergleicht diese mit der vorherigen. Wenn sich diese geändert hat, wird der DynDNS / DDNS-Service vom Anbieter [all-inkl.com](https://all-inkl.com/) über die neue IPv6-Adresse informiert, damit auch eine Erreichbarkeit mittels IPv4 sichergestellt ist.

Es wird das Modul 'requests' benötigt, das mittels 
`python -m pip install requests`
installiert werden kann.

Im Code müssen folgende Einstellungen vorgenommen werden:

- **interface**: hier ist die Bezeichnung des abzufragenden Netzwerk-Adapters einzutragen, z.B: *eth0* oder *enp4s0*.

Das Skript ist speziell für Kunden des Anbieters [all-inkl.com](https://all-inkl.com/) erstellt. Sofern der dortige Tarif des eigenen DDNS-Dienstes unterstützt, können unter *Tools*, *DDNS-Einstellungen* die erforderlichen Einstellungen entnommen werden.
- **dyndns_username**: der Benutzername beginnt üblicherweise mit dyn...
- **dyndns_password**: das Passwort kann ebenfalls dem KAS entnommen werden.
- **dyndns_url**: der Server ist unter `dyndns.kasserver.com` zu erreichen und muss in der Regel nicht angepasst werden.

- **sleep_timer**: hier kann angegeben werden, in welchem Intervall (in Sekunden) die IPv6-Adresse auf eine Änderung überprüft werden soll.


Das Skript sollte dann über die Crontab bei einem Reboot ausgeführt werden:

`@reboot python3 /pfad_zum_skript/DynDNS_IPv6_allinkl.py`
