#!/bin/python
# coding: utf-8
# Standard libraries


def task_aptinstaller():
    return {
        'actions': ["bash aptinstalls"],
        'file_dep': ["aptinstalls"],
        'verbosity': 2
    }
