# SMA MQTT Bridge

This project periodically fetches data from a local SMA solar inverter API and forwards selected values to Home Assistant using the MQTT convention.

## Features
- Periodic polling of SMA inverter API
- Publishes key values to MQTT topics for Home Assistant
- All configuration via environment variables
- Docker-ready
- GitHub Actions workflow for Docker builds

## Usage
See environment variables in `main.py` for configuration options.
