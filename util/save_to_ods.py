#!/usr/bin/env python
# -*- coding: utf-8 -*-
from odf.opendocument import OpenDocumentSpreadsheet, load
from odf.style import Style, TextProperties, TableCellProperties,TableRowProperties, ParagraphProperties
from odf.style import TableColumnProperties
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell

import conn_site
from polytechnik.price.models import Price, Valyuta, Postavshik, Manufacturer, Category, News, Pages, Type

class Save_to_ods:
    def __init__(self):
        #self.doc = load("themplate.ods")

        self.doc = OpenDocumentSpreadsheet()
# Create a style for the table content. One we can modify
# later in the word processor.
        '''border-bottom="none" fo:border-left="none" fo:border-right="0.002cm solid #000000" fo:border-top="none"        '''

        self.head = Style(name="head", family="table-cell")
        self.head.addElement( TextProperties(fontweight="bold", fontweightasian="bold"))
        self.doc.styles.addElement(self.head)

        self.tablehead = Style(name="tablehead", family="table-cell")
        self.tablehead.addElement( TableCellProperties( border="0.002cm solid #000000") )
        self.tablehead.addElement(ParagraphProperties(numberlines="false", linenumber="0", textalign="center"))
        self.tablehead.addElement( TextProperties(fontweight="bold", fontweightasian="bold"))
        self.doc.styles.addElement(self.tablehead)

        self.tablecontents = Style(name="content", family="table-cell")
        self.tablecontents.addElement(
                TableCellProperties(
                    borderbottom="none",
                    borderleft="none",
                    borderright="0.002cm solid #000000",
                    bordertop="none",
                    wrapoption="wrap",
                    verticalalign="middle",
                    ) )
        self.tablecontents.addElement( TableRowProperties(breakbefore="auto", useoptimalrowheight="true",rowheight="3cm",  ) )
        self.tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0", marginleft="0.353cm"))
        self.tablecontents.addElement( TextProperties(hyphenate="true"))
        self.doc.styles.addElement(self.tablecontents)

        self.tablemanuf = Style(name="manuf", family="table-cell")
        self.tablemanuf.addElement(
                TableCellProperties( borderbottom="none", borderleft="none", borderright="0.002cm solid #000000", bordertop="none" ) )
        self.tablemanuf.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
        self.tablemanuf.addElement( TextProperties(fontweight="bold", fontweightasian="bold"))
        self.doc.styles.addElement(self.tablemanuf)

# Create automatic styles for the column widths.
# We want two different widths, one in inches, the other one in metric.
# ODF Standard section 15.9.1
        widthname = Style(name="Wname", family="table-column")
        widthname.addElement(TableColumnProperties(columnwidth="7 cm"))
        self.doc.automaticstyles.addElement(widthname )

        widthdesc = Style(name="Wdesc", family="table-column")
        widthdesc.addElement(TableColumnProperties(columnwidth="20 cm",useoptimalcolumnwidth
="1"))
        self.doc.automaticstyles.addElement( widthdesc )

        widthcell = Style(name="Wcell", family="table-column")
        widthcell.addElement(TableColumnProperties(columnwidth="3 cm"))
        self.doc.automaticstyles.addElement(widthcell)

# Start the table, and describe the columns
        self.table = Table(name="Password")
        self.table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthname))
        self.table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthdesc))
        self.table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthcell))
        pass
    def generate_ods(self):
        head = (
                ( u'OOO "Политехник"',),
                ( u'тел:',''),
                ( u'email:',''),
                ( u'www:',''),
                ( '',),
                ( '',self.category.name, ),
                )
        for h in head:
            tr = TableRow()
            self.table.addElement(tr)
            for r in h:
                tc = TableCell( stylename= self.head )
                tr.addElement(tc)
                p = P(text = r )
                tc.addElement(p)

        for t_h in ( ( u'Наименование',u'Описаное',u'Цена',), ):
            tr = TableRow()
            self.table.addElement(tr)
            for r in t_h:
                tc = TableCell( stylename = self.tablehead )
                tr.addElement(tc)
                p= P(text=r)
                tc.addElement(p)


        manuf = None
        type_product = 13
        for p in self.price:

            tr = TableRow( stylename = self.tablecontents )
            self.table.addElement(tr)
            if manuf != p.manufacturer.id:
                manuf = p.manufacturer.id
                for m in  ( p.manufacturer.name, '','' ):
                    tc = TableCell( stylename= self.tablemanuf )
                    tr.addElement(tc)
                    _p = P(text=m)
                    tc.addElement(_p)
                tr = TableRow( stylename = self.tablecontents )
                self.table.addElement(tr)
            if type_product != p.type_product.id:
                type_product = p.type_product.id
                for m in  ( p.type_product.name, '','' ):
                    tc = TableCell( stylename= self.tablemanuf )
                    tr.addElement(tc)
                    _p = P(text=m)
                    tc.addElement(_p)
                tr = TableRow( stylename = self.tablecontents )
                self.table.addElement(tr)

            for pl in ( p.name, p.desc, ' %.2f %s'%(p.cell, p.valyuta.desc)):
                tc = TableCell( stylename= self.tablecontents )
                tr.addElement(tc)
                p = P(text=pl)
                tc.addElement(p)
        self.doc.spreadsheet.addElement( self.table )
        self.doc.save("test", True)

    '''
        for line in self.base:
            tr = TableRow()
            self.table.addElement(tr)
            for val in line:
                tc = TableCell( stylename= self.tablecontents )
                tr.addElement(tc)
                p = P(text=val)
                tc.addElement(p)
    '''

    def connect_base(self):
        self.base = []
        self.category = Category.objects.get(id=202)
        self.price = Price.objects.filter( category = self.category ).order_by( 'manufacturer', 'type_product', 'cell' )

##########################################################################################################

if __name__ == '__main__':
    t = Save_to_ods()
    t.connect_base()
    t.generate_ods()

    pass
'''
def read_base():
    category = Category.objects.get(id=199)
    print category.name
    price = Price.objects.filter( category = category ).order_by( 'manufacturer', 'cell' )
    manuf = None
    for p in price:
        if manuf != p.manufacturer.id:
            manuf = p.manufacturer.id
            print p.manufacturer.name
        print '%s %s %f %s'%(p.name, p.desc, p.cell,p.valyuta.desc)

def generate_ods():
    doc = OpenDocumentSpreadsheet()
# Create a style for the table content. One we can modify
# later in the word processor.
    tablecontents = Style(name="Table Contents", family="paragraph")
    tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
    doc.styles.addElement(tablecontents)

# Create automatic styles for the column widths.
# We want two different widths, one in inches, the other one in metric.
# ODF Standard section 15.9.1
    widthdesc = Style(name="Wshort", family="table-column")
    widthdesc.addElement(TableColumnProperties(columnwidth="20 cm"))
    doc.automaticstyles.addElement(widthdesc)

    widthcell = Style(name="Wwide", family="table-column")
    widthcell.addElement(TableColumnProperties(columnwidth="1.5in"))
    doc.automaticstyles.addElement(widthcell)

# Start the table, and describe the columns
    table = Table(name="Password")
    #table.addElement(TableColumn(numbercolumnsrepeated=4,stylename=widthshort))
    table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthcell))

    f = open('/etc/passwd')
    for line in f:
        rec = line.strip().split(":")
        tr = TableRow()
        table.addElement(tr)
        for val in rec:
            tc = TableCell()
            tr.addElement(tc)
            p = P(stylename=tablecontents,text=val)
            tc.addElement(p)

    doc.spreadsheet.addElement(table)
    doc.save("passwd", True)
'''

