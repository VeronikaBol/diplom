from django.db import models
from users.models import ChildModel, UserModel
import datetime
import os



class KeysModel(models.Model):
    class Meta:
        verbose_name = 'Ключи'
        verbose_name_plural = 'Ключи'

    #ключ
    key = models.CharField(max_length=300, verbose_name='Ключ', default='')
    #пользоваитель
    user =models.ForeignKey(UserModel,blank=True, null=True,  on_delete=models.CASCADE)
    #файл
    file =models.ForeignKey(FileEntityModel,blank=True, null=True,  on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title


    def getJson(self):
        return  {
            'id':self.id,
            'key':self.key,
            'user':self.user.id,
            'file':self.file.id
        }



