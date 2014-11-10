import requests
import sys
url = "http://localhost:5010/copyingmodule/"
#domid = "30d18a08-d6d8-d5d4-f675-8c42c11d6c62"
domid = "30d18a08-d6d8-d5d4-f675-8c42c11d6c64"


def start(domainid):
    IMG_PATH = "/samba/allaccess/VMimages/" + domid + ".img"
    r = requests.post(url + domainid + "/create", data = {"ORIGINAL_IMG_PATH": IMG_PATH})
    print(r.text)

if __name__ == "__main__": 
    start(domid)

