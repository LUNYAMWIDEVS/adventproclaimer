import datetime
import json
import random
import uuid
from django.urls import reverse
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Course, Announcement, Assignment, Submission, Material, Faculty, Department
from django.template.defaulttags import register
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from .forms import AnnouncementForm, AssignmentForm, MaterialForm,SplitMaterialsForm,ScheduleMaterialForm
from .helpers import upload_file,split_pdf
from messenger.tasks.whatsapp_manager import send_batch_whatsapp_text
from datetime import timedelta, date, datetime, timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from django.core.exceptions import ValidationError

def is_student_authorised(request, code):
    # import pdb;pdb.set_trace()
    course = Course.objects.get(code=code)
    if request.session.get('student_id') and course in Student.objects.get(student_id=request.session['student_id']).course.all():
        return True
    else:
        return False


def is_faculty_authorised(request, code):
    if request.session.get('faculty_id') and code in Course.objects.filter(faculty_id=request.session['faculty_id']).values_list('code', flat=True):
        return True
    else:
        return False


# Login page for both student and faculty
def std_login(request):

    try:
        # If the user is already logged in, redirect to the course page
        
        redirect_to = request.POST.get('next', request.GET.get('next', None))
        if redirect_to:
            return HttpResponseRedirect(redirect_to)
        
        # Check if there's a stored URL in the session
        next_url = request.session.get('next')
        if next_url:
            del request.session['next']  # Remove the stored URL from the session

        if request.session.get('student_id'):
            return redirect('/my/')
           
        elif request.session.get('faculty_id'):
        
            return redirect('/facultyCourses/')
        else:
            # If the user is not logged in, display the login page
            if request.method == 'POST':
                id = request.POST["id"]
                password = (request.POST["password"])
                try:
                    # Checks if id matches any student, if no match found, checks if id matches any faculty
                    if Student.objects.filter(student_id=id).exists():
                        student = Student.objects.get(student_id=id)
                        if str(student.student_id) == id and str(student.password) == password:

                            request.session['student_id'] = id
                            return redirect('myCourses')
                        else:
                            # id matches but student password is wrong
                            messages.error(
                                request, 'Incorrect password. Please try again.', extra_tags='alert')
                            return redirect('std_login')

                    else:
                        # Checks if id matches any faculty
                        if Faculty.objects.filter(faculty_id=id).exists():
                            faculty = Faculty.objects.get(faculty_id=id)
                            if str(faculty.faculty_id) == id and str(faculty.password) == password:
                                request.session['faculty_id'] = id
                                return redirect('facultyCourses')
                               
                            else:
                                # id matches but faculty password is wrong
                                messages.error(
                                    request, 'Incorrect password. Please try again.', extra_tags='alert')
                                return redirect('std_login')
                        else:
                            # id does not match any student or faculty
                            messages.error(
                                request, 'Incorrect user id. Please try again.', extra_tags='alert')
                            return redirect('std_login')
                except:
                    # id does not match any student or faculty
                    messages.error(
                        request, 'Invalid login credentials.', extra_tags='alert')
                    return redirect('std_login')

            else:
                return render(request, 'login_page.html')
    except:
        return render(request, 'error.html')


# Clears the session on logout
def std_logout(request):
    request.session.flush()
    return redirect('std_login')


# Display all courses (student view)
def myCourses(request):
    try:
        if request.session.get('student_id'):
            student = Student.objects.get(
                student_id=request.session['student_id'])
            courses = student.course.all()
            faculty = student.course.all().values_list('faculty_id', flat=True)

            context = {
                'courses': courses,
                'student': student,
                'faculty': faculty
            }

            return render(request, 'main/myCourses.html', context)
        else:
            return redirect('std_login')
    except:
        return render(request, 'error.html')


