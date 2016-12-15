from file_parser import FileParser
from sys import argv
from os.path import exists
from os.path import isdir
from os.path import dirname
from os.path import basename
from os import listdir
import time

script, path = argv


def dateTimeToMillis(dateTime):
# eg:10-01 18:50:28.346
    millis = dateTime[-3:]
    dateTime = ("2016-" + dateTime)[:-4]
    #print "millis:%r, dateTime:%r" % (millis, dateTime)
    timeArray = time.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    #print "dateTime -> %r" % timeStamp
    timeStamp += int(millis)
    #print "dateTime -> %r" % timeStamp
    return timeStamp


def __parse_directory(dir_path):
    filelist = []
    for fp in listdir(dir_path):
        if(cmp(basename(fp)[0], ".") == 0):
            continue
        filelist.append(dir_path + "/" + fp)
    if(len(filelist) <= 1):
        print "only one file! No need merge!"
        return
    fp_out = open(dir_path + "/merge_result.log", "a")
    print filelist
    for i in range(0, len(filelist) - 1):
        print filelist[i]
        for logline in open(filelist[i], "r"):
            fp_out.write(logline)
    fp_out.close()
    return
def __sort_log(dir_path):
    fp_in = open(dir_path + "/merge_result.log", "r")
    in_logs = fp_in.readlines()
    fp_in.close()
    line_num = len(in_logs)
    for i in range(0, line_num):
        for j in range(0, line_num - i - 1):
            #print "time_1:"+in_logs[j][0:18]+", time_2:"+in_logs[j+1][0:18]
            time_1 = dateTimeToMillis(in_logs[j][0:18])
            time_2 = dateTimeToMillis(in_logs[j+1][0:18])
            #print time_1, time_2
            if(time_1 >= time_2):
                tmp = in_logs[j]
                in_logs[j] = in_logs[j+1]
                in_logs[j+1] = tmp
    fp_out = open(dir_path + "/merge_result.log", "w")
    fp_out.writelines(in_logs)
    fp_out.close();
    
if(isdir(path)):
    __parse_directory(path)
    __sort_log(path)
    #print "01-21 23:22:05.047", dateTimeToMillis("01-21 23:22:05.047")
    #print "01-21 23:21:45.088", dateTimeToMillis("01-21 23:21:45.088")
    #print "10-10 23:40:00.000", dateTimeToMillis("10-10 23:40:00.000")
    #print "It's a directory!"
else:
    print "It's a file! Not need to merge!\n"

