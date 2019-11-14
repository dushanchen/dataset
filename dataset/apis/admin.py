from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(Lungis)
admin.site.register(PorkMarket)
admin.site.register(PorkBrand)
admin.site.register(FoodSample)