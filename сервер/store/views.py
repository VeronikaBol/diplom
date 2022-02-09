import json
import datetime
from django.http import JsonResponse
from django.shortcuts import render
import secure
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from cryptography.fernet import Fernet

from users.models import ChildModel, UserModel
from users.views import getUserIdByToken
from catalog.models import StoreModel,FolderModel, FileEntityModel, StoreUserModel, BlockModel
from store.models import  FileModel, FileSendModel, FileUserModel
from users.views import md5
# from classes.Metrika import MetricaApi








#загрузка
@csrf_exempt
def addFile(request):
    data = request.GET
    user = getUserIdByToken(request)

    file = FileModel.objects.create(
        title=request.FILES["file"].name,
        entity=request.FILES["file"]
    )
    FileUserModel.objects.create(
        user_id = user["id"],
        file_id=file.id
    )

    return  JsonResponse(file.getJson(), safe=False)

#отправка файла другому пользователю
@csrf_exempt
def sendFile(request):
    post = json.loads(request.body)
    user = getUserIdByToken(request)

    fileSendData = FileSendModel.objects.create(
        userFrom_id=user["id"],
        userToId=post["user"],
        file_id=post["file"],
    )

    return  JsonResponse(fileSendData.file.getJson(), safe=False)

#измение статуса отправления
@csrf_exempt
def changeStatusSendFile(request):
    post = json.loads(request.body)
    user = getUserIdByToken(request)

    alert = FileSendModel.objects.get(
        id=post["id"],
    )

    FileSendModel.objects.filter(
        id=post["id"],
    ).update(
        status=post["status"]
    )


    files = []
    if(post["status"] == "apply"):
        
        store = FileUserModel.objects.create(
            user_id=user["id"],
            file_id=alert.file.id,
        )
        files.append(alert.file.getJson())

    return  JsonResponse({
        "files" : files,
        "id" : alert.id}, safe=False)




#получить список файлов и оповещений
@csrf_exempt
def get(request):
    data = request.GET
    user = getUserIdByToken(request)


    result = []
    needResult = True


    if data["type"] == "files":
        needResult = False
        resultQS = FileUserModel.objects.filter(user_id=user["id"])
        for item in resultQS:
            result.append(item.file.getJson())

    
    if data["type"] == "alert":
        needResult = False
        resultQS = FileSendModel.objects.filter(userToId=user["id"],status="wait")
        for item in resultQS:
            result.append(item.getJson())

        resultQS = FileSendModel.objects.filter(userFrom_id=user["id"])
        for item in resultQS:
            tmp = item.getJson()
            tmp["user"] = UserModel.objects.get(id=item.userToId).getJson()
            tmp["self"] = True
            result.append(tmp)


        

    if data["type"] == "alert_self":
        resultQS = FileSendModel.objects.filter(userFrom_id=user["id"],status="wait")
        #FileSendModel.objects.filter(userToId=user["id"],status="wait").update(status="read")

    if needResult:
        for item in resultQS:
            result.append(item.getJson())

    return  JsonResponse(result, safe=False)
