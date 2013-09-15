#!/usr/bin/env python
import fileinput
import sys

def main(auth_file, no_auth_file):
    auth_file.write("SET foreign_key_checks = 0;\n")
    no_auth_file.write("SET foreign_key_checks = 0;\n")
    auth = False
    for line in fileinput.input('data/tmp.sql'):
        if 'Table structure for table' in line:
            auth = False
            if ' `auth_' in line:
                auth = True
        if auth:
            auth_file.write(line)
        if not auth:
            no_auth_file.write(line)

if __name__ == "__main__":
    auth_file = sys.argv[1]
    no_auth_file = sys.argv[2]
    auth_file = open(auth_file,'w')
    no_auth_file = open(no_auth_file,'w')
    main(auth_file, no_auth_file)
    auth_file.close()
    no_auth_file.close()
