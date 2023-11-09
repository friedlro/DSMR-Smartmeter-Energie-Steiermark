import time
import json
import paho.mqtt.client as mqtt

from serial import Serial, PARITY_NONE, EIGHTBITS, STOPBITS_ONE
from decode import decrypt_frame, convert_to_dict, check_and_encode_frame

GLOBAL_UNICAST_ENC_KEY = "Hier deinen GUEK Key eintragen"
GLOBAL_AUTHENTICATION_KEY = "Hier deinen GAK Key eintragen"
MQTT_BROKER = "MQTT_BROKER_IP_OR_HOSTNAME"
MQTT_PORT = 1883
MQTT_TOPIC = "your/mqtt/topic"
MQTT_USERNAME = "your_mqtt_username"
MQTT_PASSWORD = "your_mqtt_password"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)  # Setzen Sie Benutzernamen und Passwort für die MQTT-Verbindung

if __name__ == "__main__":
    if GLOBAL_UNICAST_ENC_KEY == "":
        raise RuntimeError("Please set the GLOBAL_UNICAST_ENC_KEY")
    if GLOBAL_AUTHENTICATION_KEY == "":
        raise RuntimeError("Please set the GLOBAL_AUTHENTICATION_KEY")

    while True:
        try:
            with Serial('/dev/ttyUSB0', 115200, timeout=6.0,
                        bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE, rtscts=False) as ser:
                data = ser.read(511)
                if len(data) == 0:
                    print("Warte auf Smart Meter...")
                    continue
                decrypted = decrypt_frame(GLOBAL_UNICAST_ENC_KEY, GLOBAL_AUTHENTICATION_KEY, data)
                encoded_frame = check_and_encode_frame(decrypted)
                response_as_dict = convert_to_dict(encoded_frame)

                # MQTT-Publishing
                client.connect(MQTT_BROKER, MQTT_PORT)
                client.publish(MQTT_TOPIC, json.dumps(response_as_dict))  # Sende Daten als JSON über MQTT

                print("Wird aktuell geliefert: " + str(response_as_dict["1-0:1.7.0"]))
                print("Wird aktuell eingespeist: " + str(response_as_dict["1-0:2.7.0"]))
                print("Wurde geliefert (Zählerstand): " + str(response_as_dict["1-0:1.8.0"]))
                print("Wurde eingespeist (Zählerstand): " + str(response_as_dict["1-0:2.8.0"]))

                client.disconnect()  # Trennen Sie die Verbindung zum MQTT-Broker
        except Exception as e:
            print(e)
            time.sleep(1)
            pass
