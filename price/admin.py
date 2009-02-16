from polytechnik.price.models import Price, Valyuta, Postavshik, Manufacturer, Category, News, Pages, Clients, Type
from django.contrib import admin


class PriceAdmin(admin.ModelAdmin):
    list_display = ( 'preview_img_url','name','category', 'manufacturer', 'postavshik', 'e_cell')
    list_display_links = ( 'name', )
    list_filter = ('postavshik','manufacturer', 'category')

    pass

admin.site.register( Price, PriceAdmin)


class ValyutaAdmin(admin.ModelAdmin):
    pass

admin.site.register( Valyuta, ValyutaAdmin)


class ManufacturerAdmin(admin.ModelAdmin):
    pass

admin.site.register( Manufacturer, ManufacturerAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'id','name', 'slug', 'parent')
    pass

admin.site.register( Category, CategoryAdmin)


class PostavshikAdmin(admin.ModelAdmin):

    pass

admin.site.register( Postavshik, PostavshikAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('head','date', 'hide')
    pass

admin.site.register( News, NewsAdmin)


class PagesAdmin(admin.ModelAdmin):
    pass

admin.site.register( Pages, PagesAdmin)

class ClientsAdmin(admin.ModelAdmin):
    pass

admin.site.register( Clients, ClientsAdmin)

class TypeAdmin(admin.ModelAdmin):
    pass

admin.site.register( Type, TypeAdmin)
