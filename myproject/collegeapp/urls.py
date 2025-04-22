from django.urls import path
from collegeapp import views
urlpatterns = [
    path('',views.mainhome,name='mainhome'),
    path('adminhome',views.adminhome,name='adminhome'),

   path('login/',views.logins,name='logins'),
     path('studenthome/',views.studenthome, name='studenthome'),
    path('teacherhome/',views.teacherhome, name='teacherhome'),
   path('logout/',views.logouts,name='logouts'),
    
    path('addep/',views.adddep,name='adddep'),
     path('addteacher/',views.addteacher,name='addteacher'),
     path('viewteacher/',views.viewteacher,name='viewteacher'),
     path('updateteacher/',views.updateteacher,name='updateteacher'),
    path('updateteacher1/<int:teacher_id>',views.updateteacher1,name='updateteacher1'),
     path('addstudent/',views.addstudent,name='addstudent'),
     path('viewstudents/',views.viewstudents,name='viewstudents'),
     path('admin_approve_student/<int:aid>',views.admin_approve_student,name='admin_approve_student'),
     path('staff_register',views.staff_register,name='staff_register'),
     path('stafflist/',views.stafflist,name='stafflist'),
      path('std_teacher', views.student_dashboard, name='student_dashboard'),
      path('tech_student',views.teacher_dashboard,name='teacher_dashboard'),
     
          
    
]
