from django.contrib import admin
from .models import VAPProductionData, ProductData, SourceData, ProductionDescription


@admin.register(VAPProductionData)
class VAPProductionDataAdmin(admin.ModelAdmin):
    list_display = ('Date', 'PlantLoc', 'Shift', 'get_product_name', 'TimeStart', 'TimeEnd', 'Total')
    list_filter = ('Date', 'PlantLoc', 'Shift', 'Product')
    search_fields = ('Product__Product', 'ProdMinDescrip__ProdMinDes')
    ordering = ('-Date', '-TimeStart')

    def get_product_name(self, obj):
        return obj.Product.Product if obj.Product else '-'
    get_product_name.short_description = 'Product'


@admin.register(ProductData)
class ProductDataAdmin(admin.ModelAdmin):
    list_display = ('Product',)
    search_fields = ('Product',)


@admin.register(SourceData)
class SourceDataAdmin(admin.ModelAdmin):
    list_display = ('Source',)
    search_fields = ('Source',)


@admin.register(ProductionDescription)
class ProductionDescriptionAdmin(admin.ModelAdmin):
    list_display = ('SecID', 'ProdMinDes')
    search_fields = ('ProdMinDes',)
