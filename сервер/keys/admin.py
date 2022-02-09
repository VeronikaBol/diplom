from django.contrib import admin

# Register your models here.
from catalog.models import StoreModel,FolderModel, FileModel, FileEntityModel, StoreUserModel, BlockModel, AccessModel


class CatalogAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
admin.site.register(AccessModel,CatalogAdmin)
admin.site.register(BlockModel,CatalogAdmin)
admin.site.register(StoreUserModel,CatalogAdmin)
admin.site.register(StoreModel,CatalogAdmin)
admin.site.register(FolderModel,CatalogAdmin)
admin.site.register(FileModel,CatalogAdmin)
admin.site.register(FileEntityModel,CatalogAdmin)