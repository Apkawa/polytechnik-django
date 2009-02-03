#!/usr/bin/env python
# -*- coding: utf-8 -*-
from odf.opendocument import OpenDocumentSpreadsheet, load
from odf.style import Style, TextProperties, TableCellProperties,TableRowProperties, ParagraphProperties
from odf.style import TableColumnProperties
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell

import conn_site
from polytechnik.price.models import Price, Valyuta, Postavshik, Manufacturer, Category, News, Pages, Type
import datetime
date = datetime.datetime.now().date().strftime('%F')


import os

class Save_to_ods:
    def __init__(self):
        #self.doc = load("themplate.ods")

        self.doc = OpenDocumentSpreadsheet()
        # Create a style for the table content. One we can modify
        # later in the word processor.
        '''border-bottom="none" fo:border-left="none" fo:border-right="0.002cm solid #000000" fo:border-top="none"        '''

        self.head = Style(name="head", family="table-cell")
        self.head.addElement( TextProperties(fontweight="bold", fontweightasian="bold", fontsize="14pt"))
        self.doc.styles.addElement(self.head)

        self.tablehead = Style(name="tablehead", family="table-cell")
        self.tablehead.addElement( TableCellProperties( border="0.004cm solid #000000", padding="0.199cm",  ) )
        self.tablehead.addElement(ParagraphProperties(numberlines="false", linenumber="0", textalign="center"))
        self.tablehead.addElement( TextProperties(fontweight="bold", fontweightasian="bold", fontsize="14pt"))
        self.doc.styles.addElement(self.tablehead)

        self.tablecontents = Style(name="content", family="table-cell")
        self.tablecontents.addElement(
                TableCellProperties(
#                    borderbottom="none",
 #                   borderleft="none",
  #                  borderright="0.002cm solid #000000",
   #                 bordertop="none",
                    border="0.002cm solid #000000",
                    wrapoption="wrap",
                    verticalalign="middle",
                    paddingleft="0.1cm",
                    paddingright="0.1cm",
                    paddingtop="0.4cm",
                    paddingbottom="0.4cm",
                    ) )
        self.tablecontents.addElement( TableRowProperties(breakbefore="auto", useoptimalrowheight="true",rowheight="3cm",  ) )
        self.tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0",))# marginleft="0.4cm"))
        #self.tablecontents.addElement( TextProperties(hyphenate="true"))
        self.doc.styles.addElement(self.tablecontents)

        self.tablemanuf = Style(name="manuf", family="table-cell")
        self.tablemanuf.addElement(
                TableCellProperties(
                    borderbottom="0.004cm solid #000000",
                    borderleft="none", borderright="none",
                    bordertop="0.004cm solid #000000",
                    backgroundcolor="#CCCCCC",
                    padding="0.4cm",
                    ) )
        self.tablemanuf.addElement(ParagraphProperties(numberlines="false", linenumber="0", ))#marginleft="0.4cm"))
        self.tablemanuf.addElement(ParagraphProperties(numberlines="false", linenumber="0", textalign="center"))
        self.tablemanuf.addElement( TextProperties(fontweight="bold", fontweightasian="bold"))
        self.doc.styles.addElement(self.tablemanuf)

# Create automatic styles for the column widths.
# We want two different widths, one in inches, the other one in metric.
# ODF Standard section 15.9.1
        widthname = Style(name="Wname", family="table-column")
        widthname.addElement(TableColumnProperties(columnwidth="4.2 cm"))
        self.doc.automaticstyles.addElement(widthname )

        widthdesc = Style(name="Wdesc", family="table-column")
        widthdesc.addElement(TableColumnProperties(columnwidth="10 cm",useoptimalcolumnwidth
="1"))
        self.doc.automaticstyles.addElement( widthdesc )

        widthcell = Style(name="Wcell", family="table-column")
        widthcell.addElement(TableColumnProperties(columnwidth="2.3 cm"))
        widthcell.addElement(ParagraphProperties(numberlines="false", linenumber="0", textalign="end"))
        self.doc.automaticstyles.addElement(widthcell)

