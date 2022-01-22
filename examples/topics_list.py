from columnar import columnar
from os import system, name
import sys, time

sys.path.append("./../")
from jvc_api import JVC

def clearOutput():
    if name == "nt":
        system("cls")
    else:
        system("clear")

#A simple python script which prints the topics of the first page

client = JVC("", JVC.FORUM_1825)

headers = ["Number", "Title", "Author"]

while True:
    topics = client.getTopics(1)
    data = []
    i = 0
    for topic in topics:
        data.append([str(i), topic.title, topic.author])
        i += 1
    print(columnar(data, headers, no_borders=True))
    time.sleep(5)
    clearOutput()
