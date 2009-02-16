#!/usr/bin/env python
# -*- coding: utf-8 -*-
from odf.opendocument import OpenDocumentSpreadsheet, load
from odf.style import Style
from odf.style import PageLayout, PageLayoutProperties
from odf.style import TextProperties,  ParagraphProperties
from odf.style import TableColumnProperties,TableCellProperties,TableRowProperties

from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell, CoveredTableCell

import conn_site
from polytechnik.price.models import Price, Valyuta, Postavshik, Manufacturer, Category, News, Pages, Type
import datetime
date = datetime.datetime.now().date().strftime('%F')


import os
import re

class Save_to_ods:
    def __init__(self):
        pass
    def make_style(self, tablename=date):
        #self.doc = load("themplate.ods")

        self.doc = OpenDocumentSpreadsheet()
        # Create a style for the table content. One we can modify
        # later in the word processor.
        '''border-bottom="none" fo:border-left="none" fo:border-right="0.002cm solid #000000" fo:border-top="none"        '''

        self.root_style = Style(name="root_style", family="table-cell")
        self.root_style.addElement(
                TableCellProperties(
                    #borderbottom="none",
                    #borderleft="none",
                    #borderright="0.002cm solid #000000",
                    #bordertop="none",
                    #border="0.002cm solid #000000",
                    wrapoption="wrap",
                    verticalalign="middle",
                    padding="0.049cm",
                    ) )
        self.root_style.addElement( TableRowProperties(breakbefore="auto", useoptimalrowheight="true",rowheight="3cm",  ) )
        self.root_style.addElement(ParagraphProperties(numberlines="false", linenumber="0",))# marginleft="0.4cm"))
        #self.tablecontents.addElement( TextProperties(hyphenate="true"))
        self.doc.styles.addElement( self.root_style )

        page = PageLayout( name="page" )
        self.doc.automaticstyles.addElement( page )
        page.addElement( PageLayoutProperties( margintop="0.499cm", marginbottom="0.499cm", marginleft="2cm", marginright="0.499cm", shadow="none", backgroundcolor="transparent", tablecentering="horizontal", writingmode="lr-tb") )


        self.head = Style(name="head", family="table-cell")
        self.head.addElement( TextProperties(fontweight="bold", fontweightasian="bold", fontsize="14pt"))
        self.doc.styles.addElement(self.head)

        self.tablehead = Style(name="tablehead", family="table-cell")
        self.tablehead.addElement( TableCellProperties( border="0.004cm solid #000000", padding="0.199cm",  ) )
        self.tablehead.addElement( ParagraphProperties(numberlines="false", linenumber="0", textalign="center"))
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
                    #paddingleft="0.1cm",
                    #paddingright="0.1cm",
                    #paddingtop="0.4cm",
                    #paddingbottom="0.4cm",
                    ) )
        self.doc.styles.addElement(self.tablecontents)

 #       self.tablecontents_m2cell = Style(name = "content_m2cell", family="table-cell", parentstylename="content" )
#        self.tablecontents_m2cell.addElement( TableCellProperties( t

        self.tablemanuf = Style(name="manuf", family="table-cell", parentstylename="root_style")
        self.tablemanuf.addElement(
                TableCellProperties(
                    borderbottom="0.004cm solid #000000",
                    borderleft="none", borderright="none",
                    bordertop="0.004cm solid #000000",
                    backgroundcolor="#CCCCCC",
                    ) )
        self.tablemanuf.addElement(ParagraphProperties( textalign="center" ))
        self.tablemanuf.addElement( TextProperties(fontweight="bold", fontweightasian="bold"))
        self.doc.styles.addElement(self.tablemanuf)

# Create automatic styles for the column widths.
# We want two different widths, one in inches, the other one in metric.
# ODF Standard section 15.9.1
        widthname = Style(name="Wname", family="table-column")
        widthname.addElement(TableColumnProperties(columnwidth="5 cm"))
        self.doc.automaticstyles.addElement(widthname )

        widthdesc = Style(name="Wdesc", family="table-column")
        widthdesc.addElement(TableColumnProperties(columnwidth="11 cm",useoptimalcolumnwidth
="1"))
        self.doc.automaticstyles.addElement( widthdesc )

        widthcell = Style(name="Wcell", family="table-column")
        widthcell.addElement(TableColumnProperties(columnwidth="2.3 cm"))
        widthcell.addElement(ParagraphProperties(numberlines="false", linenumber="0", textalign="end"))
        self.doc.automaticstyles.addElement(widthcell)

