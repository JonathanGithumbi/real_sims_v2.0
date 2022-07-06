from django.shortcuts import render

def notifications(request):
    return render(request, 'notification/notifications.html')