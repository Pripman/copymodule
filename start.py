#!/bin/python
# coding: utf-8
# Standard libraries
import logging

# Third party libraries

# My libraries
from hest.util import debug

log = logging.getLogger()

if debug():
    logging.basicConfig()
    log.setLevel(logging.DEBUG)
else:
    logging.basicConfig(filename="mylogs.txt")
    log.setLevel(logging.INFO)


from subprocess import call

log.info("Running doit")
call(["doit"])


def main():
    import main
    main.main()


if __name__ == "__main__":
    log.info("Starting main")
    main()
