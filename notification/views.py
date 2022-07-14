from django.shortcuts import render

def notifications(request):
    return render(request, 'notification/notifications.html')

def notification_detail(request, id):
    return render(request, 'notification/notification_detail.html')

