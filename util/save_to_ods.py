#!/usr/bin/env python
# -*- coding: utf-8 -*-
from odf.opendocument import OpenDocumentSpreadsheet, load
from odf.style import Style
from odf.style import PageLayout, PageLayoutProperties
from odf.style import TextProperties,  ParagraphProperties
from odf.style import TableColumnProperties,TableCellProperties,TableRowProperties

from odf.style import FontFace

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
        self.font = FontFace( name="Times New Roman", fontadornments="Normal", fontfamilygeneric="roman", fontpitch="variable" )
        self.doc.fontfacedecls.addElement( self.font )

        self.root_style = Style(name="rootstyle", family="table-cell")
        self.root_style.addElement(
                TableCellProperties(
                    wrapoption="wrap",
                    verticalalign="middle",
                    padding="0.049cm",
                    ) )
        #self.root_style.addElement( TableRowProperties(breakbefore="auto", useoptimalrowheight="true",rowheight="3cm",  ) )
        #self.root_style.addElement(ParagraphProperties(numberlines="false", linenumber="0",))# marginleft="0.4cm"))
        self.root_style.addElement( TextProperties( fontname="Times New Roman", fontnameasian="Times New Roman", fontsize="10pt"))
        self.doc.styles.addElement( self.root_style )

        page = PageLayout( name="page" )
        self.doc.automaticstyles.addElement( page )
        page.addElement( PageLayoutProperties( margintop="0.499cm", marginbottom="0.499cm", marginleft="2cm", marginright="0.499cm", shadow="none", backgroundcolor="transparent", tablecentering="horizontal", writingmode="lr-tb") )


        self.head = Style(name="head", family="table-cell", parentstylename="rootstyle")
        self.head.addElement( TextProperties(fontweight="bold", fontweightasian="bold", fontsize="12pt"))
        self.doc.styles.addElement(self.head)

        self.tablehead = Style(name="tablehead", family="table-cell", parentstylename="rootstyle")
        self.tablehead.addElement( ParagraphProperties(numberlines="false", linenumber="0", textalign="center"))
        self.tablehead.addElement( TableCellProperties( border="0.004cm solid #000000", padding="0.199cm",  ) )
        self.tablehead.addElement( TextProperties(fontweight="bold", fontweightasian="bold", fontsize="12pt"))
        self.doc.styles.addElement(self.tablehead)

        self.tablecontents = Style(name="content", family="table-cell", parentstylename="rootstyle")
        self.tablecontents.addElement(
                TableCellProperties(
                    border="0.004cm solid #000000",
                    wrapoption="wrap",
                    verticalalign="middle",
                    ) )
        self.doc.styles.addElement(self.tablecontents)


        self.tablemanuf = Style(name="manuf", family="table-cell", parentstylename="rootstyle")
        self.tablemanuf.addElement(
                TableCellProperties(
                    border="0.013cm solid #000000",
                    backgroundcolor="#CCCCCC",
                    ) )
        self.tablemanuf.addElement(ParagraphProperties( textalign="center" ))
        self.tablemanuf.addElement( TextProperties(fontweight="bold", fontweightasian="bold", fontsize="14pt" ))
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

        #>> Start the table, and describe the columns
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
    def add_spanned_row( self, _tuple, stylename, _count_col_spanned = 3):
        tr = TableRow()
        self.table.addElement(tr)
        for _c in _tuple:
            tc = TableCell( stylename= stylename )
            tc = TableCell( stylename= stylename, numbercolumnsspanned= _count_col_spanned, numberrowsspanned = 1 )
            tr.addElement(tc)
            p = P(text = _c )
            tc.addElement(p)
            tr.addElement( CoveredTableCell() )
    


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

        self.add_spanned_row( (u'OOO "Политехник"',), self.head )
        head = (
                ( u'phone:','+7 (812) 312-42-38'),
                ( u'','+7 (812) 970-42-93'),
                ( u'email:','polytechnik@bk.ru'),
                ( u'www:','http://polytechnik.ru'),
                ('',),
                )
        self.add_rows( head, self.head )
        self.add_row( ( u'Прайс от %s'%date,), self.root_style )
        self.add_spanned_row( (self.category.name, ), self.tablemanuf )
        
        self.add_row( ( u'Наименование',u'Описание',u'Цена',), self.tablehead )


        manuf = None
        type_product = 13
        for p in self.price:

            if manuf != p.manufacturer_id and p.manufacturer_id != 233:
                manuf = p.manufacturer.id
                self.add_spanned_row( (p.manufacturer.name,) , self.tablemanuf )

            if type_product != p.type_product_id and p.type_product_id != 13:
                type_product = p.type_product_id
                self.add_spanned_row( ( p.type_product.name,) , self.tablemanuf )

            p_desc = p.desc
            p_cell = ' %.0f %s'%(p.cell, p.valyuta.desc) if p.cell else ' -'

            if p_desc:
                self.add_row( ( p.name, p_desc, p_cell  ) , self.tablecontents )
            elif not p.desc and not p.cell:
                p_name = re.sub('(<h4>|</h4>)','',p.name)
                self.add_spanned_row( (p_name,), self.tablehead )
            else:
                tr = TableRow( stylename = self.tablecontents )
                self.table.addElement(tr)
                p_price = ( p.name, p_cell )

                #self.add_cell( pl, tr, self.tablecontents, )#numbercolumnsspanned=2, numberrowsspanned = 1 )
                tc = TableCell( stylename= self.tablecontents, numbercolumnsspanned=2, numberrowsspanned = 1 )
                tr.addElement(tc)
                p = P(text=p_price[0])
                tc.addElement(p)

                tr.addElement( CoveredTableCell() )


                self.add_cell( p_price[1], tr, self.tablecontents )

        self.doc.spreadsheet.addElement( self.table )
        self.doc.save( path , True)
    def read_stdout(self):
        print 'name; desc;cell; img_url'
        manuf = None
        type_product = None
        for p in self.price:
            if manuf != p.manufacturer_id and p.manufacturer_id != 233:
                manuf = p.manufacturer.id
                print p.manufacturer.name

            if type_product != p.type_product_id and p.type_product_id != 13:
                type_product = p.type_product_id
                print p.type_product.name
            print '%s;%s;%s;%s;'%(p.name, p.desc,'%.0f %s'%(p.cell, p.valyuta.desc), p.img_url if p.img_url else '' )


    def connect_base(self, category_id = 202, manufac_name = False):
        self.base = []
        self.category = Category.objects.get(id= category_id )
        if manufac_name:
            self.price = Price.objects.filter(
                    category = self.category, manufacturer__name = manufac_name ).order_by(
                            '-manufacturer__pos','manufacturer', '-type_product__pos','type_product','id' )
        else:
            self.price = Price.objects.filter( category = self.category ).order_by( 'manufacturer__pos','manufacturer',
                 'type_product__pos','type_product','id' )

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
    root_dir = '/home/apkawa/work/2009/price/%s_%s'%( date,'all' if not manuf_flag else 'all_by_manuf' )
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

