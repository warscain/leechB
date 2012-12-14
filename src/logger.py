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

class main_log(object):
    def __init__(self):
        general_func.dir_crt(log_main_dir)
        general_func.dir_crt(log_prj_dir)
        general_func.file_crt(log_main_file)
        self.logger = logging.getLogger("leechB")
        self.filehd = logging.FileHandler(log_main_file, "a+")
        self.streamhd = logging.StreamHandler()
        self.logger.setLevel("DEBUG")     # 全局logger的level要低，下面不同handler才有效，否则以全局为主。

    def __del__(self):
        self.logger.handlers = []

    def mainlog(self):
        fmt = {"filehd_fmt":
               '[%(asctime)s] %(process)d %(levelname)-8s \
                (%(module)s:%(lineno)d) %(message)s',

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

class prj_log(main_log):
    def __init__(self, prj_name):
        super(prj_log, self).__init__()
        log_prj_file = log_prj_dir + os.sep + prj_name
        general_func.file_crt(log_prj_file)
        self.filehd = logging.FileHandler(log_prj_file, "a+")

if __name__ == "__main__":
    pass


#aaa = main_log()
#aaa.mainlog()
#
#aaa.logger.error("adsfaf")
#aaa.__del__()
#aaa.mainlog()
#
#aaa.logger.error("adsasaaaaaaa")
#
#
#bbb = prj_log("aaa")
#bbb.mainlog()
#bbb.logger.error(1)
#
#aaa.logger.error("adsasaaaaaaa")

