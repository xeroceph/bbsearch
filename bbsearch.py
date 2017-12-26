#!/bin/python

"""
xeroceph - https://github.com/xeroceph/bbsearch
GNU General Public License GPL v3.0 - https://www.gnu.org/licenses/gpl-3.0.en.html
"""

import sys
import progressbar
import requests
from threading import Thread, Lock

class bbsearch():
    def __init__(self):
        self.item = 0
        self.hit = 0
        self.success = []
        self.failed = []
        self.list1 = []
        self.list2 = []
        self.loadList()

        # execute via two threads for speed
        t1 = Thread(target=self.execSearch, args=(self.list1,))
        t2 = Thread(target=self.execSearch, args=(self.list2,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

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

        # split into two lists for threading
        for count, i in enumerate(self.domains):
            if count % 2 == 0:
                self.list1.append(i)
            else:
                self.list2.append(i)

    def execSearch(self, domains):
        lock = Lock()
        for i in domains:
            lock.acquire()
            self.item += 1
            lock.release()
            self.progressBar(self.item, self.total)
            url = 'https://' + i + '/security.txt'
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    lock.acquire()
                    self.hit += 1
                    self.success.append(i)
                    lock.release()
            except:
                lock.acquire()
                self.failed.append(i)
                lock.release()

    def summary(self):
        failCount = len(self.failed)
        percentage = (float(self.hit) / float(self.total - failCount)) * 100
        print '  ', self.hit, '/', (self.total - failCount), ' --- ', format(round(percentage,2)),'%'
        try:
            f = open('results.txt', 'w')
            f.writelines('Domains:')
            f.writelines(str(self.success))
            f.writelines('\n')
            f.writelines('Request failures:')
            f.writelines(str(self.failed))
            f.close()
            print 'Final summary saved to results.txt'
        except:
            print 'Error: failed to write results file.'

bbsearch()
