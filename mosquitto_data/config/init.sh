#!/bin/sh

# Check if the password file exists
if [ ! -f /mosquitto/config/pwfile ]; then
    echo "Creating new Mosquitto user..."
    # Create a new password file with the user and password from environment variables
    mosquitto_passwd -b -c /mosquitto/config/pwfile $MQTT_USER $MQTT_PASSWORD
else
    echo "Mosquitto password file already exists."
fi

# Start the Mosquitto broker
exec mosquitto -c /mosquitto/config/mosquitto.conf