# Start the table, and describe the columns
        self.table = Table(name= tablename )
        self.table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthname))
        self.table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthdesc))
        self.table.addElement(TableColumn(numbercolumnsrepeated=1,stylename=widthcell))
    def add_rows(self, _tuple, stylename):
        '''
        _tuple example

        (
        ('','',), # 1 row
        ('','','',), # 2 row
        )
        '''
        for _r in _tuple:
            tr = TableRow()
            self.table.addElement(tr)
            for _c in _r:
                tc = TableCell( stylename= stylename )
                tr.addElement(tc)
                p = P(text = _c )
                tc.addElement(p)
    def add_row( self, _tuple, stylename):
        tr = TableRow()
        self.table.addElement(tr)
        for _c in _tuple:
            tc = TableCell( stylename= stylename )
            tr.addElement(tc)
            p = P(text = _c )
            tc.addElement(p)

    def add_cell( self, _cell, _table_row, stylename):
        tc = TableCell( stylename= stylename )
        _table_row.addElement(tc)
        p = P(text = _cell )
        tc.addElement(p)



    def generate_ods(self, path="/home/apkawa/work/test_desu"):
        self.make_style( tablename = self.category.name )
        head = (
                ( '',u'OOO "Политехник"',),
                ( u'phone:','+7 (812) 312-42-38'),
                ( u'','+7 (812) 970-42-93'),
                ( u'email:','polytechnik@bk.ru'),
                ( u'www:','http://polytechnik.ru'),
                ('',),
                )
        self.add_rows( head, self.head )
        self.add_row( ( u'Прайс от %s'%date,), self.root_style )
        self.add_row( ( '',self.category.name, ), self.head )
        self.add_row( ( u'Наименование',u'Описание',u'Цена',), self.tablehead )


        manuf = None
        type_product = 13
        for p in self.price:

            if manuf != p.manufacturer_id and p.manufacturer_id != 233:
                manuf = p.manufacturer.id
                self.add_row( ( '',p.manufacturer.name,'' ) , self.tablemanuf )

            if type_product != p.type_product_id and p.type_product_id != 13:
                type_product = p.type_product_id
                self.add_row( ('', p.type_product.name, '' ) , self.tablemanuf )

            p_desc = p.desc

            if p_desc:
                self.add_row( ( p.name, p_desc, ' %.0f %s'%(p.cell, p.valyuta.desc) ) , self.tablecontents )
            else:
                tr = TableRow( stylename = self.tablecontents )
                self.table.addElement(tr)
                p_price = ( p.name, ' %.0f %s'%(p.cell, p.valyuta.desc))

                #self.add_cell( pl, tr, self.tablecontents, )#numbercolumnsspanned=2, numberrowsspanned = 1 )
                tc = TableCell( stylename= self.tablecontents, numbercolumnsspanned=2, numberrowsspanned = 1 )
                tr.addElement(tc)
                p = P(text=p_price[0])
                tc.addElement(p)

                tr.addElement( CoveredTableCell() )


                self.add_cell( p_price[1], tr, self.tablecontents )

        self.doc.spreadsheet.addElement( self.table )
        self.doc.save( path , True)

    def connect_base(self, category_id = 202, manufac_name = False):
        self.base = []
        self.category = Category.objects.get(id= category_id )
        if manufac_name:
            self.price = Price.objects.filter(
                    category = self.category, manufacturer__name = manufac_name ).order_by(
                            '-manufacturer__pos','manufacturer', '-type_product__pos','type_product','id' )
        else:
            self.price = Price.objects.filter( category = self.category ).order_by( 'manufacturer__pos','manufacturer',
                 '-type_product__pos','type_product','id' )

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


def generate_all_prices(manuf_flag = False):
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
            _gt = Save_to_ods()
            if manuf_flag:
                manufs = set(Manufacturer.objects.filter( price__category__id = s.id))
            else:
                manufs = ( False,)
            for m in manufs:
                s_path = os.path.join( root_dir,r.name if manuf_flag else '', s.name if manuf_flag else r.name, re.sub('(\"|\'|\(|\))','',m.name) if manuf_flag else s.name )
                print s_path
                if _gt.connect_base( category_id=s.id, manufac_name = m ):
                    path = os.path.join( root_dir,r.name if manuf_flag else '' , s.name if manuf_flag else r.name )
                    try:
                        os.makedirs(path)
                    except:
                        pass
                    _gt.generate_ods( s_path )
                    save_ods_to_xls( s_path )
    _all = Category.objects.all()
    for a in _all:
        if a.id == a.parent_id:
            if manuf_flag:
                manufs = set(Manufacturer.objects.filter( price__category__id = a.id))
            else:
                manufs = ( False,)

            _gt = Save_to_ods()
            for m in manufs:
                s_path = os.path.join( root_dir, a.name if manuf_flag else '' , re.sub('(\"|\'|\(|\))','',m.name) if manuf_flag else a.name )
                print s_path
                try:
                    os.makedirs(s_path)
                except:
                    pass

                if _gt.connect_base( category_id=a.id, manufac_name= m ):
                    _gt.generate_ods( s_path )
                    save_ods_to_xls( s_path )

            #print a.name,';', a.slug, ';', a.id
    pass

##########################################################################################################

if __name__ == '__main__':
    from sys import argv
    if argv[1] in ('--all', '-a'):
        generate_all_prices()
    if argv[1] in ('--all_m', '-am'):
        generate_all_prices( True )
    elif argv[1] == '--id':
        t = Save_to_ods()
        t.connect_base( argv[2] )
        t.generate_ods()

    pass

