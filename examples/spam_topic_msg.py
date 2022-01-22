from os import system, name
import sys, time
import random

sys.path.append("./../")
from jvc_api import JVC

#A simple python script which send a message on a random topic from the first page

client = JVC("", JVC.FORUM_1825)

while True:
    time.sleep(1)
    topic = client.getTopics(1)[random.randint(1, 24)]
    message = "Beautiful evening..."
    if topic.sendMessage(message):
        print(topic.base_url + topic.url)
