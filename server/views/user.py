from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from server.models import User


def user_login(request):
    if request.method == 'GET':
        return JsonResponse({'success': False,
                                 'error': {
                                     'code': 405,
                                     'message': 'Method Not Allowed'
                            }})
    data = request.POST
    if data.get('fb_id', False) and authenticate(data['fb_id']) is not None:
        login(request, authenticate(data['fb_id']))
        return JsonResponse({'success': True})
    else:
        try:
            user = User.objects.create_user(data['fb_id'], data['fb_name'], data['fb_token'], data['fb_token_exp'], data['email'], data['telephone'], data['birth_date'])
            user.save()
        except Exception:
            return JsonResponse({'success': False,
                                 'error': {
                                     'code': 1000,
                                     'message': 'An error has occurred while creating a views account.'
                                 }})
        login(request, user)
        return JsonResponse({'success': True})


def user_logout(request):
    logout(request)
    return JsonResponse({'success': True})