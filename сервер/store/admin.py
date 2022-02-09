from django.contrib import admin

# Register your models here.
from store.models import  FileModel, FileSendModel, FileUserModel


class CatalogAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

admin.site.register(FileModel,CatalogAdmin)
admin.site.register(FileSendModel,CatalogAdmin)
admin.site.register(FileUserModel,CatalogAdmin)