# Display all courses (faculty view)
def facultyCourses(request):
    try:
        if request.session['faculty_id']:
            faculty = Faculty.objects.get(
                faculty_id=request.session['faculty_id'])
            courses = Course.objects.filter(
                faculty_id=request.session['faculty_id'])
            # Student count of each course to show on the faculty page
            studentCount = Course.objects.all().annotate(student_count=Count('students'))

            studentCountDict = {}

            for course in studentCount:
                studentCountDict[course.code] = course.student_count

            @register.filter
            def get_item(dictionary, course_code):
                return dictionary.get(course_code)

            context = {
                'courses': courses,
                'faculty': faculty,
                'studentCount': studentCountDict
            }

            return render(request, 'main/facultyCourses.html', context)

        else:
            return redirect('std_login')
    except:

        return redirect('std_login')


# Particular course page (student view)
def course_page(request, code):
    try:
        course = Course.objects.get(code=code)
        if is_student_authorised(request, code):
            try:
                announcements = Announcement.objects.filter(course_code=course)
                assignments = Assignment.objects.filter(
                    course_code=course.code)
                materials = Material.objects.filter(course_code=course.code)

            except:
                announcements = None
                assignments = None
                materials = None

            context = {
                'course': course,
                'announcements': announcements,
                'assignments': assignments[:3],
                'materials': materials,
                'student': Student.objects.get(student_id=request.session['student_id'])
            }

            return render(request, 'main/course.html', context)

        else:
            return redirect('std_login')
    except:
        return render(request, 'error.html')


# Particular course page (faculty view)
def course_page_faculty(request, code):
    course = Course.objects.get(code=code)
    if request.session.get('faculty_id'):
        try:
            announcements = Announcement.objects.filter(course_code=course)
            assignments = Assignment.objects.filter(
                course_code=course.code)
            materials = Material.objects.filter(course_code=course.code)
            studentCount = Student.objects.filter(course=course).count()

        except:
            announcements = None
            assignments = None
            materials = None

        context = {
            'course': course,
            'announcements': announcements,
            'assignments': assignments[:3],
            'materials': materials,
            'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
            'studentCount': studentCount
        }

        return render(request, 'main/faculty_course.html', context)
    else:
        return redirect('std_login')


def error(request):
    return render(request, 'error.html')


# Display user profile(student & faculty)
def profile(request, id):
    try:
        if request.session['student_id'] == id:
            student = Student.objects.get(student_id=id)
            return render(request, 'main/profile.html', {'student': student})
        else:
            return redirect('std_login')
    except:
        try:
            if request.session['faculty_id'] == id:
                faculty = Faculty.objects.get(faculty_id=id)
                return render(request, 'main/faculty_profile.html', {'faculty': faculty})
            else:
                return redirect('std_login')
        except:
            return render(request, 'error.html')


