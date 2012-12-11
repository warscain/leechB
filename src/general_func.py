#!/usr/bin/env python
# -*- coding: utf-8 *-*
# general_func.py
import os
import re

#判断少了。

def dir_crt(anypath):
    try:
        if not os.path.exists(anypath):
            os.makedirs(anypath, mode=0755)
            return "created"
        else:
            return "exist"
    except (OSError, IOError):
        return "permissiondeny"


def file_crt(anyfile):
    try:
        if not os.path.exists(anyfile):
            file_create = open(anyfile, "w")
            file_create.close
            return "created"
        else:
            return "exist"
    except (OSError, IOError):
        return "permissiondeny"


def user_quit(anyinput): 
    quit_cmp = re.compile("^quit$", re.I)
    if re.search(quit_cmp, str(anyinput)):
            return "quit"