from django.shortcuts import render

def dashboard(request):
    if 'access_token' in request.session.keys():
        return render(request, 'dashboard/dashboard.html',{'status':'connected'})
    else:
        return render(request, 'dashboard/dashboard.html',{'status':'disconnected'})