def addAnnouncement(request, code):
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            form = AnnouncementForm(request.POST)
            form.instance.course_code = Course.objects.get(code=code)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Announcement added successfully.')
                return redirect('/faculty/' + str(code))
        else:
            form = AnnouncementForm()
        return render(request, 'main/announcement.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
    else:
        return redirect('std_login')


def deleteAnnouncement(request, code, id):
    if is_faculty_authorised(request, code):
        try:
            announcement = Announcement.objects.get(course_code=code, id=id)
            announcement.delete()
            messages.warning(request, 'Announcement deleted successfully.')
            return redirect('/faculty/' + str(code))
        except:
            return redirect('/faculty/' + str(code))
    else:
        return redirect('std_login')


def editAnnouncement(request, code, id):
    if is_faculty_authorised(request, code):
        announcement = Announcement.objects.get(course_code_id=code, id=id)
        form = AnnouncementForm(instance=announcement)
        context = {
            'announcement': announcement,
            'course': Course.objects.get(code=code),
            'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
            'form': form
        }
        return render(request, 'main/update-announcement.html', context)
    else:
        return redirect('std_login')


def updateAnnouncement(request, code, id):
    if is_faculty_authorised(request, code):
        try:
            announcement = Announcement.objects.get(course_code_id=code, id=id)
            form = AnnouncementForm(request.POST, instance=announcement)
            if form.is_valid():
                form.save()
                messages.info(request, 'Announcement updated successfully.')
                return redirect('/faculty/' + str(code))
        except:
            return redirect('/faculty/' + str(code))

    else:
        return redirect('std_login')


def addAssignment(request, code):
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            form = AssignmentForm(request.POST, request.FILES)
            form.instance.course_code = Course.objects.get(code=code)
            if form.is_valid():
                form.save()
                messages.success(request, 'Assignment added successfully.')
                return redirect('/faculty/' + str(code))
        else:
            form = AssignmentForm()
        return render(request, 'main/assignment.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
    else:
        return redirect('std_login')


def assignmentPage(request, code, id):
    course = Course.objects.get(code=code)
    if is_student_authorised(request, code):
        assignment = Assignment.objects.get(course_code=course.code, id=id)
        try:

            submission = Submission.objects.get(assignment=assignment, student=Student.objects.get(
                student_id=request.session['student_id']))

            context = {
                'assignment': assignment,
                'course': course,
                'submission': submission,
                'time': datetime.now(),
                'student': Student.objects.get(student_id=request.session['student_id']),
                'courses': Student.objects.get(student_id=request.session['student_id']).course.all()
            }

            return render(request, 'main/assignment-portal.html', context)

        except:
            submission = None

        context = {
            'assignment': assignment,
            'course': course,
            'submission': submission,
            'time': datetime.now(),
            'student': Student.objects.get(student_id=request.session['student_id']),
            'courses': Student.objects.get(student_id=request.session['student_id']).course.all()
        }

        return render(request, 'main/assignment-portal.html', context)
    else:
        request.session['next'] = reverse('assignment_page', args=(code, id))
        return redirect('std_login')


def allAssignments(request, code):
    if is_faculty_authorised(request, code):
        course = Course.objects.get(code=code)
        assignments = Assignment.objects.filter(course_code=course)
        studentCount = Student.objects.filter(course=course).count()

        context = {
            'assignments': assignments,
            'course': course,
            'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
            'studentCount': studentCount

        }
        return render(request, 'main/all-assignments.html', context)
    else:
        return redirect('std_login')


def allAssignmentsSTD(request, code):
    if is_student_authorised(request, code):
        course = Course.objects.get(code=code)
        assignments = Assignment.objects.filter(course_code=course)
        context = {
            'assignments': assignments,
            'course': course,
            'student': Student.objects.get(student_id=request.session['student_id']),

        }
        return render(request, 'main/all-assignments-std.html', context)
    else:
        return redirect('std_login')


def addSubmission(request, code, id):
    try:
        course = Course.objects.get(code=code)
        if is_student_authorised(request, code):
            # check if assignment is open
            assignment = Assignment.objects.get(course_code=course.code, id=id)
            if assignment.deadline < datetime.datetime.now():

                return redirect('/assignment/' + str(code) + '/' + str(id))

            if request.method == 'POST':
                assignment = Assignment.objects.get(
                    course_code=course.code, id=id)
                submission = Submission(assignment=assignment, student=Student.objects.get(
                    student_id=request.session['student_id']), summary=request.POST.get('summary'),)
                submission.status = 'Submitted'
                submission.save()
                return HttpResponseRedirect(request.path_info)
            else:
                assignment = Assignment.objects.get(
                    course_code=course.code, id=id)
                submission = Submission.objects.get(assignment=assignment, student=Student.objects.get(
                    student_id=request.session['student_id']))
                context = {
                    'assignment': assignment,
                    'course': course,
                    'submission': submission,
                    'time': datetime.datetime.now(),
                    'student': Student.objects.get(student_id=request.session['student_id']),
                    'courses': Student.objects.get(student_id=request.session['student_id']).course.all()
                }

                return render(request, 'main/assignment-portal.html', context)
        else:
            return redirect('std_login')
    except:
        return HttpResponseRedirect(request.path_info)


def viewSubmission(request, code, id):
    course = Course.objects.get(code=code)
    if is_faculty_authorised(request, code):
        try:
            assignment = Assignment.objects.get(course_code_id=code, id=id)
            submissions = Submission.objects.filter(
                assignment_id=assignment.id)

            context = {
                'course': course,
                'submissions': submissions,
                'assignment': assignment,
                'totalStudents': len(Student.objects.filter(course=course)),
                'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
                'courses': Course.objects.filter(faculty_id=request.session['faculty_id'])
            }

            return render(request, 'main/assignment-view.html', context)

        except:
            return redirect('/faculty/' + str(code))
    else:
        return redirect('std_login')


def gradeSubmission(request, code, id, sub_id):
    try:
        course = Course.objects.get(code=code)
        if is_faculty_authorised(request, code):
            if request.method == 'POST':
                assignment = Assignment.objects.get(course_code_id=code, id=id)
                submissions = Submission.objects.filter(
                    assignment_id=assignment.id)
                submission = Submission.objects.get(
                    assignment_id=id, id=sub_id)
                submission.marks = request.POST['marks']
                if request.POST['marks'] == 0:
                    submission.marks = 0
                submission.save()
                return HttpResponseRedirect(request.path_info)
            else:
                assignment = Assignment.objects.get(course_code_id=code, id=id)
                submissions = Submission.objects.filter(
                    assignment_id=assignment.id)
                submission = Submission.objects.get(
                    assignment_id=id, id=sub_id)

                context = {
                    'course': course,
                    'submissions': submissions,
                    'assignment': assignment,
                    'totalStudents': len(Student.objects.filter(course=course)),
                    'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
                    'courses': Course.objects.filter(faculty_id=request.session['faculty_id'])
                }

                return render(request, 'main/assignment-view.html', context)

        else:
            return redirect('std_login')
    except:
        return redirect('/error/')


def addCourseMaterial(request, code):
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            form = MaterialForm(request.POST, request.FILES)
            form.instance.course_code = Course.objects.get(code=code)
            file_id = None
            if form.is_valid():
                file_id = upload_file(form.files['book'])    
                form.instance.file = file_id
                form.save()
                messages.success(request, 'New course material added')
                return redirect('/faculty/' + str(code))
            else:
                return render(request, 'main/course-material.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
        else:
            form = MaterialForm()
            return render(request, 'main/course-material.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
    else:
        return redirect('std_login')

def splitCourseMaterial(request, code,id):
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            form = SplitMaterialsForm(request.POST or None)
            if form.is_valid():
                material = get_object_or_404(Material,id=id)
                split_pdf(file_id=material.file,steps=int(request.POST.get('no_pages'))) 
                messages.success(request, 'Material Successfully split')
                return redirect('/faculty/' + str(code))
            else:
                return render(request, 'main/split-material.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
        else:
            form = SplitMaterialsForm()
            return render(request, 'main/split-material.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
    else:
        return redirect('std_login')

def scheduleCourseMaterial(request, code, id):
    error = None
    gmt_offset = timedelta(hours=+3)
    desired_timezone = timezone(gmt_offset)

    
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            form = ScheduleMaterialForm(request.POST or None)
            if form.is_valid():
                material = get_object_or_404(Material,id=id)
                assigments =material.assignments.all()
                student = Student.objects.get(student_id=request.POST.get('user'))
                morning_flag = True
                for index,assignment in enumerate(assigments):
                    # TODO: order the assignments
                    # TODO: ensure the loop is not one assignment per day
                    schedule = None
                    relative_date = datetime.now(tz=desired_timezone) + timedelta(days=index+1)
                    random_minutes = random.randint(1,2)
                    random_hour = None
                    time_period = None
                    if morning_flag:
                        random_hour = random.randint(1, 2)  # morning devotion
                        time_period = "Morning"
                    else:
                        random_hour = random.randint(1, 2)  # evening devotion
                        time_period = "Evening"

                    morning_flag = not morning_flag  # Toggle the flag
                    schedule, _ = CrontabSchedule.objects.get_or_create(
                        minute=f'{random_minutes}',
                        hour=f'{random_hour}',
                        day_of_week=f'*',
                        day_of_month=f'{relative_date.day}',
                        month_of_year=f'{relative_date.month}',
                    )
                    try:
                        # import pdb;pdb.set_trace()
                        # print(form['course_format'].value)
                        # print(request.POST.get('course_format'))
                        
                        if request.POST.get('course_format') == 'W':
                            # import pdb;pdb.set_trace()
                            PeriodicTask.objects.update_or_create(
                                crontab=schedule,                  # we created this above.
                                name=f'Send Assignment {time_period} - {student.name} - {assignment.id}--{index}',          # simply describes this periodic task.
                                task='messenger.tasks.whatsapp_manager.send_batch_whatsapp_text',  # name of task.
                                args=json.dumps([[student.phone_number], [student.name], assignment.description]),
                            )
                        if request.POST.get('course_format') == 'E':
                            PeriodicTask.objects.update_or_create(
                                crontab=schedule,                  # we created this above.
                                name=f'Send Assignment {time_period} - {student.name} - {assignment.id}--{index}',          # simply describes this periodic task.
                                task='messenger.tasks.email_manager.send_newsletter',  # name of task.
                                args=json.dumps([student.name, student.email,assignment.description]),
                            )
                        
                    except ValidationError as err:
                        error=err

                    
                if error:        
                    messages.error(request, str(error))
                else:
                    messages.success(request, 'Material Successfully scheduled')    
                
                return redirect('/faculty/' + str(code))
            else:
                return render(request, 'main/schedule-material.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
        else:
            form = ScheduleMaterialForm()
            return render(request, 'main/schedule-material.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']), 'form': form})
    else:
        return redirect('std_login')

def deleteCourseMaterial(request, code, id):
    if is_faculty_authorised(request, code):
        course = Course.objects.get(code=code)
        course_material = Material.objects.get(course_code=course, id=id)
        course_material.delete()
        messages.warning(request, 'Course material deleted')
        return redirect('/faculty/' + str(code))
    else:
        return redirect('std_login')


def courses(request):
    if request.session.get('student_id') or request.session.get('faculty_id'):

        courses = Course.objects.all()
        if request.session.get('student_id'):
            student = Student.objects.get(
                student_id=request.session['student_id'])
        else:
            student = None
        if request.session.get('faculty_id'):
            faculty = Faculty.objects.get(
                faculty_id=request.session['faculty_id'])
        else:
            faculty = None

        enrolled = student.course.all() if student else None
        accessed = Course.objects.filter(
            faculty_id=faculty.faculty_id) if faculty else None

        context = {
            'faculty': faculty,
            'courses': courses,
            'student': student,
            'enrolled': enrolled,
            'accessed': accessed
        }

        return render(request, 'main/all-courses.html', context)

    else:
        return redirect('std_login')


def departments(request):
    if request.session.get('student_id') or request.session.get('faculty_id'):
        departments = Department.objects.all()
        if request.session.get('student_id'):
            student = Student.objects.get(
                student_id=request.session['student_id'])
        else:
            student = None
        if request.session.get('faculty_id'):
            faculty = Faculty.objects.get(
                faculty_id=request.session['faculty_id'])
        else:
            faculty = None
        context = {
            'faculty': faculty,
            'student': student,
            'deps': departments
        }

        return render(request, 'main/departments.html', context)

    else:
        return redirect('std_login')


def access(request, code):
    if request.session.get('student_id'):
        course = Course.objects.get(code=code)
        student = Student.objects.get(student_id=request.session['student_id'])
        if request.method == 'POST':
            if (request.POST['key']) == str(course.studentKey):
                student.course.add(course)
                student.save()
                return redirect('/my/')
            else:
                messages.error(request, 'Invalid key')
                return HttpResponseRedirect(request.path_info)
        else:
            return render(request, 'main/access.html', {'course': course, 'student': student})

    else:
        return redirect('std_login')


def search(request):
    if request.session.get('student_id') or request.session.get('faculty_id'):
        if request.method == 'GET' and request.GET['q']:
            q = request.GET['q']
            courses = Course.objects.filter(Q(code__icontains=q) | Q(
                name__icontains=q) | Q(faculty__name__icontains=q))

            if request.session.get('student_id'):
                student = Student.objects.get(
                    student_id=request.session['student_id'])
            else:
                student = None
            if request.session.get('faculty_id'):
                faculty = Faculty.objects.get(
                    faculty_id=request.session['faculty_id'])
            else:
                faculty = None
            enrolled = student.course.all() if student else None
            accessed = Course.objects.filter(
                faculty_id=faculty.faculty_id) if faculty else None

            context = {
                'courses': courses,
                'faculty': faculty,
                'student': student,
                'enrolled': enrolled,
                'accessed': accessed,
                'q': q
            }
            return render(request, 'main/search.html', context)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('std_login')


def changePasswordPrompt(request):
    if request.session.get('student_id'):
        student = Student.objects.get(student_id=request.session['student_id'])
        return render(request, 'main/changePassword.html', {'student': student})
    elif request.session.get('faculty_id'):
        faculty = Faculty.objects.get(faculty_id=request.session['faculty_id'])
        return render(request, 'main/changePasswordFaculty.html', {'faculty': faculty})
    else:
        return redirect('std_login')


def changePhotoPrompt(request):
    if request.session.get('student_id'):
        student = Student.objects.get(student_id=request.session['student_id'])
        return render(request, 'main/changePhoto.html', {'student': student})
    elif request.session.get('faculty_id'):
        faculty = Faculty.objects.get(faculty_id=request.session['faculty_id'])
        return render(request, 'main/changePhotoFaculty.html', {'faculty': faculty})
    else:
        return redirect('std_login')


def changePassword(request):
    if request.session.get('student_id'):
        student = Student.objects.get(
            student_id=request.session['student_id'])
        if request.method == 'POST':
            if student.password == request.POST['oldPassword']:
                # New and confirm password check is done in the client side
                student.password = request.POST['newPassword']
                student.save()
                messages.success(request, 'Password was changed successfully')
                return redirect('/profile/' + str(student.student_id))
            else:
                messages.error(
                    request, 'Password is incorrect. Please try again')
                return redirect('/changePassword/')
        else:
            return render(request, 'main/changePassword.html', {'student': student})
    else:
        return redirect('std_login')


def changePasswordFaculty(request):
    if request.session.get('faculty_id'):
        faculty = Faculty.objects.get(
            faculty_id=request.session['faculty_id'])
        if request.method == 'POST':
            if faculty.password == request.POST['oldPassword']:
                # New and confirm password check is done in the client side
                faculty.password = request.POST['newPassword']
                faculty.save()
                messages.success(request, 'Password was changed successfully')
                return redirect('/facultyProfile/' + str(faculty.faculty_id))
            else:
                print('error')
                messages.error(
                    request, 'Password is incorrect. Please try again')
                return redirect('/changePasswordFaculty/')
        else:
            print(faculty)
            return render(request, 'main/changePasswordFaculty.html', {'faculty': faculty})
    else:
        return redirect('std_login')


def changePhoto(request):
    if request.session.get('student_id'):
        student = Student.objects.get(
            student_id=request.session['student_id'])
        if request.method == 'POST':
            if request.FILES['photo']:
                student.photo = request.FILES['photo']
                student.save()
                messages.success(request, 'Photo was changed successfully')
                return redirect('/profile/' + str(student.student_id))
            else:
                messages.error(
                    request, 'Please select a photo')
                return redirect('/changePhoto/')
        else:
            return render(request, 'main/changePhoto.html', {'student': student})
    else:
        return redirect('std_login')


def changePhotoFaculty(request):
    if request.session.get('faculty_id'):
        faculty = Faculty.objects.get(
            faculty_id=request.session['faculty_id'])
        if request.method == 'POST':
            if request.FILES['photo']:
                faculty.photo = request.FILES['photo']
                faculty.save()
                messages.success(request, 'Photo was changed successfully')
                return redirect('/facultyProfile/' + str(faculty.faculty_id))
            else:
                messages.error(
                    request, 'Please select a photo')
                return redirect('/changePhotoFaculty/')
        else:
            return render(request, 'main/changePhotoFaculty.html', {'faculty': faculty})
    else:
        return redirect('std_login')


def guestStudent(request):
    request.session.flush()
    try:
        student = Student.objects.get(name='Guest Student')
        request.session['student_id'] = str(student.student_id)
        return redirect('myCourses')
    except:
        return redirect('std_login')


def guestFaculty(request):
    request.session.flush()
    try:
        faculty = Faculty.objects.get(name='Guest Faculty')
        request.session['faculty_id'] = str(faculty.faculty_id)
        return redirect('facultyCourses')
    except:
        return redirect('std_login')