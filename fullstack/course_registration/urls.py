from django.urls import path 
from . import views 
urlpatterns = [ 
path('add_student/', views.add_student, name='add_student'), 
path('add_course/', views.add_course, name='add_course'),
path('register/', views.register_student, name='register_student'), 
path('courses/', views.course_registration, name='course_registration'), 
path('students_list/<int:course_id>/', views.students_list, name='students_list'), 
path('students/', views.StudentListView.as_view(), name='student_list'), 
path('student/<int:pk>/', views.StudentDetailView.as_view(), 
name='student_detail'), 
]