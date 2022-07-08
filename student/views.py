from django.forms import ValidationError
from django.shortcuts import render,redirect
from django.urls import reverse
from regex import P


from student.models import Student
from .forms import StudentRegistrationForm,EditStudentProfileForm

def students(request):
    students = Student.objects.all()
    return render(request, 'student/student.html',{'students':students})

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            model = form.save()
            return redirect(reverse('student_profile',args=[model.id]))
        else:
            return render(request, 'student/registration.html',{'form':form})
    elif request.method == 'GET':
        form = StudentRegistrationForm()
        return render(request, 'student/registration.html',{'form':form})
    
def student_profile(request,id):
    student = Student.objects.get(pk=id)
    return render(request, 'student/student_profile.html',{'student':student})

def edit_student_profile(request,id):
    student = Student.objects.get(pk=id)
    if request.method == 'POST':
        form = EditStudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            instance = form.save()
            if form.has_changed():
                if 'hot_lunch' in form.changed_data:
                    pass
                #Create invoice for lunch
                if 'transport' in form.changed_data:
                    #create invoice for transport
                    pass
                return redirect(reverse('student_profile', args=[instance.id]))
            else:
                return redirect(reverse('student_profile', args=[instance.id]))
        else:
            return render(request,'student/edit_student_profile.html',{'form':form,'student':student})
    if request.method =='GET':
        form = EditStudentProfileForm(instance=student)
        return render(request,'student/edit_student_profile.html',{'form':form,'student':student})
