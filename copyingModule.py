# Standard libraries
import logging
import thread
import uuid
from subprocess import call
from os import path

# Third party libraries
from flask import Blueprint, render_template_string
import libvirt
from hest.decorators import routelog, requireformdata
from hest.util import encode


log = logging.getLogger("CopyingModuleTemplate")
bp = Blueprint("CopyingModule", __name__)

#global variables
hypervisor = libvirt.open("qemu:///system")
img_path = "/samba/allaccess/VMimages/"

#functions


def create_new_domain_xml(template, motherid, newid):
    img = path.join(img_path, newid) + ".img"
    try:
        newxml = render_template_string(
            template,
            name=newid,
            uuid=newid,
            img=img)
    except:
        raise FailedToLoadTemplateError("There was an error loading template")
        log.info("copyingModule.create_new_domain_xml: created :\n " + newxml)
    return newxml


def clone_image(original_img_path, newid):
    new_path = path.join(img_path, newid) + ".img"
    if path.isfile(original_img_path):
        #TODO: Lav Popen i stedet for ny traad
        thread.start_new_thread(_startcloning, (original_img_path, new_path))
    else:
        raise NoOriginalImageError("requested image does not exist")
    return new_path


def _startcloning(original_img_path, new_img_path):
    call(["cp", original_img_path, new_img_path])


# API calls
@bp.route("/copyservice/<motherid>/create", methods=["POST"])
@routelog
@requireformdata(["ORIGINAL_IMG_PATH"])
@requireformdata(["TEMPLATE"])
def startdomain(ORIGINAL_IMG_PATH, motherid, TEMPLATE):
    newid = str(uuid.uuid1())
    try:
        new_xml = create_new_domain_xml(TEMPLATE, motherid,  newid)
    except FailedToLoadTemplateError:
        return encode(
            {
                "Exception": "No template with requested id",
                "Status": 503
            })

    try:
        new_img_path = clone_image(ORIGINAL_IMG_PATH, newid)
    except NoOriginalImageError:
        return encode(
            {
                "Exception": "requested image does not exist",
                "Status": 503
            })

    return encode({
        "Xml": new_xml,
        "newpath": new_img_path,
        "Status": 200,
        "ID": newid})


class NoOriginalImageError(Exception):
    pass


class FailedToLoadTemplateError(Exception):
    pass
