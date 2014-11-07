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

log = logging.getLogger("CopyingModuleTemplate")
bp = Blueprint("CopyingModule", __name__)

#global variables
hypervisor = libvirt.open("qemu:///system")
img_path = "/samba/allaccess/VMimages/"

#functions

def create_new_domain_xml(motherid, newid): 
    img = img_path + newid + ".img"
    newxml = render_template(motherid, 
                                name = newid,
                                uuid = newid,
                                img = img)

    log.info("The xml for the Domain  with id" + newid+ " is " + newxml)
    return newxml  

def clone_image(original_img_path, newid):
    imgexists = path.isfile(original_img_path)  
    if(imgexists):
        thread.start_new_thread(_startcloning, (original_img_path, newid)) 
   
def _startcloning(original_img_path, newid):
    new_img_path = img_path + newid + ".img"
    call(["cp", original_img_path, new_img_path])



# API calls
@bp.route("/copyingmodule/<motherid>/create", methods = ["POST"])
@routelog
@requireformdata(["IMG_PATH"])
def startdomain(IMG_PATH, motherid):
    newid = str(uuid.uuid1())
    new_xml = create_new_domain_xml(motherid,  newid)
    clone_image(IMG_PATH, newid) 

    return encode ({"Xml": new_xml, "Status": 200, "ID": newid})

    
