from django.http import JsonResponse

from django.contrib.auth.hashers import make_password, check_password
from user.models import User
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
