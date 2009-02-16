# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
def upload_img(url):
    from libuimge.imagehost import Host_r_radikal
    img = Host_r_radikal().send( url, True )
    if img:
        return img
    else:
        return None


class Clients( models.Model ):
    name = models.CharField( max_length = 222 )
    email = models.EmailField(blank=True)
    www = models.URLField(blank=True)
    def __unicode__(self):
        return  u'%s'%self.name

class Postavshik(models.Model):
    name = models.CharField( max_length = 222 )
    email = models.EmailField(blank=True)
    www = models.URLField(blank=True)
    marketing_margin = models.FloatField('% наценки',blank=True, default = 0)
    def __unicode__(self):
        return  u'%s'%self.name

class Manufacturer( models.Model):
    name = models.CharField( max_length = 222 )
    www = models.URLField(blank=True)
    img_url = models.URLField(blank=True)
    pos = models.IntegerField( blank=True, null=True)
    def __unicode__(self):
        return  u'%s'%self.name

class Category( models.Model ):
    name = models.CharField( max_length = 222 )
    slug = models.CharField( max_length = 100 )
    parent = models.ForeignKey('self', blank=True,null=True)
    desc = models.TextField( max_length = 2048, blank= True )
    img_url = models.URLField(blank=True)
    old_db = models.BooleanField( default=False, )
#    page_mode = models.BooleanField( default=False, blank=True )
    def __unicode__(self):
        return  u'%s'%self.name

class Type( models.Model ):
    name = models.CharField( max_length = 222 )
    slug = models.CharField( max_length = 100, blank=True )
    parent = models.ForeignKey('self', blank=True,null=True)
    desc = models.TextField( max_length = 500, blank=True )
    img_url = models.URLField(blank=True)
    pos = models.IntegerField( blank=True, null=True)
    def __unicode__(self):
        return  u'%s'%self.name

class Price( models.Model ):
    name = models.TextField( max_length = 1024 )
    desc = models.TextField( max_length = 2048, blank = True )
    cell = models.FloatField()
    valyuta = models.ForeignKey( 'Valyuta' )
    postavshik =  models.ForeignKey( 'Postavshik' , blank=True, null=True)
    manufacturer = models.ForeignKey( 'Manufacturer', blank=True, null=True)
    category = models.ForeignKey( 'Category')
    type_product = models.ForeignKey('Type', blank = True, null=True )
    img_url = models.URLField(blank=True)
    thumb_img_url = models.URLField(blank=True)

    def preview_img_url(self):
        return '<img src="%s" alt="" width="100"/>'%self.thumb_img_url
    preview_img_url.allow_tags = True

    def e_cell(self):
        return '%.2f%s'%(self.cell, self.valyuta.desc)

    def save(self,  force_insert=False, force_update=False ):
        if self.img_url:
            upl_url = upload_img( self.img_url )
            if upl_url:
                self.img_url = upl_url[0]
                self.thumb_img_url = upl_url[1]
            else:
                self.img_url = None
                self.thumb_img_url = None
        else:
            self.thumb_img_url = None
        super( Price, self).save()

    def __unicode__(self):
        return  u'%s'%self.name

class Valyuta( models.Model ):
    name = models.CharField(max_length = 222)
    desc = models.CharField(max_length = 222, blank=True )
    cource = models.FloatField(blank=True)
    def __unicode__(self):
        return  u'%s'%self.name

class News( models.Model ):
    head = models.CharField( max_length = 222 )
    body = models.TextField( max_length = 1024 )
    date = models.DateField( )
    hide = models.BooleanField( default = False)
    def __unicode__(self):
        return  u'%s'%self.head

class Pages( models.Model ):
    name = models.CharField( max_length = 222 )
    body = models.TextField( max_length = 1024 )
    slug = models.CharField( max_length = 100 )
    img_url_1 = models.URLField(blank=True)
    img_url_2 = models.URLField(blank=True)
    def _save(self):
        if self.img_url_1 or self.img_url_2:
            if self.img_url_1:
                self.img_url_1 = upload_img( self.img_url_1[0])
            if self.img_url_2:
                self.img_url_2 = upload_img( self.img_url_2[0])
        super( Pages, self).save()

    def __unicode__(self):
        return  u'%s'%self.name




