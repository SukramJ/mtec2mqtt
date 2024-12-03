#!/bin/sh

DIR=$(dirname "$0")
BASE_DIR=$(readlink -f $DIR)

SVC_TXT="
[Unit]
Description=M-TEC MQTT service 
After=multi-user.target

[Service]
Type=simple
User=USER
WorkingDirectory=BASE_DIR
ExecStart=BASE_DIR/python3 mtec2mqtt
Restart=always

[Install]
WantedBy=multi-user.target
"

echo "mtec2mqtt: Installing systemd service to auto-start mtec2mqtt"

if [ $(id -u) != "0" ]; then
  echo "This script required root rights. Please restart using 'sudo'"
else
  echo "$SVC_TXT" | sed "s!BASE_DIR!$BASE_DIR!g" | sed "s/USER/$SUDO_USER/g" > /tmp/mtec2mqtt.service
  chmod 666 /tmp/mtec2mqtt.service
  mv /tmp/mtec2mqtt.service /etc/systemd/system
  systemctl daemon-reload
  systemctl enable mtec2mqtt.service
  systemctl start mtec2mqtt.service
  echo "==> systemd service '/etc/systemd/system/mtec2mqtt.service' installed"
fi

