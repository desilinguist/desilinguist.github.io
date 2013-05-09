#!/usr/bin/env python

import glob
import re
import sys

# As input, this script just takes the directory
# containing nothing except the files generated
# by running the hadoopified word association
# program. These file were generated as part 
# of my PyCon 2010 talk that can be seen here:
# http://pycon.blip.tv/file/3259632/

# The files themselves can be downloaded 
# from my webpage at:
# http://www.umiacs.umd.edu/~nmadnani/pycon/results.zip
inputdir = sys.argv[1]
answerpat = re.compile(r'(\[(\w+?), (\d+?)\])+')

# Return the 1-best association for a given word
def get_best(line):
    answers = []
    miter = answerpat.finditer(line)
    # Get an extra answer in case we need it
    for i in range(2):
        try:
            ans = miter.next().group(2)
        except StopIteration: 
            return answers
        else:
            answers.append(ans)
    return answers        

# For now we are just printing out the 1-best answer.
# If you want to print out more than one, you will need
# to modify the code below appropriately and the 
# get_best() function above
if __name__ == "__main__":
    for resultfile in glob.glob('%s/part*' % inputdir):
        for line in open(resultfile):
            word, line = line.strip().split('\t')        
            answers = get_best(line)
            if not answers: 
                continue
            elif answers[0] == word:
                if len(answers) > 1:
                    print word, answers[1]
                else:
                    continue
            else:
                print word, answers[0]
            
        