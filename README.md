# DSMR Samrtmeter mit Mqtt Energie-Steiermark

Installation: </br>

python3 -m venv venv/source ./venv/bin/activate </br>

pip3 install -r pre-requirements.txt </br>

CRYPTOGRAPHY_DONT_BUILD_RUST=1 </br>

pip3 install -r requirements.txt

Start Script:
sudo nano /etc/systemd/system/service_name.service </br>
sudo chomd 644/etc/systemd/system/service_name.service </br>
sudo chmod +x /pfad zu Python Script </br>
sudo systemctl enable Python Script </br>
sudo systemctl start service_name </br>

Um das Script zu stoppen </br>
sudo systemctl stop service_name
