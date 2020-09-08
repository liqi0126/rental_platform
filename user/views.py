from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from user.models import User, UserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import QueryDict, HttpResponse


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


class UsersList(APIView):
    def get(self, request, format=None):

        size = request.query_params.get('size', '10')
        try:
            size = int(size)
        except ValueError:
            return Response(f'invalid parameter size: {size}', status=400)

        page = request.query_params.get('page', '1')
        try:
            page = int(page)
        except ValueError:
            return Response(f'invalid parameter page: {page}', status=400)

        users = User.objects.all()[(page - 1) * size:page * size]
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


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

# def get_user_by_id(request, userId):
#     if request.method != 'GET':
#         response = HttpResponseNotAllowed(['GET'])
#         response.write(f'<p>Invalid Method {request.method}</p>')
#         return response
#
#     try:
#         user = User.objects.get(id=userId)
#     except:
#         response = HttpResponseNotFound()
#         response.write('<p>User doesn\'t exists</p>')
#         return response
#
#
#
#     return JsonResponse({
#         'username': user.username,
#         'create_at': user.created_at,
#         'address': user.address,
#         'email': user.email,
#         'phone': str(user.phone),
#         'is_renter': user.is_renter,
#     })
