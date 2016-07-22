# Expelliarmus

## Purpose
The purpose of this script is to scan pairs of files in a directory to check for a ratio of similarity and any two files that meet the threshold (user defined) will then be printed out as warrenting a look from the human. It also hashes the files and any two files that share a same md5  and sha1 hash will be printed out as matching, they will also likely be printed out for the ratio of similarity.

## Installation
Installing this is simple.  Get the packages needed (For OS)  
Centos: `sudo yum install python-pip antiword`  
Ubuntu: `sudo apt-get install python-pip antiword`  
Mac: `brew install antiword python-pip`  
Then just  pip install the python libraries
`pip install fuzzywuzzy hashlib  docx2txt`
**Note**: if argparse isn't installed by default include it too  
Next just clone this repository and have fun.  
`git clone https://github.com/zcatbear/Expelliarmus.git`

##Running this program
This uses argparse for passing arguments so to invoke it you need to give it a directory to look at.
`./expelliarmus.py --dir  files/ `  
The threshold is the ratio of matching between two files for their names to be printed out. This prevents you from being inundated with data.  
The default threshold is 90. To use something else:  
`./expelliarmus.py --dir files/ --threshold <##>` Where ## are the threshold
##### Note
If for some reason `./` doesn't work you can either use `python expelliarmus.py ...` or just `chmod` the file:  
`chmod 775 expelliarmus.py` (or other appropriate permissions)
  


### Complexity (for those concerned)
Sadly this isn't efficient in the slightest. This has the same complexity as a K complete graph. This is due to each pair of files being run together is similar to an edge. 
Therefore the complexity is O(n^2). In exact terms it is going to be n(n-1)/2. 

##### Optimization
To optimize it (may be coming), maybe append the hash matches to a list. This will cut out [n/2, (n-1)/2, ... , (n-(n+1)/2)] runs because they won't be an edge. 
## Use