def generate_by_rules():
    def __load_csv( path ):
        import csv
        c = csv.reader( open( path , 'r') )
        return [l for l in c]

    root_dir = '/home/apkawa/work/2009/price/%s_%s'%( date,'by_rule' )
    file_rule = '/home/apkawa/work/rules.csv'
    rules= __load_csv( file_rule )
    __type = { '#D': lambda x, f: None,#os.mkdir( x ),
                '#F': lambda d,f:None ,
                '#FO': lambda d,f: '#F %s'% os.path.join(d,f),
                '#FOC': lambda d,f: '#F %s'% os.path.join(d,f),
            }
    __type_keys = __type.keys()
    for rl in rules:
        flag = rl[0]
        name = rl[1]
        category_id = rl[2]
        manufacturer_name = rl[3] if rl[3] else False
        if flag in __type_keys:
            if flag == '#D':
                __dir = os.path.join( root_dir, rl[1] )
                try:
                    os.makedirs( __dir )
                except OSError:
                    pass
                print '#D',__dir
            elif flag in ('#F','#FO'):
                print rl
                __file = os.path.join( __dir,'%s%s'%(name,'(старое)' if flag == '#FO' else '' ))
                t = Save_to_ods()
                if category_id:
                    t.connect_base( category_id, manufacturer_name )
                    t.generate_ods( __file )
                else:
                    continue






##########################################################################################################

if __name__ == '__main__':
    from sys import argv
    if argv[1] in ('--all', '-a'):
        generate_all_prices()
    elif argv[1] in ('--all_m', '-am'):
        generate_all_prices( True )
    elif argv[1] == '--id':
        t = Save_to_ods()
        t.connect_base( argv[2] )
        t.generate_ods()
    elif argv[1] == '-r':
        t = Save_to_ods()
        t.connect_base( argv[2] )
        t.read_stdout()
    elif argv[1] == '--by_rules':
        generate_by_rules()
        

    pass

