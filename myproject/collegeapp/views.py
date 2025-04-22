from django.shortcuts import render,redirect
from collegeapp.models import Department,Teacher,User,Student,Staff
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
@never_cache
@login_required
def adminhome(request):
    if not request.user.is_superuser:
         return HttpResponse("unaouthorized",status=401)
    return render(request,'adminhome.html')


def adddep(request):
    if request.method == 'POST':
        d = request.POST['dep']
        x = Department.objects.create(Dep_Name=d)  # Corrected model name
        x.save()
        return HttpResponse("<script>alert('Added successfully');</script>")  # Fixed <script> tag
    else:
        return render(request, 'adddep.html')





def addteacher(request):
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        u = request.POST['uname']
        p = request.POST['password']
        ph = request.POST['phone']
        qu = request.POST['qual']
        d = request.POST['did']
        print(f,l,e,u,p,ph,qu,d)
        x = User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l,Usertype="Teacher")
        x.save()
        y = Teacher.objects.create(teach_id=x,Qualification=qu,phone=ph,dep_id_id=d)
        y.save()
        
        return HttpResponse("success")
    else:
        x = Department.objects.all()
        return render(request,'addteacher.html',{'data':x})
    
    
    
    
def mainhome(request):
    return render(request,'mainhome.html')


@never_cache
@login_required
def teacherhome(request):
    return render(request,'teacherhome.html')
# def teacherhome(request):
#     teach = request.session.get("teacher_id")  # Fetch teacher_id from session

#     if not teach:
#         return HttpResponse("Error: No teacher ID found in session")

#     try:
#         teacher = Teacher.objects.get(teach_id_id=teach)
#         user1 = teacher.user  # Assuming there's a related user model
#     except Teacher.DoesNotExist:
#         return HttpResponse("Error: Teacher not found")

#     return render(request, 'teacherhome.html', {"teacher": teacher, "user1": user1})



@never_cache
@login_required
def studenthome(request):
    return render(request,'studenthome.html')


  



def viewteacher(request):
    x = Teacher.objects.all()
    
    return render(request,'viewteacher.html',{'data':x})
    
#
    
    



from django.db import IntegrityError

def addstudent(request):
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        u = request.POST['uname']
        p = request.POST['password']
        ph = request.POST['phone']
        pl = request.POST['place']
        d = request.POST['did']
        
        # Check if the username already exists
        if User.objects.filter(username=u).exists():
            return HttpResponse("<script>alert('Username already exists, please choose another one.');</script>")
        
        try:
            # Create the new user
            x = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l, Usertype="Student", is_active=False)
            x.save()
            
            # Create the student record
            y = Student.objects.create(stud_id=x, Phone=ph, place=pl, dep_id_id=d)
            y.save()
            
            return HttpResponse("success")
        except IntegrityError:
            return HttpResponse("<script>alert('Error occurred, please try again.');</script>")
    else:
        x = Department.objects.all()
        return render(request, 'addstudent.html', {'data': x})
@never_cache
@login_required  
def viewstudents(request):
    x = Student.objects.all()
    
    return render(request,'viewstudent.html',{'data':x})





def admin_approve_student(request, aid):
    print(".......", aid)
    stud = Student.objects.get(id=aid)
    print("oke", stud)
    
    stud.stud_id.is_active = True  # ✅ Correct assignment
    stud.stud_id.save()  # ✅ Save the updated status in the database

    return redirect('viewstudents')  










def logouts(request):
    logout(request)
    return redirect('logins')  # Redirect to login page


@never_cache
@login_required

def logins(request):
    if request.method == "POST":
        un = request.POST.get('uname')  # Get username
        ps = request.POST.get('password')  # Get password

        print("Received username:", un, "Password:", ps)  # Debugging

        user = authenticate(request, username=un, password=ps)

        if user is not None:
            if user.is_superuser:
                return redirect('adminhome')
            elif getattr(user, 'Usertype', None) == "Teacher":
                login(request, user)
                request.session['teacher_id'] = user.id  # ✅ Store teacher_id properly
                return redirect('teacherhome')
            elif getattr(user, 'Usertype', None) == "Student" and user.is_active:
                login(request, user)
                request.session['student_id'] = user.id
                return redirect('studenthome')
        else:
            return HttpResponse('Invalid credentials')

    return render(request, "logins.html")





@never_cache
@login_required
def updateteacher(request):
    teach = request.session.get("teacher_id")

    if not teach:
        return HttpResponse("Error: Teacher ID not found in session.", status=400)

    try:
        teacher = Teacher.objects.get(teach_id_id=teach)
        user1 = User.objects.get(id=teach)
        return render(request, 'updateteacher.html', {"teacher": teacher, "user1": user1})
    except Teacher.DoesNotExist:
        return HttpResponse("Error: Teacher not found.", status=404)
    except User.DoesNotExist:
        return HttpResponse("Error: User not found.", status=404)


def updateteacher1(request, teacher_id):  # Change uid to teacher_id
    if request.method == "POST":
        try:
            teach = Teacher.objects.get(id=teacher_id)
            user1 = User.objects.get(id=teach.teach_id_id)

            # Update user details
            user1.first_name = request.POST['fname']
            user1.last_name = request.POST['lname']
            user1.email = request.POST['email']
            user1.save()

            # Update teacher details
            teach.phone = request.POST['phone']
            teach.Qualification = request.POST['qual']
            teach.save()

            return redirect('viewteacher')  # Redirect to teacher list page
        except Teacher.DoesNotExist:
            return HttpResponse("Teacher not found")
        except User.DoesNotExist:
            return HttpResponse("User not found")

    return HttpResponse("Invalid request")




@never_cache
@login_required
def staff_register(request):
    if request.method=='POST':
        n=request.POST.get('name')
        p=request.FILES.get('photo')
        Staff.objects.create(name=n,photo=p)
        return HttpResponse("success")
    else:
       return render(request,'staff_register.html')
   
   
def stafflist(request):
    staff=Staff.objects.all()
    return render(request,'staff_list.html',{'staff':staff})


# def student_dashboard(request):
#     # Get the logged-in student
#     student = Student.objects.get(stud_id=request.user)

#     # Filter teachers based on student department
#     teachers = Teacher.objects.filter(dep_id=student.dep_id)

#     return render(request, 'student_dashboard.html', {'teachers': teachers})


@login_required
@never_cache
def student_dashboard(request):
    # Check if the logged-in user is a student
    student = Student.objects.filter(stud_id=request.user).first()

    if not student:
        return render(request, 'student_dashboard.html', {'teachers': None, 'error': 'You are not registered as a student.'})

    # Get teachers of the same department as the student
    teachers = Teacher.objects.filter(dep_id=student.dep_id)

    return render(request, 'student_dashboard.html', {'teachers': teachers})
@login_required
@never_cache

def teacher_dashboard(request):
    teacher = Teacher.objects.select_related('dep_id').filter(teach_id=request.user).first()
    
    if not teacher:
        return render(request, 'teacher_dashbord.html', {
            'teacher': None,
            'error': 'You are not a registered teacher.'
        })

    students = Student.objects.select_related('stud_id', 'dep_id').filter(dep_id=teacher.dep_id)

    return render(request, 'teacher_dashbord.html', {
        'teacher': teacher,
        'students': students
    })



