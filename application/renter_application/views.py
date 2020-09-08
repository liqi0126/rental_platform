from django.shortcuts import render
from django.http import JsonResponse
from application.renter_application.models import RenterApplication
from equipment.models import Equipment
from user.models import User


# Create your views here.
def create_renter_application(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'require POST'})

    if not request.session['is_login']:
        return JsonResponse({'error': 'wrong status: is_login == False'})

    user_id = request.session['user_id']
    user_name = request.session['user_name']

    try:
        user = User.objects.get(username=user_name)
    except:
        return JsonResponse({'error': 'no such a user'})

    description = request.POST.get('description', '')

    new_renter_application = RenterApplication(User=user, discription=description)

    new_renter_application.save()

    return JsonResponse({'applicant': user_id})


def get_renter_application(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'require GET'})

    page = request.GET.get('page', '')

    renter_application_list = RenterApplication.all()
    renter_application_list_json = []
    for item in renter_application_list:
        renter_application_list_json.append({
            "id": item.id,
            "applicant_name": item.User.username,
            "status": item.status,
            "description": item.description
        })

    return JsonResponse(renter_application_list_json, safe=False)

