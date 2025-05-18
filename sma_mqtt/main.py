import os
import time
import json
import requests
import paho.mqtt.client as mqtt
from sma_mqtt.sma_keys import SMA_KEYS, HA_DISCOVERY_PREFIX, DEVICE_INFO

SMA_URL = os.environ.get("SMA_URL")
SMA_USER_GROUP = os.environ.get("SMA_USER_GROUP", "istl")
SMA_PASSWORD = os.environ.get("SMA_PASSWORD")
SMA_VERIFY_SSL = os.environ.get("SMA_VERIFY_SSL", "false").lower() == "true"
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
MQTT_USERNAME = os.environ.get("MQTT_USERNAME")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", 30))
DEVICE_ID = os.environ.get("DEVICE_ID", "sma_inverter")


def login():
    resp = requests.post(
        f"{SMA_URL}/dyn/login.json",
        json={"right": SMA_USER_GROUP, "pass": SMA_PASSWORD},
        verify=SMA_VERIFY_SSL,
        timeout=10,
    )
    resp.raise_for_status()
    sid = resp.json()["result"]["sid"]
    if not sid or sid == "null":
        raise Exception("Failed to login to SMA inverter")
    return sid


def get_values(sid):
    resp = requests.post(
        f"{SMA_URL}/dyn/getAllOnlValues.json?sid={sid}",
        json={"destDev": []},
        verify=SMA_VERIFY_SSL,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["result"]


def extract_values(data):
    device = next(iter(data))
    values = {}
    for key, (name, unit, topic) in SMA_KEYS.items():
        val = data[device].get(key, {}).get("1", [{}])[0].get("val")
        values[key] = val
    return values


def publish_ha_discovery(
    client, sensor, name, unit, device_class, state_class, icon, value_template
):
    topic = f"{HA_DISCOVERY_PREFIX}/sensor/{DEVICE_ID}/{sensor}/config"
    payload = {
        "name": name,
        "state_topic": f"{HA_DISCOVERY_PREFIX}/sensor/{DEVICE_ID}/{sensor}/state",
        "unique_id": f"{DEVICE_ID}_{sensor}",
        "device": DEVICE_INFO,
    }
    if unit:
        payload["unit_of_measurement"] = unit
    if device_class:
        payload["device_class"] = device_class
    if state_class:
        payload["state_class"] = state_class
    if icon:
        payload["icon"] = icon
    if value_template:
        payload["value_template"] = value_template
    client.publish(topic, json.dumps(payload), retain=True)


def publish_to_mqtt(client, values):
    for key, (
        name,
        unit,
        device_class,
        state_class,
        icon,
        value_template,
    ) in SMA_KEYS.items():
        val = values.get(key)
        sensor = key.lower()
        # Publish Home Assistant discovery config
        publish_ha_discovery(
            client,
            sensor,
            name,
            unit,
            device_class,
            state_class,
            icon,
            value_template,
        )
        # Publish state
        state_topic = f"{HA_DISCOVERY_PREFIX}/sensor/{DEVICE_ID}/{sensor}/state"
        if val is not None:
            client.publish(state_topic, val, retain=True)


def main():
    client = mqtt.Client()
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    if MQTT_PORT == 8883:
        client.tls_set()  # Enable SSL/TLS for MQTT
        if os.environ.get("MQTT_TLS_INSECURE", "false").lower() == "true":
            client.tls_insecure_set(True)
    client.connect(MQTT_HOST, MQTT_PORT)
    client.loop_start()
    while True:
        try:
            sid = login()
            data = get_values(sid)
            values = extract_values(data)
            publish_to_mqtt(client, values)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
