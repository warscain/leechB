#!/usr/bin/env python
# -*- coding: utf-8 *-*
# prj_cfg_mng.py

import os
import re
import general_func
import ConfigParser
import logger

prj_main_dir = re.search('(.*leechB).*', os.getcwd()).group(1) + os.sep + "prj"
prj_main_cfg = prj_main_dir + os.sep + "prj_cfg.cfg"
prj_cfg_dir = prj_main_dir + os.sep + "projects"

class prj_cfg_parse(object):
    def __init__(self):
        # file/dir init
        general_func.dir_crt(prj_main_dir)
        general_func.file_crt(prj_main_cfg)
        general_func.dir_crt(prj_cfg_dir)
        # cfg init
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(prj_main_cfg)
        # main log init
        self.prj_mng_log = logger.main_log()
        self.prj_mng_log.mainlog()

    def section_create(self, section):
        if self.cfg.has_section(section):
            self.prj_mng_log.logger.error("CREATE: " + "project: " + section + " Can't create project: It's already exist")
            return None
        else:
            self.cfg.add_section(section)
            self.cfg.write(open(prj_main_cfg, "w"))
            self.prj_mng_log.logger.info("CREATE: " + "project: " + section)
            return section

    def _value_modify_single(self, section, option, value):
        if value:
            self.cfg.set(section, option, value)
            self.cfg.write(open(prj_main_cfg, "w"))
            self.prj_mng_log.logger.info("MODIFY: " + "project: " + section + " " + option + ": " + value)
            return (option, value)
        else:
            return (option, self.cfg.get(section, option))


    def value_modify(self, section, items):
        if self.cfg.has_section(section):
            result = []
            for (option, value) in items:
                result.append(self._value_modify_single(section, option, value))
            return result
        else:
            self.prj_mng_log.logger.error("MODIFY: " + "project: " + section + " Can't modify project: It's not exist")
            return None

    def section_list(self):
        self.prj_mng_log.logger.info("LIST: " + "project list")
        return self.cfg.sections()

    def section_delete(self, section):
        if self.cfg.has_section(section):
            self.cfg.remove_section(section)
            self.cfg.write(open(prj_main_cfg, "w"))
            self.prj_mng_log.logger.info("DELETE: " + "project: " + section)
            return section
        else:
            self.prj_mng_log.logger.error("DELETE: " + "project: " + section + " Can't delete project: It's not exist")
            return None

    def section_read(self, section):
        if self.cfg.has_section(section):
            result = self.cfg.items(section)
            self.prj_mng_log.logger.info("READ: " + "project: " + section)
            return result
        else:
            self.prj_mng_log.logger.error("READ: " + "project: " + section + " Can't read project: It's not exist")
            return None


class prj_cfg(object):
    def __init__(self):
        self.cfg_parse = prj_cfg_parse()

    def prjcfg_create(self, prj_name):
        return self.cfg_parse.section_create(prj_name)

    def prjcfg_edit(self, prj_name, items):
        return self.cfg_parse.value_modify(prj_name, items)

    def prjcfg_delete(self, prj_name):
        return self.cfg_parse.section_delete(prj_name)

    def prjcfg_read(self, prj_name):
        return self.cfg_parse.section_read(prj_name)

    def prjcfg_list(self):
        return self.cfg_parse.section_list()

if __name__ == "__main__":
    pass

#EXAMPLE
#aaa = prj_cfg()
#
#if aaa.prjcfg_create("fffff"):
#    aaa.prjcfg_edit("fffff", [("prj_src", '10000'), ("prj_dst", '123123')])

#aaa.prjcfg_create("sectionB")
#aaa.prjcfg_create("sectionA")
#print aaa.prjcfg_edit("a", [("prj_dst", 123123)])
#aaa.prjcfg_edit("ffff", [("prj_src", '/home/lucifer/test'), ("prj_dst", '/tmp')])
#aaa.prjcfg_read("dddd")
##aaa.prjcfg_list()
#aaa.prjcfg_delete("sectionA")

