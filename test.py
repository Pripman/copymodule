import requests
url = "http://localhost:5010/copyservice/"
#domid = "30d18a08-d6d8-d5d4-f675-8c42c11d6c62"
domid = "nytimg"


def start(domainid):
    IMG_PATH = "/samba/allaccess/VMimages/" + domid + ".img"
    r = requests.post(url + domainid + "/create", data={
        "ORIGINAL_IMG_PATH": IMG_PATH})
    print(r.text)


def createshare(xml, domainid):
    IMG_PATH = "/samba/allaccess/VMimages/" + domid + ".img"
    r = requests.post(url + domainid + "/createsharedomain", data={
        "ORIGINAL_IMG_PATH": IMG_PATH,
        "XML": xml})
    print(r.text)

if __name__ == "__main__":
    #start(domid)
    with open("/samba/allaccess/ConfigFiles/workingconfig_usernetwork.xml", 'r') as xml:
        data = xml.read().replace('\n', '')
        createshare(data, domid)
            
