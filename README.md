# Expelliarmus

## Purpose
The purpose of this script is to scan pairs of files in a directory to check for a ratio of similarity and any two files that meet the threshold (user defined) will then be printed out as warrenting a look from the human. It also hashes the files and any two files that share a same md5  and sha1 hash will be printed out as matching, they will also likely be printed out for the ratio of similarity.

## Complexity
This always runs 2n times (where n is the number of files in the directory) because it is similar to a complete graph in graph theory where every node is equally connected to all other nodes. 

