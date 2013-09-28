#!/usr/bin/env python
import fileinput
import sys

class SplitWriter():
    def __init__(self, file_name):
        self.MAX_LENGTH = 1024 * 1024 * 20 # 20 megabytes
        self.current_length = 0
        self.base_file_name = file_name
        self.current_file_num = 0
        self.current_file = None
        self.new_file()

    def write(self, line):
        self.current_length += len(line)
        if self.current_length > self.MAX_LENGTH:
            self.new_file()
        self.current_file.write(line)

    def new_file(self):
        if self.current_file != None:
            self.current_file.close()
        self.current_file = open(self.base_file_name+'.'+str(self.current_file_num)+'.sql', 'w')
        self.current_file_num += 1
        self.current_length = 0

    def close(self):
        self.current_file.close()


def main(orig_file, auth_file, no_auth_file):
    auth_file = SplitWriter(auth_file)
    no_auth_file = SplitWriter(no_auth_file)
    auth_file.write("SET foreign_key_checks = 0;\n")
    no_auth_file.write("SET foreign_key_checks = 0;\n")
    auth = False
    for line in fileinput.input(orig_file):
        if 'Table structure for table' in line:
            auth = False
            if ' `auth_' in line:
                auth = True
        if auth:
            auth_file.write(line)
        if not auth:
            no_auth_file.write(line)
    auth_file.close()
    no_auth_file.close()

if __name__ == "__main__":
    orig_file = sys.argv[1]
    auth_file = sys.argv[2]
    no_auth_file = sys.argv[3]
    main(orig_file, auth_file, no_auth_file)
