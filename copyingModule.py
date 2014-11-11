# Standard libraries
import logging
import thread
import uuid
from subprocess import call
from os import path

# Third party libraries
from flask import Blueprint, render_template
import libvirt
from hest.decorators import routelog, requireformdata
from hest.util import encode


log = logging.getLogger("CopyingModuleTemplate")
bp = Blueprint("CopyingModule", __name__)

#global variables
hypervisor = libvirt.open("qemu:///system")
img_path = "/samba/allaccess/VMimages/"

#functions


def create_new_domain_xml(motherid, newid):
    img = path.join(img_path, newid) + ".img"
    if not path.isfile("templates/" + motherid):
        raise NoOriginalTemplateError("No template with requested id")
    else:
        newxml = render_template(
            motherid,
            name=newid,
            uuid=newid,
            img=img)

        log.info("The xml for the Domain  with id" + newid + " is " + newxml)
        return newxml


def clone_image(original_img_path, newid):
    if path.isfile(original_img_path):
        #TODO: Lav Popen i stedet for ny traad
        thread.start_new_thread(_startcloning, (original_img_path, newid))
    else:
        raise NoOriginalImageError("requested image does not exist")


def _startcloning(original_img_path, newid):
    new_img_path = path.join(img_path, newid) + ".img"
    call(["cp", original_img_path, new_img_path])


# API calls
@bp.route("/copyservice/<motherid>/create", methods=["POST"])
@routelog
@requireformdata(["ORIGINAL_IMG_PATH"])
def startdomain(ORIGINAL_IMG_PATH, motherid):
    newid = str(uuid.uuid1())
    try:
        new_xml = create_new_domain_xml(motherid,  newid)
    except NoOriginalTemplateError:
        return encode(
            {
                "Exception": "No template with requested id",
                "Statuscode": 503
            })

    try:
        clone_image(ORIGINAL_IMG_PATH, newid)
    except NoOriginalImageError:
        return encode(
            {
                "Exception": "requested image does not exist",
                "Statuscode": 503
            })

    return encode({"Xml": new_xml, "Status": 200, "ID": newid})


class NoOriginalImageError(Exception):
    pass


class NoOriginalTemplateError(Exception):
    pass
