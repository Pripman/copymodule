# Standard libraries
import logging
import thread
import uuid
import socket
from subprocess import call
from os import path

# Third party libraries
from flask import Blueprint, render_template
import libvirt

# Our libraries
from hest.decorators import routelog, requireformdata
from hest.util import encode

log = logging.getLogger("ControllerTemplate")
bp = Blueprint("Controller", __name__)

# classes
class PortAllocator:
    portnrStack = [] 
    
    def getportnumber(self):
        try:
            return self.portnrStack.pop()
        except Indexerror as e:
            raise NoPortsAvailableError("No ports avaliable")

    def releaseport(self, port):
        self.portnrStack.append(port)

class NoPortsAvailableError(Exception):
    pass

# functions
def getIP():
    return "172.25.11.90"
#socket.gethostbyname(socket.gethostname())

def _initializestack():
    availbleports = 16000
    while availbleports > 1024:
        PortAllocator.portnrStack.append(availbleports)
        availbleports = availbleports - 1

def makeinfodict(domain):
    infolist = domain.info() 
    domainid = domain.UUIDString()
    return { "status": infolist[0],  "maxmem": infolist[1], "mem": infolist[2],  " vcpus": infolist[3], "cputime": infolist[4], "id": domainid}

def startDomain(xmlfile, uuid, portallocator):
    port = portallocator.getportnumber()      
    hypervisor.createXML(xmlfile)
    call(["virsh", "qemu-monitor-command", "--hmp", uuid, "hostfwd_add ::" + str(port) + "-:23"])
    return port

def stopDomain(uuid, portallocator, port):
    domain = hypervisor.lookupByUUIDString(uuid)
    xmldesc = domain.XMLDesc()
    domain.shutdown() 
    portallocator.releaseport(port)
    return xmldesc

#global variables
hypervisor = libvirt.open("qemu:///system")
_initializestack()

# API calls
@bp.route("/controller/domains/<domainid>/start", methods = ["POST"])
@routelog
@requireformdata(["XML"])
def startdomain(domainid, XML):
    try:
        port = startDomain(XML, domainid, PortAllocator())
    except NoPortsAvailableError:
        return  encode({"Exception": "no avaliable port", "Status": 503})
    return encode ({"Port": port, "Status": 200, "ID": domainid, "IP": getIP()})  

@bp.route("/controller/domains/<domainid>/stop", methods = ["DELETE"])
@routelog
@requireformdata(["PORT"])
def stopdomain(domainid, PORT):
    XML = stopDomain(domainid, PortAllocator(), PORT)
    return encode ({"Xml": XML, "Status": 200})


@bp.route("/controller/statuslist/")
@routelog
def getStatusList():
    domainlist = hypervisor.listAllDomains()    
    converteddomains = []
    for domain in domainlist:
        converteddomains.append(makeinfodict(domain))
        
    return encode(converteddomains)



