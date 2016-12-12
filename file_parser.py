from os.path import exists
from os.path import isdir
from os.path import dirname
from os.path import basename
from os import listdir
from os import mkdir

class FileParser(object):
    #Static variable of Class FileParser
    AUTO_MATCH_LANGUAGE = "auto_match_language"
    AUTO_MATCH_TIME_ZONE = "auto_match_time_zone"
    CANNOT_TURNOFF_SCREEN = "cannot_turnoff_screen"
    OPT_AND = "and"
    OPT_OR = "or"
    
    #Member names start with '__' means private variable/functions.
    def __init__(self, logPath, keywords_path, issue_type):
        self.__logPath = logPath
        self.__keywords_path = keywords_path
        self.__issue_type = issue_type
    
    def __parse_auto_match_language(self):
        print "handle parse_auto_match_language\n"
        return True
        
    def __parse_auto_match_time_zone():
        print "handle parse_auto_match_time_zone\n"
        return True
        
    def __parse_cannot_turnoff_screen():
        print "handle parse_cannot_turnoff_screen\n"
        return True
        
    #Private and static dictionary. Here it's used for mapping functions by key
    __functions = {AUTO_MATCH_LANGUAGE : __parse_auto_match_language,
                 AUTO_MATCH_TIME_ZONE : __parse_auto_match_time_zone,
                 CANNOT_TURNOFF_SCREEN : __parse_cannot_turnoff_screen}
    def __parse_directory(self, dir_path):
        for fp in listdir(dir_path):
            #print "fp: ", dir_path + fp
            if(isdir(dir_path + "\\" + fp)):
                continue
            else:
                self.__parse_file(dir_path + "\\" + fp)
            
        return
    def __parse_file(self, file_path):
        linenum = 0
        print file_path
        if(exists(dirname(file_path) + "\\result") == False):
            print dirname(file_path) + "\\result"
            mkdir(dirname(file_path) + "\\result")
        if(basename(file_path).find("main") >= 0):
            self.__keys_and = self.__mainkeys_and
            self.__opt = self.__main_opt
            self.__keys_or = self.__mainkeys_or
        if(basename(file_path).find("system") >= 0):
            self.__keys_and = self.__systemkeys_and
            self.__opt = self.__system_opt
            self.__keys_or = self.__systemkeys_or
        if(basename(file_path).find("radio") >= 0):
            self.__keys_and = self.__radiokeys_and
            self.__opt = self.__radio_opt
            self.__keys_or = self.__radiokeys_or
        if(basename(file_path).find("event") >= 0):
            self.__keys_and = self.__eventkeys_and
            self.__opt = self.__event_opt
            self.__keys_or = self.__eventkeys_or
        print "keys: %r %r %r" % (self.__keys_and, self.__opt, self.__keys_or)
        fp_out = open(dirname(file_path) + "\\result\\" + basename(file_path) + "_result", "w")
        for readData in open(file_path, "r"):
            flag = False
            linenum += 1
            #print "linenum: ", linenum, " read line: ", readData
            for keyword_and in self.__keys_and:
                #print "keyword_and: ", keyword_and, "index: ", readData.index(keyword_and)
                if(cmp(keyword_and, "null") == 0):
                    flag = True
                    break
                try:
                    if(readData.index(keyword_and) >= 0):
                        continue
                except ValueError:
                    flag = True
                    break
            #print "opt: ", self.__opt, " cmp: ", cmp(self.__opt, FileParser.OPT_OR)
            if(cmp(self.__opt, FileParser.OPT_AND) == 0):
                if(flag == True):
                    continue
                found = False
                for keyword_or in self.__keys_or:
                    #print "1 keyword_or: ", keyword_or
                    try:
                        if(cmp(keyword_or, "null") == 0):
                            break
                        if(readData.index(keyword_or) >= 0):
                            #print "1 break"
                            found = True
                            flag = False
                    except ValueError:
                        if(found == False):
                            flag = True
                    #print "1 found: ", found
                    if(found == False):
                        flag = True
            elif(cmp(self.__opt, FileParser.OPT_OR) == 0):
                for keyword_or in self.__keys_or:
                    #print "2 keyword_or: ", keyword_or
                    try:
                        if(cmp(keyword_or, "null") == 0):
                            break
                        if(readData.index(keyword_or) >= 0):
                            #print "2 flag: ", flag
                            flag = False
                            break
                    except ValueError:
                        continue
                    flag = True

            if(flag == True):
                continue
            #print "write line: ", "linenum: ", linenum, readData, " flag: ", flag
            fp_out.write(readData)
        fp_out.close()
        return
    def start_parsing(self):
        if(exists(self.__keywords_path) == False or isdir(self.__keywords_path)):
            print "Invalid key words input(%s), exit", self.__keywords_path
            return;
        elif(exists(self.__logPath) == False):
            print "Invalid log path:", self.__logPath
            return False

        #Parse key words and operator
        fp = open(self.__keywords_path, 'r');
        fp.readline()
        self.__mainkeys_and = (fp.readline())[:-1].split(";")
        self.__main_opt = (fp.readline())[:-1]
        self.__mainkeys_or = (fp.readline())[:-1].split(";")
        fp.readline()
        self.__systemkeys_and = (fp.readline())[:-1].split(";")
        self.__system_opt = (fp.readline())[:-1]
        self.__systemkeys_or = (fp.readline())[:-1].split(";")
        fp.readline()
        self.__radiokeys_and = (fp.readline())[:-1].split(";")
        self.__radio_opt = (fp.readline())[:-1]
        self.__radiokeys_or = (fp.readline())[:-1].split(";")
        fp.readline()
        self.__eventkeys_and = (fp.readline())[:-1].split(";")
        self.__event_opt = (fp.readline())[:-1]
        self.__eventkeys_or = (fp.readline())[:-1].split(";")
        fp.close()
        self.__keys_and = self.__mainkeys_and
        self.__opt = self.__main_opt
        self.__keys_or = self.__mainkeys_or
        print "main keys: %r %r %r" % (self.__mainkeys_and, self.__main_opt, self.__mainkeys_or)
        print "system keys: %r %r %r" % (self.__systemkeys_and, self.__system_opt, self.__systemkeys_or)
        print "radio keys: %r %r %r" % (self.__radiokeys_and, self.__radio_opt, self.__radiokeys_or)
        print "event keys: %r %r %r" % (self.__eventkeys_and, self.__event_opt, self.__eventkeys_or)
        
        if(isdir(self.__logPath)):
            self.__parse_directory(self.__logPath)
            print "It's a directory!"
        else:
            print "It's a file!"
            self.__parse_file(self.__logPath)
            #self.__functions.get(self.__issue_type)(self)
