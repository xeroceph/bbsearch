#!/bin/python

"""
xeroceph - https://github.com/xeroceph/bbsearch
GNU General Public License GPL v3.0 - https://www.gnu.org/licenses/gpl-3.0.en.html
"""

import sys
import progressbar
import requests

# open a list from 'domains.txt' locally
file = open('domains.txt', 'r')
items = file.readlines()
domains = [x[:-1] for x in items] # strip newline chars from list

item  = 0
hit = 0
total = len(domains)
success = []
failed = []

def progressBar(value, endvalue, bar_length=20):

        percent = float(value) / endvalue
        arrow = '=' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()

for i in domains :
    item += 1
    progressBar(item, total)
    url = 'https://' + i + '/security.txt'
    try:
        r = requests.get(url)
        if r.status_code == 200:
            hit += 1
            success.append(i)
    except:
        failed.append(i)

percentage = (float(hit) / float(total)) * 100
print '  ', hit, '/', total, ' --- ', format(round(percentage,2)),'%'
print "Domains:", success
print "Request failures:", failed
