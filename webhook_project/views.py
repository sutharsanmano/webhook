import json
import requests
from django.http import JsonResponse
from account.models import Account
from destination.models import Destination
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def incoming_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        app_secret_token = request.headers.get('CL-X-TOKEN')
        
        if app_secret_token:
            try:
                account = Account.objects.get(app_secret_token=app_secret_token)
                destinations = Destination.objects.filter(account=account)
                
                for destination in destinations:
                    if destination.http_method == 'GET':
                        response = requests.get(destination.url, params=data, headers=destination.headers)
                    else:
                        response = requests.request(destination.http_method, destination.url, json=data, headers=destination.headers)
                    # Handle the response if needed
                    
                return JsonResponse({'message': 'Data sent to destinations successfully'})
            except Account.DoesNotExist:
                return JsonResponse({'message': 'Unauthenticated'}, status=401)
        else:
            return JsonResponse({'message': 'Unauthorized'}, status=401)
    else:
        return JsonResponse({'message': 'Invalid Data'}, status=400)
