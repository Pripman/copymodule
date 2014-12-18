#!/bin/python
# coding: utf-8
# Standard libraries


def task_installs():
    return {
        'actions': ["bash installs"],
        'file_dep': ["aptinstalls"],
        'verbosity': 2
    }

 def task_rundebug():
    return {
        "actions": ["python main.py", ],
        "verbosity": 2
    }
