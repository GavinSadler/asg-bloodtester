#!/bin/bash

# Prompt for UML student email
read -p "Enter your UML student email: " uml_email

# Prompt for password (hidden input)
read -s -p "Enter your UML password: " uml_password
echo  # Add a newline after password input

# Execute the nmcli command with the provided credentials
nmcli connection add \
connection.id eduroam \
connection.uuid new \
connection.type 802-11-wireless \
802-11-wireless.ssid eduroam \
802-11-wireless-security.key-mgmt wpa-eap \
802-1x.eap peap \
802-1x.phase2-auth mschapv2 \
802-1x.identity "$uml_email" \
802-1x.password "$uml_password"

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Connection 'eduroam' has been successfully added."
else
    echo "Failed to add the 'eduroam' connection. Please check your credentials and try again."
fi