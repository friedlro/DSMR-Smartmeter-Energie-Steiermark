[Unit]
Description=Smartmeter
After=network.target
[Service]
User=<Angemeldeter Benutzer>
WorkingDirectory= <Pfad zum smartmeter.py oder smartmeter_mqtt.py>
ExecStart=python3 <smartmeter.py oder smartmeter_mqtt.py>
Restart=always
[Install]
WantedBy=multi-user.target
