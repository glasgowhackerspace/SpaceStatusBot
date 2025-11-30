# Hackspace Status Bot

Indicates hackspace open/closed state to Discord channel.

Connect switch between GPIO4 and GND. Switch closed indicates space is open.

Connect SSD1306 OLED to I2C port 1 SCL/SCA, 3V3 and GND to show status and IP address.

Set up the config.json file in the same directory as spacebot.py as follows, where 1234 is the channel number and TOKEN is the token obtained from the Discord developer portal when configuring the bot:

 {
    "glashack channel": 1234,
    "glashack token": "TOKEN"
 }


Copy the python-script.service file to /etc/systemd/system/ and configure as described in:

 https://linuxconfig.org/how-to-autostart-python-script-on-raspberry-pi

 to run the script on startup