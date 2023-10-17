[Unit]
Description=mytest
After=network.target
[Service]
User=<Benutzer>>
WorkingDirectory= <Pfad zu Python Script>
ExecStart=python3 <Python Sript>
Restart=always
[Install]
WantedBy=multi-user.target