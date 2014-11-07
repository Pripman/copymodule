import requests
import sys
url = "http/localhost:5009/controller/domains/"
copyurl = "http:5009/copyingmodule/"
cmd = sys.argv[0]
port = sys.argv[1]
domid = "30d18a08-d6d8-d5d4-f675-8c42c11d6c62"


def copy(domainid):
    with open("/samba/allaccess/ConfigFiles/workingconfig_usernetwork.xml") as f:
        xml = f.read()
    r = requests.post(url + domainid + "/start", data = {"XML": xml})
    print(r.text)

if cmd == "start":
    start(domid)

