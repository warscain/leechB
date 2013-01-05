#!/usr/bin/env python
# -*- coding: utf-8 *-*
# backup.py

import os
import logger
import re

class backup(object):
    def __init__(self, prj_name, items):
        self.snap_ctllog_instance = logger.snap_ctl_log(prj_name)
        self.snap_ctllog_instance.mainlog()
        
        self.prj_name = prj_name
        self.prj_src = items[0][1]
        self.prj_dst = items[1][1]
        self.work_dir = os.getcwd()

        self.src_father_df = os.sep
        for mid_dir in self.prj_src.split("/")[1:-1]:
            self.src_father_df += mid_dir + os.sep

    def __prj_snap_base_read(self):
        log_fh = open(logger.prj_cfg_dir + os.sep + self.prj_name)
        try:
            snap_base = int([x for x in log_fh][-1].strip().split()[-1])
        except IndexError: #文件为空，则做第一次备份，base为-1 这样每次snap都是+1,则next是0
            snap_base = -1
        log_fh.close()
        return snap_base

    def snap_create(self, msg):
        #一个base一个next next是base+1.base=0 所以，__prj_snap_base_read迭代失败为-1则next=0
        snap_base = self.__prj_snap_base_read()
        snap_next = snap_base + 1
        #时间戳记文件和备份文件名
        dst_stamp = self.prj_dst + os.sep + self.prj_name
        dst_filename = self.prj_dst + os.sep + self.prj_name + "_" + str(snap_next) + ".tar.gz"
        #chdir的目的在于备份的文件只有单层文件夹
        os.chdir(self.src_father_df)
        self.src_df = str(self.prj_src.split("/")[-1])

        os.system("tar -g" + " " + dst_stamp + " " + "-zcf" + dst_filename + " " + self.src_df)
        self.snap_ctllog_instance.logger.info(msg + " " + str(snap_next))

        os.chdir(self.work_dir)

    def snap_delete(self, snap_num):
        snap_base = self.__prj_snap_base_read()

        if snap_base == -1: # 没有备份过，pass
            pass

        if snap_num <= snap_base: #基本条件 如果没有这个snap则不运行

            log_fh = open(logger.prj_cfg_dir + os.sep + self.prj_name, "r") #这里已经下面的for循环为找到给出的snap的行数
            self.line_num = 0
            for x in log_fh: #循环一次行数 + 1, 之后读取全部行数
                aaa = re.search(" " + str(snap_num) + os.linesep, x)
                self.line_num += 1
                try:
                    aaa.group(0)
#                    log_fh.close()
#                    return self.line_num  #若单独把循环找到line_num写成函数的话可以用这两行 否则用后面的else
                except AttributeError:
                        pass
                else:
                    log_fh.close()
                    break   # 匹配之后文件句柄已经关闭，所以循环也退出
            #根据上面的log行数 读取snap的log确认需要删除的列表
            log_fh = open(logger.prj_cfg_dir + os.sep + self.prj_name, "r")
            all_file_list = [line for line in log_fh]
            delete_list = all_file_list[self.line_num - 1:]
            for del_item in delete_list:
                all_file_list.remove(del_item)
            log_fh.close()

            #覆盖上面已经确定的列表，写入文件
            log_fh = open(logger.prj_cfg_dir + os.sep + self.prj_name, "w")
            for good_line in all_file_list:
                log_fh.write(good_line)
            log_fh.close()

            #开始删除备份文件和备份时间戳记
            for i in range(snap_num, snap_base + 1):
                try:
                    os.remove(self.prj_dst + os.sep + self.prj_name + "_" + str(i) + ".tar.gz")
                except OSError:
                    pass
            #下面两种情况，一种，snap全清除，另一种则不是。因为tar的time stamp文件不支持回滚，
            #因此，当做snap删除的时候需要吧timestamp清空，则下一次create snap是一个全备
            #下一版本备份替换timestamp，使用python自带tarfile以及自己写的timestamp。
            #后续可能写一个daemon来监控src文件变更
            if snap_num == 0: # 附加条件。当要删除base snap的时候 删除time stamp彻底清空
                os.remove(self.prj_dst + os.sep + self.prj_name)
            else:
                dst_stamp = open(self.prj_dst + os.sep + self.prj_name, "w")
                dst_stamp.close()

    def snap_rebase(self):
        '''删除所有备份文件，并做一次全备份'''
        self.snap_delete(snap_num=0) # 清除所有备份文件，时间戳记以及备份日志
        self.snap_create(msg="rebase") # 创建备份文件0.

    def __df_del(self, df_name):
        '''递归删除文件夹。df_name及其下属文件，文件夹删除。
        注意这里只定义了两种文件，其余例如link不会被删除'''
        if os.path.isfile(df_name):
            os.remove(df_name)
        elif os.path.isdir(df_name):
            for item in os.listdir(df_name):
                df_name_item = os.path.join(df_name, item)
                self.__df_del(df_name_item)
                try:
                    os.rmdir(df_name)
                except:
                    pass

    def snap_revert(self, snap_num):
        self.__df_del(self.prj_src) # 删除源文件
        for num in range(0,snap_num+1): # 批量解压到源文件来还原
            os.system("tar -zxvf " + 
                      self.prj_dst + 
                      os.sep + 
                      self.prj_name + 
                      "_" + 
                      str(num) + 
                      ".tar.gz" + 
                      " -C " + 
                      self.src_father_df)

    def snap_list(self):
        log_read_hd = open(logger.prj_cfg_dir + os.sep + self.prj_name, 'r')
        print "==========snapshot list=========="
        print "PrjName: %s" % self.prj_name
        line_cmp = re.compile('^(\[.*\]).*\)\s(.*)\s([0-9]+)$')
        for line in log_read_hd:
            temp = line.rstrip()
            result = re.search(line_cmp, temp)
            print "SnapNum: %s\tSnapTime: %s\tSummary: %s" % (result.group(3), result.group(1), result.group(2))
        
    def snap_revert_to(self, snap_num, dst_lct):
        for num in range(0,snap_num+1): # 批量解压到源文件来还原
            os.system("tar -zxvf " + 
                      self.prj_dst + 
                      os.sep + 
                      self.prj_name + 
                      "_" + 
                      str(num) + 
                      ".tar.gz" + 
                      " -C " + 
                      dst_lct)

    def test(self, df_name):
        '''递归删除文件夹。df_name及其下属文件，文件夹删除。
        注意这里只定义了两种文件，其余例如link不会被删除'''
        if os.path.isfile(df_name):
            os.remove(df_name)
        elif os.path.isdir(df_name):
            for item in os.listdir(df_name):
                df_name_item = os.path.join(df_name, item)
                self.__df_del(df_name_item)
                try:
                    os.rmdir(df_name)
                except:
                    pass

#aaa = backup("aaa", [("prj_src", "/home/lucifer/test"), ("prj_dst", "/tmp")])
#aaa.test("/home/lucifer/test")
#aaa.snap_revert(0)
#print aaa.prj_name
#print aaa.prj_src
#print aaa.prj_dst
#aaa.snap_create("less tha as as asd")
#aaa.snap_delete(0)
#aaa.snap_rebase()
#aaa.test(5)
#print aaa.work_dir
#print aaa.test()
#aaa.snap_list()


