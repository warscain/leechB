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
    ''''''
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
            self.prj_mng_log.logger.error("Can't CREATE " + section + ":It's already exist")
            print "Section exist"
            return None
        else:
            self.cfg.add_section(section)
            self.cfg.write(open(prj_main_cfg, "w"))
            self.prj_mng_log.logger.info("CREATE: " + section)
            print "Project %s is Created" % section
            return True

    def _value_modify_single(self, section, option, value):
        if option in ("prj_src", "prj_dst"):
            self.cfg.set(section, option, value)
            self.cfg.write(open(prj_main_cfg, "w"))
            self.prj_mng_log.logger.info("MODIFY: " + section + " " + option)
            print "%s: %s" % (option, value)
        else:
            self.prj_mng_log.logger.error("MODIFY: " + section + " " + option + " " + "is not legal")

    def value_modify(self, section, items):
        if self.cfg.has_section(section):
            for (option, value) in items:
                self._value_modify_single(section, option, value)
        else:
            self.prj_mng_log.logger.error("MODIFY: " + section + " " + "is not exist")
            print "No such section: %s" % section

    def section_list(self):
        self.sections = self.cfg.sections()
        print "==========projects list=========="
        for prj in self.sections:
            print prj

    def section_delete(self, section):
        if self.cfg.has_section(section):
            self.cfg.remove_section(section)
            self.cfg.write(open(prj_main_cfg, "w"))
            self.prj_mng_log.logger.info("DELETE: " + section)
            print "Project %s is Deleted" % section
        else:
            print "No such section"

    def section_read(self, section):
        if self.cfg.has_section(section):
            result = self.cfg.items(section)
            self.prj_mng_log.logger.info("READ: " + section)
            print "%s: %s" % (result[0][0], result[0][1])
            print "%s: %s" % (result[1][0], result[1][1])
        else:
            self.prj_mng_log.logger.error("READ: " + section + " " +  "is not exist")
            print "No such section"
            return None


class prj_cfg(object):
    def __init__(self):
        self.cfg_parse = prj_cfg_parse()

    def prjcfg_create(self, prj_name):
        if self.cfg_parse.section_create(prj_name):
            return True

    def prjcfg_edit(self, prj_name, items):
        self.cfg_parse.value_modify(prj_name, items)

    def prjcfg_delete(self, prj_name):
        self.cfg_parse.section_delete(prj_name)

    def prjcfg_read(self, prj_name):
        return self.cfg_parse.section_read(prj_name)

    def prjcfg_list(self):
        self.cfg_parse.section_list()

if __name__ == "__main__":
    pass

#EXAMPLE
#aaa = prj_cfg()
#print aaa.prjcfg_create("noexffffifst")
#aaa.prjcfg_create("sectionB")
#aaa.prjcfg_create("sectionA")
#aaa.prjcfg_edit("sectionB", [("prj_dst", 123123)])
#aaa.prjcfg_edit("dfff", [("prj_src", 10000), ("prj_dst", 123123)])
#aaa.prjcfg_read("dddd")
##aaa.prjcfg_list()
#aaa.prjcfg_delete("sectionA")

