#!/usr/bin/env python
# -*- coding: utf-8 *-*
# prj_cfg_mng.py

import os
import re
import general_func
import ConfigParser

prj_main_dir = re.search('(.*bucpp).*', os.getcwd()).group(1) + os.sep + "prj"
prj_main_cfg = prj_main_dir + os.sep + "prj_cfg.cfg"
prj_cfg_dir = prj_main_dir + os.sep + "projects"


class prj_cfg_parse(object):
    ''''''
    def __init__(self):
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(prj_main_cfg)
        self.sections = self.cfg.sections()

    def section_create(self, section):
        try:
            self.cfg.add_section(section)
            self.cfg.write(open(prj_main_cfg, "w"))
            self.sections = self.cfg.sections()
        except ConfigParser.DuplicateSectionError, e:
            print "Section Duplicate. More Info: %s" % e
            return None
    
    def section_list(self):
        return self.sections

    def section_delete(self, section):
        if section in self.sections:
            self.cfg.remove_section(section)
            self.cfg.write(open(prj_main_cfg, "w"))
            self.sections = self.cfg.sections()
        else:
            print "No such section"

    def value_modify(self, section, option, value):
        self.cfg.set(section, option, value)
        self.cfg.write(open(prj_main_cfg, "w"))

    def item_read(self, section):
        try:
            self.cfg.items(section)
            return self.cfg.items(section)
        except ConfigParser.NoSectionError, e:
            print "No This Section. More Info: %s" % e
            return None


class prj_cfg(object):
    ''''''
    def __init__(self):
        general_func.dir_crt(prj_main_dir)
        general_func.file_crt(prj_main_cfg)
        general_func.dir_crt(prj_cfg_dir)

        self.cfg_parse = prj_cfg_parse()

    def prjcfg_create(self, prj_name):
        self.cfg_parse.section_create(prj_name)

    def prjcfg_edit(self, prj_name, items):
        for (option, value) in items:
            self.cfg_parse.value_modify(prj_name, option, value)

    def prjcfg_delete(self, prj_name):
        self.cfg_parse.section_delete(prj_name)

    def prjcfg_read(self, prj_name):
        return self.cfg_parse.item_read(prj_name)

    def prjcfg_list(self):
        for section in self.cfg_parse.section_list():
            print section

if __name__ == "__main__":
    pass

#aaa = prj_cfg()
#print aaa.prjcfg_read("aaa")
#aaa.prjcfg_create("sectionB")
#aaa.prjcfg_edit("sectionB", [("bbb", "adsf"), ("ccc", 123123)])
#aaa.prjcfg_list()

