from django.db import models
from users.models import  UserModel
import datetime
import os




#описывает файлы
class FileModel(models.Model):
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    title = models.CharField(max_length=300, verbose_name='Название', default='')
    entity = models.FileField(upload_to='store-secure/', null=True, verbose_name='Фото', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    def getJson(self):

        fullfilepath=  os.path.join(os.path.dirname(os.path.dirname(__file__)),"media/store-secure/" + str(self.title))
        filesize= os.path.getsize(fullfilepath)

        return  {
            'id':self.id,
            'title':self.title,
            'url':'http://veronika.tasty-catalog.ru/media/store-secure/'+self.title,
            'size':filesize,
            'date':self.created_at.strftime("%d.%m.%Y %H:%M") if self.created_at else ""
        }

#хранит информацию, кто каким файлом владеет
class FileUserModel(models.Model):
    class Meta:
        verbose_name = 'Хранение файлов'
        verbose_name_plural = 'Хранение файлов'

    user = models.ForeignKey(UserModel,blank=True, null=True,  on_delete=models.CASCADE)
    file = models.ForeignKey(FileModel,blank=True, null=True,  on_delete=models.CASCADE)



    def __str__(self):
        return self.file.title


#кто кому отправляет
class FileSendModel(models.Model):
    class Meta:
        verbose_name = 'Отправка файла'
        verbose_name_plural = 'Отправка файла'
    #отправитель
    userFrom = models.ForeignKey(UserModel,blank=True, null=True,  on_delete=models.CASCADE)
    #получатель
    userToId = models.CharField(max_length=300, verbose_name='Получатель', default='')
    #файл
    file = models.ForeignKey(FileModel,blank=True, null=True,  on_delete=models.CASCADE)
    #статус
    status = models.CharField(max_length=300, verbose_name='Статус', default='wait')
    #дата
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.title

    def getJson(self):
        return {
            'id':self.id,
            'user':self.userFrom.getJson(),
            'file':self.file.getJson(),
            'status':self.status,
            'date':self.created_at.strftime("%d.%m.%Y %H:%M") if self.created_at else "",
            'self':False
        }




