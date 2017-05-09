import random
import sys
import os
import argparse


parser = argparse.ArgumentParser(description='Random KW list generator')
parser.add_argument('-c', action='store', dest='list_length', type=int, default='1000', help='count of words to return')
parser.add_argument('-t', action='store_true', dest='template_it', help='Generate fake template')
args = parser.parse_args()
length = args.list_length
include_template = args.template_it


words = []
basedir = '../data/'
templates = ['{{{document.address.city}}}', '{{{document.name}}}', '{{{document.address.state}}}']

all_files = [fname for fname in os.listdir(basedir) if fname.find('.py') == -1]

for name in all_files:
    with open(basedir + name) as word_source:
        for word in word_source:
            if word.find("'") == -1 and len(word) > 1:
                words.append(word.strip())

if length > len(words):
    """There's a finite list of words available, if we ask for more return all"""
    length = len(words)
random.shuffle(words)
for i in xrange(length):
    if include_template:
        words[i] = '{} {}'.format(words[i], templates[random.randint(0, len(templates)-1)])
    print(words[i])
