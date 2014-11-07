# Standard libraries
import logging

# Third party libraries
from flask import Blueprint

# Our libraries
from fesse import routelog

log = logging.getLogger("supertemplate")
bp = Blueprint("blueprint template", __name__)

@bp.route("/blueprinttest")
@routelog
def bptest():
    return "ham"


