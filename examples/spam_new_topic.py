from os import system, name
import sys, time

sys.path.append("./../")
from jvc_api import JVC

#A simple python script which create topics

client = JVC("", JVC.FORUM_1825)

while True:
    time.sleep(1)
    title = "My topic is impressive."
    message = "Beautiful evening..."
    if client.createTopic(title, message):
        print("Success!")
