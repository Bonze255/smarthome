
.. role:: bluesup

##########################################
SmartHomeNG installieren :bluesup:`update`
##########################################

- Schritte der Installation:
    - zusätzliche Pakete installieren
    - Quellcode laden
    - Erstmalige Konfiguration erstellen
    - Zusätzliche Python Module installieren
    - SmartHomeNG starten
    - Backend Plugin nutzen


zusätzliche Pakete installieren
-------------------------------

Zunächst müssen einige zusätzlichen Pakete erfüllt werden:

.. code-block:: bash

   sudo apt-get -y install dialog python3 python3-dev python3-setuptools unzip build-essential
   sudo apt-get install python3-pip


Dann noch Pythons Paketmanager PIP auf den neuesten Stand bringen:

.. code-block:: bash

   sudo python3 -m pip install --upgrade pip


Quellcode laden
---------------

SmartHomeNG Dateien vom github holen:

Die folgenden Kommandos am besten mit dem User Account (smarthome) durchführen unter dem später SmartHomeNG laufen soll.

.. code-block:: bash

   cd /usr/local
   sudo mkdir smarthome
   sudo chown -R smarthome:smarthome /usr/local/smarthome

   cd smarthome
   git clone git://github.com/smarthomeNG/smarthome.git .

   mkdir plugins
   cd plugins
   git clone git://github.com/smarthomeNG/plugins.git .
   cd ..
   python3 tools/build_requirements.py


Bitte auf den Punkt am Ende der **git clone** Kommandos achten!

Das letzte Kommando sorgt dafür, dass die Python Requirements (../requirements/all.txt) aktuell generiert werden.


Erstmalige Konfiguration erstellen
----------------------------------

smarthome.yaml
~~~~~~~~~~~~~~

In der **smarthome.yaml** stehen die allgemeinen Konfigurationseinstellungen der SmartHomeNG Installation, wie z.B. die
Koordinaten des Standortes. Die Koordinaten werden benötigt um unter anderem Sonnenaufgang / -untergang zu berechnen.
Die Koordinaten für einen Standort kann man z.B. auf http://www.mapcoordinates.net/de ermitteln.

Wenn keine Datei **smarthome.yaml** existiert, wird beim ersten Start von SmartHomeNG die mitgelieferte Datei **smarthome.yaml.default**
kopiert. Anschießend kann **smarthome.yaml** bearbeitet werden. Damit die Änderungen wirksam werden, muss SmartHomeNG im
Anschluß neu gestartet werden.

Der Inhalt von **smarthome.yaml** sollte mit einem Editor (z.B. **nano**) angepasst werden. Bei anderen Editoren ist darauf
zu achten, dass sie die Datei im UTF-8 Format schreiben.


plugin.yaml
~~~~~~~~~~~

In der **plugin.yaml** stehen die Plugins die verwendet werden sollen, sowie ihre Konfigurationsparameter.

Wenn keine Datei **plugin.yaml** existiert, wird beim ersten Start von SmartHomeNG die mitgelieferte Datei **plugin.yaml.default**
kopiert. In dieser Datei ist ein minimaler Set von Plugins konfiguriert, so dass z.B. per Browser oder mit der smartVISU auf die
SmartHomeNG Instanz zugegriffen werden kann.

.. code-block:: yaml

   %YAML 1.1
   ---
   BackendServer:
       plugin_name: backend
       #updates_allowed: False

   cli:
       plugin_name: cli
       ip: 0.0.0.0
       #port: 2323
       update: True
       #hashed_password: 1245a9633edf47b7091f37c4d294b5be5a9936c81c5359b16d1c48337$

   # Bereitstellung eines Websockets zur Kommunikation zwischen SmartVISU und SmartHomeNG
   websocket:
       plugin_name: visu_websocket
       #ip: 0.0.0.0
       #port: 2424
       #tls: no
       #wsproto: 4
       #acl: rw


Die Konfiguration weitere Plugins ist auskommentiert vorhanden, um die Nutzung dieser Plugins möglichst einfach zu
gestalten.


Zusätzliche Python Module installieren
--------------------------------------

Für den ersten Start müssen noch einige Python Packages nachgeladen werden, dazu muss für den Core eine Requirements-Datei
erstellt werden und anschliend müssen die in dieser Datei (**requirements/base.txt**) angegebenen Module installiert werden.

Zum erstellen der Datei folgende Befehle eingeben:

.. code-block:: bash

   cd /usr/local/smarthome
   python3 tools/build_requirements.py


Anschließend die Packages mit folgenden Befehlen installieren:

.. code-block:: bash

   cd /usr/local/smarthome
   sudo pip3 install -r requirements/base.txt

Mit diesen Befehlen werden die benötigten Python Packages für den Core und die Module von SmartHomeNG installiert.


Jedes Plugin kann weitere Abhängigkeiten mit sich bringen. Diese sind einzeln zu installieren mit

.. code-block:: bash

   sudo pip3 install -r plugins/<plugin-name-hier-einsetzen>/requirements.txt


oder aber alternativ kann man auch sämtliche von allen Plugins benötigten Python Packages nachladen über

.. code-block:: bash

   cd /usr/local/smarthome
   python3 tools/build_requirements.py

   sudo pip3 install -r requirements/all.txt

