from django.shortcuts import render
from django.http import JsonResponse

from equipment.models import Equipment
from user.models import User
# Create your views here.


def create_new_equipment(request):

    if request.method != 'POST':
        return JsonResponse({'error': 'require POST'})

    name = request.POST.get('name', '')
    address = request.POST.get('address', '')
    email = request.POST.get('email', '')
    phone = request.POST.get('phone', '')
    description = request.POST.get('description', '')

    owner_name = request.POST.get('owner', '')
    try:
        owner = User.objects.get(username=owner_name)
    except:
        return JsonResponse({'error': 'no such a user'})

    equipment = Equipment(name=name, address=address, email=email, phone=phone, description=description, owner=owner)

    equipment.save()

    return JsonResponse({'equipment': name})
