#!/bin/python

"""
xeroceph - https://github.com/xeroceph/bbsearch
GNU General Public License GPL v3.0 - https://www.gnu.org/licenses/gpl-3.0.en.html
"""

import sys
import progressbar
import requests

class bbsearch():
    def __init__(self):
        self.item = 0
        self.hit = 0
        self.success = []
        self.failed = []
        self.loadList()
        self.execSearch()
        self.summary()

    def progressBar(self, value, endvalue, bar_length=20):
        percent = float(value) / endvalue
        arrow = '=' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))
        sys.stdout.write("\rExecuting search: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()

    def loadList(self):
        # open a list from 'domains.txt' locally
        file = open('domains.txt', 'r')
        items = file.readlines()
        self.domains = [x[:-1] for x in items] # strip newline chars from list
        self.total = len(self.domains)
        
    def execSearch(self):
        for i in self.domains:
            self.item += 1
            self.progressBar(self.item, self.total)
            url = 'https://' + i + '/security.txt'
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    self.hit += 1
                    self.success.append(i)
            except:
                self.failed.append(i)

    def summary(self):
        failCount = len(self.failed)
        percentage = (float(self.hit) / float(self.total - failCount)) * 100
        print '  ', self.hit, '/', (self.total - failCount), ' --- ', format(round(percentage,2)),'%'
        print "Domains:", self.success
        print "Request failures:", self.failed

bbsearch()
