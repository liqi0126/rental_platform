from django.http import JsonResponse
from user.models import User
from user.serializers import UserSerializer

from rest_framework.views import APIView


from django.http import QueryDict, HttpResponse


from rest_framework import generics
# Create your views here.


def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'require POST'})

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    if username == '':
        return JsonResponse({'error': 'no such a user'})

    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({'error': 'no such a user'})

    if not check_password(password, user.password):
        return JsonResponse({'error': 'password is wrong'})

    if 'is_login' in request.session:
        return JsonResponse({'error': 'has logged in'})

    request.session['is_login'] = True
    request.session['user_id'] = user.id
    request.session['user_name'] = username
    return JsonResponse({'user': username})


class register(APIView):
    def patch(self, request, format=None):

        dict = QueryDict(request.body)
        username = dict.get('username', '')
        password = dict.get('password', '')
        address = dict.get('address', '')
        email = dict.get('email', '')
        phone = dict.get('phone', '')
        is_renter = dict.get('is_renter', False)

        if username == '' or password == '' or address == '' or email == '' or phone == '':
            return HttpResponse(400)

        user = User(username=username, password=password, address=address, email=email, phone=phone,
                    is_renter=is_renter)
        user.save()

        return JsonResponse({'message': 'OK'})


# high level API
class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

