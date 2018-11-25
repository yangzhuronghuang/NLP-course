import re
import codecs
import sys

r1 = re.compile(r'^<')

def pre(input_file):
    outfile = codecs.open(input_file + '_pre', 'w', 'utf-8')
    with codecs.open(input_file, 'r', 'utf-8') as myfile:
        for line in myfile:
            if re.match(r1, line):
                pass
            else:
                outfile.write(line)
    outfile.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit()

    pre(sys.argv[1])
