#!/usr/bin/env python

__authors__ = 'Yoann Sculo <yoann.sculo@gmail.com>'
__copyright__ = 'Copyright (C) 2013 Yoann Sculo'
__license__ = '????'
__version__ = '0.1'

import os
import sys
import sqlite3 as lite
import datetime
from optparse import OptionParser

reload(sys)
sys.setdefaultencoding("utf-8")

class Offer():
    def __init__(self, src, ref, date_pub, date_add, title, company, contract, location, salary, url, content):
        self.src = src
        self.ref = ref
        self.date_pub = datetime.datetime.fromtimestamp(int(date_pub))
        self.date_add = datetime.datetime.fromtimestamp(int(date_add))
        self.title = title.encode("utf-8")
        self.company = company.encode("utf-8")
        self.contract = contract.encode("utf-8")
        self.location = location.encode("utf-8")
        self.salary = salary.encode("utf-8")
        self.url = url.encode("utf-8")
        self.content = content.encode("utf-8")

    #def set_from_row(row):
    #    self.src = row[0]
    #    self.ref = row[1]
    #    self.date_pub = datetime.datetime.fromtimestamp(int(row[2]))
    #    self.date_add = datetime.datetime.fromtimestamp(int(row[3]))
    #    self.title = row[4].encode("utf-8")
    #    self.company = row[5].encode("utf-8")
    #    self.contract = row[6].encode("utf-8")
    #    self.location = row[7].encode("utf-8")
    #    self.salary = row[8].encode("utf-8")
    #    self.url = row[9].encode("utf-8")
    #    self.content = row[10].encode("utf-8")

def db_create():
    conn = None
    conn = lite.connect("jobs.db")
    cursor = conn.cursor()

    # create a table
    cursor.execute("""CREATE TABLE offers( \
                        source TEXT, \
                        ref TEXT, \
                        date_pub INTEGER, \
                        date_add INTEGER, \
                        title TEXT, \
                        company TEXT, \
                        contract TEXT, \
                        location TEXT, \
                        salary TEXT, \
                        url TEXT, \
                        content TEXT, \
                        PRIMARY KEY(source, ref))""")
    # cursor.execute("""CREATE TABLE blacklist(company TEXT, PRIMARY KEY(company))""")

def db_add_offer(offer):
    try:
        conn = lite.connect("jobs.db")
        conn.text_factory = str
        cursor = conn.cursor()
        #print "%s" % offer.content
        # cursor.execute("INSERT INTO offers VALUES(?,?,?,?,?,?,?,?,?,?,?)",
        #         (offer.src, offer.ref,
        #          offer.date_pub.strftime('%s'), offer.date_add.strftime('%s'),
        #          offer.title, offer.company, offer.contract, offer.location, offer.salary, offer.url, offer.content))
        # conn.commit()

    except lite.Error, e:
        print "Error %s:" % e.args[0]

    finally:
        if conn:
            conn.close()

def report_generate():
    report = open('full_report.html', 'w')
    conn = lite.connect("jobs.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM offers ORDER BY date_pub DESC"
    cursor.execute(sql)
    data = cursor.fetchall()

    report.write("<html><head>")
    report.write("<link href=\"./bootstrap.css\" rel=\"stylesheet\">")
    report.write("<style>table{border:1px solid black; font: 10pt verdana, geneva, lucida, 'lucida grande', arial, helvetica, sans-serif;}</style>")
    report.write("<meta http-equiv=\"Content-type\" content=\"text/html\"; charset=\"utf-8\"></head>")
    report.write("<body><table class=\"table table-bordered\">")

    report.write("<thead>")
    report.write("<tr>")
    report.write("<th>Pubdate</th>")
    report.write("<th>Source</th>")
    report.write("<th>Title</th>")
    report.write("<th>Location</th>")
    report.write("<th>Company</th>")
    report.write("<th>Salary</th>")
    report.write("</tr>")
    report.write("</thead>")

    for row in data:
        offer = Offer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        report.write("<tr>")
        report.write('<td>' + offer.date_pub.strftime('%Y-%m-%d') + '</a></td>')
        report.write('<td>' + offer.src + '</td>')
        report.write('<td><a href="'+offer.url+'">' + offer.title + '</a></td>')
        report.write('<td>' + offer.location + '</td>')
        report.write('<td>' + offer.company + '</td>')
        report.write('<td>' + offer.salary + '</td>')
        report.write("</tr>")
    report.write("</table></body></html>")
    report.close()

if __name__ == '__main__':
    parser = OptionParser(usage = 'syntax: %prog [options] <from> [to]')
    args = sys.argv[1:]

    parser.set_defaults(version = False)
    parser.add_option('-v', '--version',
                          action = 'store_true', dest = 'version',
                          help = 'Output version information and exit')
    parser.add_option('-r', '--report',
                          action = 'store_true', dest = 'report',
                          help = 'Generate a full report')
    parser.add_option('-a', '--add',
                          action = 'store_true', dest = 'add',
                          help = 'add an offer')
    parser.add_option('-c', '--create',
                          action = 'store_true', dest = 'create',
                          help = 'create the databse')

    (options, args) = parser.parse_args(args)

    if options.version:
        print 'apecbot version %s - %s (%s)' % (__version__,
                                                __copyright__,
                                                __license__)
        sys.exit(0)

    if options.report:
        print "Report generation..."
        report_generate()
        print "Done."
        sys.exit(0)

    if options.add:
        if len(args) == 11:
            print "%s" % args[10]
            offer = Offer(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9], args[10])
            db_add_offer(offer)

        sys.exit(0)

    if options.create:
        db_create()
        sys.exit(0)
