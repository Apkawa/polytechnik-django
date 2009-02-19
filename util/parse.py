# -*- coding: utf-8 -*-
import os, sys
sys.path.append('/home/apkawa/Code/work')
remote = True
from django.core.management import setup_environ
if remote:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'polytechnik.settings_remote'
    from polytechnik import settings_remote
    setup_environ( settings_remote)
else:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'polytechnik.settings'
    from polytechnik import settings
    setup_environ(settings)



from polytechnik.price.models import Price, Valyuta, Postavshik, Manufacturer, Category, News, Pages, Type
import csv
import re
import time

'''
format delimiter=',' quotechar='"'

name, desc, cell, manufacturer, postavshik_id, category_id, img_url_flag ( 1 - find in google )

0	     1	    2	    3	    4	        5	        6	    7	        8
name_pr	desc	cell	manuf	pos	type_product	pos_t	category_id	    img_flag


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
    def __init__(self, test = False):
        self.test = test
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
        for l in self.loaded:
            #time.sleep(1)
            name = clear_space( l[0])
            if not name:
                continue
            elif name == '#D':
                print '#D ',l[1]
                category_id = l[1]
                p = Price.objects.filter( category__id = category_id )
                print p
                p.delete()
                continue

            desc = clear_space( l[1])
            match = '\$|€|руб\.|р\.|y\.e\.|У\.Е\.'
            v = ''.join(re.findall('(%s)'%match,l[2]))
            _valyuta = Valyuta.objects.filter( desc = v )
            if _valyuta:
                cell = float(re.sub(',','.', re.sub( '(%s|[\s]|\xc2\xa0)'%match ,'',l[2])))
                l_3 = clear_space(l[3])
                if l_3:
                    _m = Manufacturer.objects.get_or_create( name = l_3 , defaults={'pos': int(l[4]) if l[4] else 0} )
                    manufac  = _m[0]
                    if not _m[1]:
                        manufac.pos =int(l[4]) if l[4] else 0
                        manufac.save()

                else:
                    manufac = Manufacturer.objects.get( id = 233 )

                l_5 = clear_space(l[5])
                if l_5:

                    _t = Type.objects.get_or_create( name = l_5, defaults={'pos':int(l[6])if l[6] else 0} )
                    type_product = _t[0]
                    if not _t[1]:
                        type_product.pos = int(l[6])if l[6] else 0
                        type_product.save()

                else:
                    type_product = Type.objects.get( id = 13 )
                postavshik = None #Postavshik.objects.get( id = int(l[5]) ) if l[5] else None
                category = Category.objects.get( id= int(l[7]))
                try:
                    img_url_flag = l[8]
                except IndexError:
                    img_url_flag = None
                if re.match('http://',img_url_flag):
                    img_url = img_url_flag
                elif img_url_flag:
                    word =  manufac[0].name.encode('utf-8')+name
                    img_url = self._find_in_google(word )
                else:
                    img_url = None
                print name, desc, cell, _valyuta, category, img_url
                p = Price.objects.get_or_create(name = name, category = category, desc = desc,
                        defaults={#'desc': desc,
                            'cell':cell,
                            'valyuta' : _valyuta[0],
                            'manufacturer': manufac,
                            'type_product': type_product,
                            'img_url':img_url,
                            'postavshik': postavshik,
                            })
                print p
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

def tree_category():
    root_c = Category.objects.filter( parent__id = None )
    for r in root_c:
        print r.id,';',r.name,';', r.slug, ';',r.price_set.all().count()
        sub_c = Category.objects.filter( parent = r )
        for s in sub_c:
            print s.id, ';','    ',s.name,';', s.slug, ';', s.price_set.all().count()
    _all = Category.objects.all()
    for a in _all:
        if a.id == a.parent_id:
            print a.id, ';',a.name,';', a.slug,';',a.price_set.all().count()

def clear_space(text):
        cleared_t = re.sub( '(^\s|\s$)','',re.sub('[\s]{2,}',' ', text ))
        if cleared_t:
            return cleared_t
        else:
            return None


if __name__ == '__main__':
    import sys
    #print google( sys.argv[1] )
    p = Parse().load_file( sys.argv[1:])
    #tree_category()
