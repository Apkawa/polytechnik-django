# -*- coding: utf-8 -*-
import os, sys
sys.path.append('/home/apkawa/Code/work')
os.environ['DJANGO_SETTINGS_MODULE'] = 'polytechnik.settings'
from django.core.management import setup_environ
from polytechnik import settings

setup_environ(settings)


from polytechnik.price.models import Price, Valyuta, Postavshik, Manufacturer, Category, News, Pages, Type
import csv
import re
import time

'''
format delimiter=',' quotechar='"'

name, desc, cell, manufacturer, category_id, img_url_flag ( 1 - find in google )


class Price( models.Model ):
    name = models.CharField( max_length = 222 )
    desc = models.CharField( max_length = 222 )
    cell = models.FloatField()
    valyuta = models.ForeignKey( 'Valyuta' )
    postavshik =  models.ForeignKey( 'Postavshik' )
    manufacturer = models.ForeignKey( 'Manufacturer')
    img_url = models.URLField(blank=True)
    position = models.IntegerField(blank=True)
    def __unicode__(self):
        return  u'%s'%self.name

'''
class Parse:
    def __init__(self):
        pass
    def _find_in_google(self, query):
        query = query
        return google(query)
        pass

    def load_file( self, argv ):
        csv_f = argv[0]
        #self.category = argv[1]
        c = csv.reader( open( csv_f , 'r') )
        self.loaded = [l for l in c]
        self._parse()
    def _parse( self ):
        print '_parse'
        for l in self.loaded:
            #time.sleep(1)
            name = l[0]
            if not name:
                print 'not name'
                continue
            desc = l[1]
            match = '\$|€|руб\.|р\.|y\.e\.|У\.Е\.'
            v = ''.join(re.findall('(%s)'%match,l[2]))
            _valyuta = Valyuta.objects.filter( desc = v )
            if _valyuta:
                print l
                cell = float(re.sub(',','.', re.sub( '(%s|[\s]|\xc2\xa0)'%match ,'',l[2])))
                manufac = Manufacturer.objects.get_or_create( name = l[3] )
                if l[4] and l[4] != 'NULL':
                    type_product = Type.objects.get_or_create( name = l[4] )
                elif not l[4] and l[4] == 'NULL':
                    type_product = ( None, )
                postavshik = Postavshik.objects.get( id = int(l[5]) )
                category = Category.objects.get( id= int(l[6]))
                try:
                    img_url_flag = l[7]
                except IndexError:
                    img_url_flag = None
                if img_url_flag:
                    word =  manufac[0].name.encode('utf-8')+name
                    img_url = self._find_in_google(word )
                else:
                    img_url = None
                print name, desc, cell, _valyuta, manufac[0], type_product, postavshik, category, img_url
                #Price.objects.get_or_create(name = name, desc =desc, cell = cell, valyuta = _valyuta[0],\
                #        manufacturer = manufac[0], img_url = img_url, category = category )

                Price.objects.get_or_create(name = name,
                        defaults={'desc':desc,
                            'cell':cell,
                            'valyuta' : _valyuta[0],
                            'manufacturer': manufac[0],
                            'type_product': type_product[0],
                            'img_url':img_url,
                            'postavshik': postavshik,
                            'category': category,
                            })
            else:
                continue
    def insert_db(self):
        pass

import urllib
from json import loads
def google(word):
    def web(results):
        if results:
            url = urllib.unquote(results[0]['url'])
            title1 = results[0]['titleNoFormatting']
            title2 = results[0]['title']
            content = re.sub('(<b>)|(</b>)','',results[0]['content'])
            text = '%s\n%s\n%s'%(title1,content,url)
            text = re.sub('&#39;','\'',unescape(text))
            #print text

            extra = '''<a href="%s">%s</a>
            <p>%s</p>
            '''%(url,title2,content)
            return True, text, extra
        else: return True, 'Nyaaa... Ничего не нашла.', ''
    def images(results):
        if results:
            imgurl = results[0]['unescapedUrl']
            return imgurl
        else: return None
    #http://code.google.com/apis/ajaxsearch/documentation/reference.html#_intro_fonje
    _type = 'images'
    #word = urllib.quote(word.encode('utf-8'))
    word = urllib.quote(word)
    src =  urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/%s?v=1.0&q=%s'%(_type,word)).read()
    convert = loads(src)
    results = convert['responseData']['results']
    return images(results)
    #if type == 'web':
        #return web(results)
    #if type == 'images':
   #     return images(results)

def tree_category(self):
    root_c = Category.objects.filter( parent__id = None )
    for r in root_c:
        print r.name,';', r.slug, ';', r.id
        sub_c = Category.objects.filter( parent = r )
        for s in sub_c:
            print '---->',s.name,';', s.slug, ';', s.id
    _all = Category.objects.all()
    for a in _all:
        if a.id == a.parent_id:
            print a.name,';', a.slug, ';', a.id


    pass
if __name__ == '__main__':
    import sys
    #print google( sys.argv[1] )
    print 'nya'
    p = Parse().load_file( sys.argv[1:])
    '''
    '€ 1 154,00'
    "$2 365,00"
    '''
