# Standard libraries
import logging

# Third party libraries
from flask import Flask, request

# Our libraries
import copyingModule


log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.basicConfig()

app = Flask(__name__)
app.register_blueprint(copyingModule.bp)

def main():
    app.debug = True
    app.run("0.0.0.0", port = 5010)

if __name__ == "__main__":
    log.info("Starting Copyservice main")
    main()