# Start the table, and describe the columns
        self.table = Table(name=date)
        self.table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthname))
        self.table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthdesc))
        self.table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthcell))
    def generate_ods(self, path="test"):
        head = (
                ( '',u'OOO "Политехник"',),
                ( u'phone:','+7 (812) 571-11-10'),
                ( u'email:','polytechnik@bk.ru'),
                ( u'www:','http://polytechnik.ru'),
                ('',),
                ( '',u'Прайс от %s'%date,),
                ('',),
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

        for t_h in ( ( u'Наименование',u'Описание',u'Цена',), ):
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
            if manuf != p.manufacturer_id:
                manuf = p.manufacturer.id
                for m in  ( '',p.manufacturer.name,'' ):
                    tc = TableCell( stylename= self.tablemanuf )
                    tr.addElement(tc)
                    _p = P(text=m)
                    tc.addElement(_p)
                tr = TableRow( stylename = self.tablecontents )
                self.table.addElement(tr)

            if type_product != p.type_product_id and p.type_product_id != 13:
                type_product = p.type_product_id
                for m in  ('', p.type_product.name, '' ):
                    tc = TableCell( stylename= self.tablemanuf )
                    tr.addElement(tc)
                    _p = P(text=m)
                    tc.addElement(_p)
                tr = TableRow( stylename = self.tablecontents )
                self.table.addElement(tr)

            if p.desc:
                p_price = ( p.name, p.desc, ' %.2f %s'%(p.cell, p.valyuta.desc))
            else:
                p_price = ( '',p.name, ' %.2f %s'%(p.cell, p.valyuta.desc))

            for pl in p_price:
                #if p.desc:
                tc = TableCell( stylename= self.tablecontents)
                #else:
                #tc = TableCell( stylename= self.tablecontents, table={'numbercolumnsspanned':2, 'number-rows-spanned':1} )
                tr.addElement(tc)
                p = P(text=pl)
                tc.addElement(p)
        self.doc.spreadsheet.addElement( self.table )
        self.doc.save( path , True)

    def connect_base(self, category_id = 202):
        self.base = []
        self.category = Category.objects.get(id= category_id )
        self.price = Price.objects.filter( category = self.category ).order_by( 'manufacturer', 'type_product', 'cell' )
        if not self.price.count():
            return False
        else:
            return True

def save_ods_to_xls(path):
    ar =  'openoffice.org3.0 -invisible \"macro:///Standard.Module1.SaveAsXLS(%s.ods)\"'%path
    command = ar.encode('utf-8')
    os.popen( command )
    print "Save As XLS file: %s.ods"%path
    pass

def generate_all_prices():
    root_dir = '/home/apkawa/work/2009/price/%s'%date
    try:
        os.mkdir( root_dir )
    except:
        pass
    root_c = Category.objects.filter( parent__id = None )
    for r in root_c:
        #print r.name,';', r.slug, ';', r.id
        sub_c = Category.objects.filter( parent = r )
        for s in sub_c:
            s_path = os.path.join( root_dir, r.name, s.name )
            _gt = Save_to_ods()
            if _gt.connect_base( category_id=s.id ):
                path = os.path.join( root_dir, r.name )
                try:
                    os.mkdir(path)
                except:
                    pass
                _gt.generate_ods( s_path )
                save_ods_to_xls( s_path )
    _all = Category.objects.all()
    for a in _all:
        if a.id == a.parent_id:
            s_path = os.path.join( root_dir, a.name )
            _gt = Save_to_ods()
            if _gt.connect_base( category_id=a.id ):
                _gt.generate_ods( s_path )
                save_ods_to_xls( s_path )

            #print a.name,';', a.slug, ';', a.id
    pass

##########################################################################################################

if __name__ == '__main__':
    from sys import argv
    if argv[1] in ('--all', '-a'):
        generate_all_prices()
    elif argv[1] == '--id':
        t = Save_to_ods()
        t.connect_base( argv[2] )
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

