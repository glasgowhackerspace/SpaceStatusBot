# Space Stauts Bot
# J Beeley Oct 2025
# Connect switch between GPIO4 and GND. Switch closed indicates space is open
# Connect SSD1306 OLED to I2C port 1 SCL/SCA, 3V3 and GND

# config.json format:
#  {
#     "glashack channel": 1234,
#     "glashack token": "TOKEN"
#  }

import discord, json
from discord.ext import tasks
from gpiozero import Button
from time import sleep
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from time import sleep
import os

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

ip_str = os.popen("ifconfig").read().split(" ")
# print(ip_str)

for c in range(0, len(ip_str)): 
    # print(c, ip_str[c])
    if "wlan0" in ip_str[c]:
        ip_addr=ip_str[c+13]
        print(ip_addr)
... 

with canvas(device) as draw:
    draw.text((20, 20), ip_addr, fill="white")

try:
    with open("config.json", mode="r", encoding="utf-8") as config_file:
        config_json = json.load(config_file)
except IOError:
    print("Unable to open config.json")
    with canvas(device) as draw:
        draw.text((20, 40), "Cant open config", fill="white")
    exit()


button=Button(4)
count=0

class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        global status        
        super().__init__(*args, **kwargs)
        status=""
        # an attribute we can access from our task
        self.counter = 0

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=1)  # task runs every 1 second
    async def my_background_task(self):
        global status
        channel = self.get_channel(config_json["glashack channel"])  # channel ID goes here
        if button.is_pressed: #Pin low - space open
            if status=="" or status=="closed":
                status="open"
                print("Switch: Space open")
                with canvas(device) as draw:
                    draw.text((20, 20), ip_addr, fill="white")
                    draw.text((20, 40), "Open", fill="white")
                await channel.send("Space open")
        else:    #Pin high - space closed
            if status=="" or status=="open":
                status="closed"
                print("Switch: Space closed")
                with canvas(device) as draw:
                    draw.text((20, 20), ip_addr, fill="white")
                    draw.text((20, 40), "Closed", fill="white")                   
                await channel.send("Space closed")

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


status=""
client = MyClient(intents=discord.Intents.default())


@client.event
async def on_message(message):
    global status    
    if message.author == client.user:
        return
    if status=="open":
        print("Discord mention: Space open")
        with canvas(device) as draw:
            draw.text((20, 20), ip_addr, fill="white")
            draw.text((20, 40), "Open", fill="white")        
        await message.channel.send("Space open")
    elif status=="closed":
        print("Discord mention: Space closed")
        with canvas(device) as draw:
            draw.text((20, 20), ip_addr, fill="white")
            draw.text((20, 40), "Closed", fill="white")           
        await message.channel.send("Space closed")


client.run(config_json["glashack token"])






