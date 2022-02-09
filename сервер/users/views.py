import json
import datetime
import hashlib
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from users.models import ChildModel, UserModel
from history.models import HistoryModel, QueryGroupToChildModel, QueriesModel, QueriesGroupModel



#регистрация
@csrf_exempt
def registration(request):
    #получаем параметры post запроса
    post = json.loads(request.body)


    login = post['email'].lower()
    name = post['name']
    password = post['password']
    #email = post['email'].lower()


    #создаем пользователя
    userQS = UserModel.objects.create(
        login=login,
        name=name,
        password=password,
        #email=email,
    )


    return JsonResponse(userQS.getJson())



#авторизация
@csrf_exempt
def login(request):

    #получаем параметры post запроса
    post = json.loads(request.body)

    login = post['login'].lower()
    password = post['password']
     #формируем токен из логина
    token = getToken(login)

    #ЗАПРОС В БАЗУ ДАННЫХ
    usersQS = UserModel.objects.filter(login=login,password=password)

    #если пользователь прошел авторизацию
    if usersQS.count() > 0:
        #меняем токен
        UserModel.objects.filter(login=login, password=password).update(token=token)

        #новый токен отправляем клиенту и сетим в куки
        response = JsonResponse({
            'token': token
        })
        set_cookie(response,"token",
                            token)


    #иначе ошибка 401 (отказ в доступе)
    else:
        response = JsonResponse({
            'error': 1,
            'code': 401
        })


    return response



@csrf_exempt
#выход пользователя
def logout(request):
    user = getUserIdByToken(request)


    response = JsonResponse({
            'status': True
        })
    #меняем куки на случайную запись


        #ЗАПРОС В БАЗУ ДАННЫХ
    usersQS = UserModel.objects.filter(id=user["id"]).update(token="111111111")


    return response



#метод для проверки существует ли пользователь , -1 если нет
def checkLogin(request):
    return JsonResponse({
     'status' : getUserIdByToken(request) != -1
    })

def getCurrentUser(request):
    user = getUserIdByToken(request)
    if not user == -1:
        return JsonResponse(user)
    else:
        return JsonResponse({
        'status' : false
        })
# def get(request):
#     usersQS = UserModel.objects.all()
#     users = []
#     for u in usersQS:
#         users.append(u.getJson())

#     return JsonResponse(users,safe=False )


def getDetail(request):
    post = json.load(request)
    usersQS = UserModel.objects.get(id=post["id"])
    users = []
    for u in usersQS:
        users.append(u.getJson())

    return JsonResponse(users[0],safe=False )





def getUserIdByToken(request):

    result = -1
    if "token" in request.COOKIES:
        usersQS = UserModel.objects.filter(token=request.COOKIES["token"])
        users = []
        if len(usersQS) > 0:
            return usersQS[0].getJson()

    return result



def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%d-%m-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None
    )

def md5(str):
    return hashlib.md5(
        (str).lower().encode()
    ).hexdigest()


#метод для формирования уникального токена
def getToken(login):
    return md5((login + str(datetime.datetime.now())))