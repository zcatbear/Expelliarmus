#!/usr/bin/env python


from fuzzywuzzy import fuzz
from subprocess import Popen, PIPE
import docx2txt as doc
from os import listdir
from os.path import isfile, join
import hashlib
import argparse
from collections import defaultdict
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def convert_pdf_to_txt(path, password=""):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'ascii'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str
def removeNonAscii(string):
    #Removes all characters that aren't ascii compatible. Sorry if you don't speak American
    return "".join(i for i in string if ord(i)<128)
def documentToText(path):
    if path[-4:] == ".doc":
        cmd = ['antiword', path]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return removeNonAscii(stdout)
    elif path[-5:] == ".docx":
        return removeNonAscii(doc.process(path))
    elif path[-4:] == ".txt":
        inputFile = open(path)
        text = inputFile.read() #Because memory and such
        inputFile.close()
        return(removeNonAscii(text))
    elif path[-4:] == ".pdf":
        return removeNonAscii(convert_pdf_to_txt(path))
    return ""
def getHashes(path):
    with open(path,  'rb') as afile:
        md5 = hashlib.md5(afile.read()).hexdigest()
        #I'd like to just read through the file once too but apparenlty it doesn't work that way. You have to read through twice
    with open(path, 'rb') as bfile:
        sha1 = hashlib.sha1(bfile.read()).hexdigest()
    return (md5, sha1)

parser = argparse.ArgumentParser(description="This script compares every pair of files in a given directory against each other to get a ratio of similarity to help give an idea of whether they were cheating or not")
parser.add_argument('-d', '--dir', help='Directory that is the root directory for each of the files', required=True)
parser.add_argument('-t', '--threshold', help='This is the user defined threshold. Any ratios >= this threshold are printed', default=90)
args = parser.parse_args()


files = [ f for f in listdir(args.dir) if isfile(join(args.dir,f))]

hashes = defaultdict(list)
scanned = list()
ratios = list()
count = 0
for i in files:
    path = args.dir + i
    hashes[getHashes(path)].append(i)
    for j in scanned:
        ratios.append((i,j.split("/")[-1],fuzz.ratio(documentToText(path), documentToText(j))))
        count +=1
    scanned.append(path)
print("Files worth looking at:")

for ratio in ratios:
    if ratio[2] > args.threshold:
        print("\t" + str(ratio))


print("Hash matches:")
for key  in hashes:
    if len(hashes[key]) > 1:
        print(hashes[key])
print("Count: " + str(count))

