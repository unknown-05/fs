from .forms import StudentForm, CourseForm
from .models import Student, Course
from django.shortcuts import render, redirect, get_object_or_404

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a view that lists all students
            course_id = request.POST.get('course_id')
            if course_id:
                return redirect('students_list', course_id=course_id)
            else:
                return redirect('course_registration')  # Fallback URL
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_registration')
    else:
        form = CourseForm()
    return render(request, 'add_course.html', {'form': form})

def register_student(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        course_id = request.POST.get('course_id')
        # Validate that both student_name and course_id are provided
        if not student_name or not course_id:
            return render(request, 'register_student.html', {
                'courses': Course.objects.all(),
                'error_message': 'Please provide both student name and select a course.'
            })
        try:
            # Retrieve the course based on course_id or return 404 if not found
            course = get_object_or_404(Course, pk=course_id)
            # Check if the student already exists in the database
            student = Student.objects.filter(name=student_name).first()
            if not student:
                # If the student does not exist, return an error message
                return render(request, 'register_student.html', {
                    'courses': Course.objects.all(),
                    'error_message': 'Student does not exist in the database.'
                })
            # Add the student to the course
            course.students.add(student)
            return redirect('course_registration')
        except Course.DoesNotExist:
            return render(request, 'register_student.html', {
                'courses': Course.objects.all(),
                'error_message': 'Invalid course ID. Please select a valid course.'
            })
    # If not a POST request, render the registration form with all courses
    return render(request, 'register_student.html', {'courses': Course.objects.all()})

def course_registration(request):
    courses = Course.objects.all()
    return render(request, 'course_registration.html', {'courses': courses})

def students_list(request, course_id):
    # Retrieve the course based on course_id or return 404 if not found
    course = get_object_or_404(Course, course_id=course_id)
    # Retrieve the students associated with the course
    students = course.students.all()
    return render(request, 'students_list.html', {'course': course, 'students': students})

from .models import Student
from django.views.generic import ListView, DetailView

class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'

class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object  # Get the student object
        context['date_of_birth'] = student.date_of_birth
        context['email'] = student.email
        # Add more fields as needed
        return context
