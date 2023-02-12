#!/bin/bash

cat club_names.html |
grep -E '<h3 class=\".*?\">.*?<\/h3>' |
grep -E '<span class=\".*?\">.*?<\/span>'




# get list of clubs and clean the strings
# for each club string cleaned curl the data
# regex to get json portion of file
# add "," and move onto next club