Die Datei **requirements/all.txt** installiert auch die vom Core benötigten Packages mit. Diese Datei wird mit dem oben
beschriebenen Befehl zum Erstellen der Requirements-Datei mit erstellt.

.. Note::

   Falls der Befehl zum Erstellen der Requirements Dateien (base.txt und all.txt) nicht vorab ausgeführt wird, werden die
   Dateien spätestens beim Start von SmartHomeNG erstellt.

   Es kann allerdings dann zu einem Abbruch des Starts von SmartHomeNG kommen, da beim Start automatisch nur die beiden
   Requirements-Dateien erstellt werden. Die benötigten Python Packages werden dabei nicht automatisch installiert, da
   hierzu erweiterte Rechte (sudo) benötigt werden.


SmartHomeNG starten
-------------------

Erstmalig bietet es sich an, SmartHomeNG im Verbose-Modus zu starten um zu sehen was passiert und ob Fehler auftauchen.
Dafür ausführen:

.. code-block:: bash

   cd /usr/local/smarthome/bin
   python3 ./smarthome.py -v


Jetzt sollten jede Menge Logging-Meldungen über den Bildschirm laufen, die sehen in etwa so aus:

.. code-block:: text

   2018-05-21  00:10:38 WARNING  __main__            --------------------   Init SmartHomeNG 1.4   --------------------
   2018-05-21  00:10:38 INFO     lib.scheduler       Init Scheduler
   2018-05-21  00:10:40 INFO     plugins.backend     WebInterface: Running from '/usr/local/shng_dev/plugins/backend/webif'
   2018-05-21  00:10:40 INFO     plugins.backend     BackendSysteminfo __init__
   2018-05-21  00:10:40 INFO     plugins.backend     BackendServices __init__
   2018-05-21  00:10:40 INFO     plugins.backend     BackendItems __init__ <lib.item.Items object at 0x7fc4e61d84a8>
   2018-05-21  00:10:40 INFO     plugins.backend     BackendLogics __init__ self.logics = None
   2018-05-21  00:10:40 INFO     plugins.backend     BackendLogics __init__ self.plugins = <lib.plugin.Plugins object at 0x7fc4e61d8898>
   2018-05-21  00:10:40 INFO     plugins.backend     BackendLogics __init__ self.scheduler = <Scheduler(Scheduler, started 140483646863104)>
   2018-05-21  00:10:40 INFO     plugins.backend     BackendSchedulers __init__ self.scheduler = <Scheduler(Scheduler, started 140483646863104)>
   2018-05-21  00:10:40 INFO     plugins.backend     BackendPlugins __init__ self.plugins = <lib.plugin.Plugins object at 0x7fc4e61d8898>
   2018-05-21  00:10:40 INFO     plugins.backend     BackendScenes __init__
   2018-05-21  00:10:40 INFO     plugins.backend     BackendThreads __init__
   2018-05-21  00:10:40 INFO     plugins.backend     BackendLogging __init__
   2018-05-21  00:10:40 WARNING  lib.shyaml          YAML-file not found: /usr/local/shng_dev/plugins/logconf/plugin.yaml
   2018-05-21  00:10:40 ERROR    lib.plugin          Plugins, section logconf: class_name is not defined
   2018-05-21  00:11:00 WARNING  plugins.knx         Using busmonitor (L) = 'logger'
   2018-05-21  00:11:01 INFO     plugins.mqtt        Connecting to broker. Starting mqtt client 'SmartHomeNG'


Vorne steht Datum und Uhrzeit, dann der Loglevel (ERROR, WARNING, INFO), dann je nach Setup in der Datei logging.yaml
noch Name bzw. Modul oder Thread und ein Meldungstext der den Logeintrag beschreibt.

Wichtig ist es nach CRITICAL, ERROR und WARNING zu schauen und zu versuchen diese zu vermeiden.
Meldungen der Level INFO und DEBUG sind normal und brauchen erstmal nicht weiter beachtet zu werden.


Backend Plugin nutzen
---------------------

Wenn jetzt erstmal SmartHomeNG am Laufen ist, sollte auch das Backend funktionieren. Dazu kann man im Browser unter der
Adresse **http://<IP vom SmartHomeNG>:8383** den Zugriff prüfen.

Initial ist SmartHomeNG ohne Benutzer Anmeldung konfiguriert. Wenn ein Zugriff nur mit User/Password möglich sein soll,
muss dieses im Abschnitt **http:** in **../etc/module.yaml** konfiguriert werden.

Der Backendserver ist unabhängig von der smartVISU und funktioniert auch dann, wenn kein visu Plugin geladen ist.

Hier sind ein paar Bilder vom Backendserver, um einen Eindruck zu vermitteln:


Der Item-Tree
~~~~~~~~~~~~~

.. image:: assets/backend_items.jpg
   :class: screenshot


Die Dienste/Tools Seite
~~~~~~~~~~~~~~~~~~~~~~~

.. image:: assets/backend_dienste.jpg
   :class: screenshot


Die Logik-Liste
~~~~~~~~~~~~~~~

.. image:: assets/backend_logiken.jpg
   :class: screenshot


Die Szenen Übersicht
~~~~~~~~~~~~~~~~~~~~

.. image:: assets/Backend_Szenen.jpg
   :class: screenshot

