from file_parser import FileParser
from sys import argv
script, path, keywords = argv
parser = FileParser(path, keywords, FileParser.AUTO_MATCH_LANGUAGE)
parser.start_parsing()
