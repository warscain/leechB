#!/usr/bin/env python
# -*- coding: utf-8 *-*
# logger.py

import os
import re
import general_func
import logging

log_main_dir = re.search('(.*leechB).*', os.getcwd()).group(1) + os.sep + "log"
log_main_file = log_main_dir + os.sep + "leechB.log"
log_prj_dir = log_main_dir + os.sep + "prjlogs"

prj_main_dir = re.search('(.*leechB).*', os.getcwd()).group(1) + os.sep + "prj"
prj_cfg_dir = prj_main_dir + os.sep + "projects"


class main_log(object):
    def __init__(self):
        general_func.dir_crt(log_main_dir)
        general_func.dir_crt(log_prj_dir)
        general_func.file_crt(log_main_file)
        self.logger = logging.getLogger("leechB")
        self.filehd = logging.FileHandler(log_main_file, "a+")
        self.streamhd = logging.StreamHandler()
        self.logger.setLevel("DEBUG")     # 全局logger的level要低，下面不同handler才有效，否则以全局为主。

    def mainlog(self):
        fmt = {"filehd_fmt":
               '[%(asctime)s] %(process)d %(levelname)-8s (%(module)s:%(lineno)d) %(message)s',

                "streamhd_fmt":
                '%(asctime)s|%(levelname)-6s|%(message)s'}

        datefmt = '%H:%M:%S'

        file_fmt = logging.Formatter(fmt["filehd_fmt"], datefmt)
        self.filehd.setFormatter(file_fmt)
        self.logger.addHandler(self.filehd)
        self.filehd.setLevel("DEBUG")

        stream_fmt = logging.Formatter(fmt["streamhd_fmt"], datefmt)
        self.streamhd.setFormatter(stream_fmt)
        self.logger.addHandler(self.streamhd)
        self.streamhd.setLevel("ERROR")


class snap_ctl_log(object):
    def __init__(self, prj_name):
        general_func.dir_crt(log_main_dir)
        general_func.dir_crt(log_prj_dir)
        general_func.file_crt(log_main_file)

        self.logger = logging.getLogger("snap_ctl_log") 

        prj_snap_file = prj_cfg_dir + os.sep + prj_name
        general_func.file_crt(prj_snap_file)
        self.filehd = logging.FileHandler(prj_snap_file, "a+")

        self.streamhd = logging.StreamHandler()
        self.logger.setLevel("DEBUG")     # 全局logger的level要低，下面不同handler才有效，否则以全局为主。

    def mainlog(self):
        fmt = {"filehd_fmt":
               '[%(asctime)s] %(process)d (%(module)s:%(lineno)d) %(message)s',

                "streamhd_fmt":
                '%(asctime)s|%(levelname)-6s|%(message)s'}

        datefmt = '%Y/%m/%d %H:%M:%S'

        file_fmt = logging.Formatter(fmt["filehd_fmt"], datefmt)
        self.filehd.setFormatter(file_fmt)
        self.logger.addHandler(self.filehd)
        self.filehd.setLevel("DEBUG")

        stream_fmt = logging.Formatter(fmt["streamhd_fmt"], datefmt)
        self.streamhd.setFormatter(stream_fmt)
        self.logger.addHandler(self.streamhd)
        self.streamhd.setLevel("ERROR")

if __name__ == "__main__":
    pass


#aaa = main_log()
#aaa.mainlog()
#
#aaa.logger.error("adsfaf")
#aaa.__del__()
#aaa.mainlog()

#aaa = main_log()
#aaa.mainlog()
#aaa.logger.info("aaaaa")
#
#bbb = prj_log("bbbbb")
#bbb.mainlog()
#bbb.logger.info("bbbbbb")
##
##
#ccc = snap_ctl_log("ccccc")
#ccc.mainlog()
#ccc.logger.info("cccccc")





