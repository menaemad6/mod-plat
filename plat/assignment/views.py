from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import random
from django.shortcuts import get_object_or_404
from main.models import *





# Views 
@login_required(login_url='login')
def lecture_assignment(request , id , assignment):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    lecture = get_object_or_404(Lecture ,slug=id)

    if User.objects.filter(username=request.user.username).first():
        parts = StudentPartObject.objects.filter(user=request.user , lecture_id=lecture.id)
    else:
        parts = Part.objects.filter(lecture_id=lecture.id)

    videos_count = Part.objects.filter(lecture_id=lecture.id , type='video').count()
    assignments_count = Part.objects.filter(lecture_id=lecture.id , type='assignment').count() 
    total_questions_number = 0
    links_count = Part.objects.filter(lecture_id=lecture.id , type='link').count()
    students = BuyLesson.objects.filter(lecture_id=id)

    related_assignments = Assignment.objects.filter(lecture_id=lecture.id)
    for x in related_assignments:
        total_questions_number = total_questions_number + x.questions_count







    if Part.objects.filter(part_id=assignment).first():
        part = Part.objects.get(part_id=assignment)
        assignment = Assignment.objects.get(assignment_id=part.assignment_id)
        mode = 'assignment'
    else:
        return redirect("/lecture/" + str(lecture.id))
    

    if User.objects.filter(username=request.user.username).first():
        if user_profile.instructor == True:
            status = 'instructor'
        else:
            if BuyLesson.objects.filter(user=request.user , lecture_id=lecture.id).first():
                status = 'purchased'
            else:
                status = 'not-purchased'
    else:
        status = 'not-logged'

    if User.objects.filter(username=request.user.username).first():
        if user_profile.instructor == True:
            do_nothing = ''
        else:
            if BuyLesson.objects.filter(user=request.user , lecture_id=lecture.id).first():
                do_nothing = ''
            else:
                return redirect('/lecture/' + str(lecture.id))
    else:
        return redirect('/lecture/' + str(lecture.id))




    if User.objects.filter(username=request.user.username).first():
        if user_profile.instructor == True:
            do_nothing = ''
            assignment_status = 'instructor'
        else:
            if AssignmentOpen.objects.filter(user=request.user ,assignment_id=assignment.assignment_id).first():
                if AssignmentSubmit.objects.filter(user=request.user ,assignment_id=assignment.assignment_id).first():
                    assignment_status = 'submitted'
                else:
                    assignment_status = 'opened'
            else:
                assignment_status = 'not-started'






    return render(request, 'lectures/lecture.html' , {'part':part , 'assignment':assignment, 'assignment_status':assignment_status ,    'mode':mode , 'status':status , 'lecture':lecture , 'parts':parts, 'videos_count' : videos_count, 'links_count' : links_count , 'assignments_count':assignments_count ,'students':students , 'total_questions_number':total_questions_number , 'user_profile': user_profile , 'notifications' : notifications_count })








# Functions 
@login_required(login_url='register')
def create_assignment(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        assignment_name = request.POST['title']
        assignment_type = request.POST['type']
        assignment_lecture_id = request.POST['lecture-id']

        lecture = Lecture.objects.get(id=assignment_lecture_id)

        new_assignment= Assignment.objects.create(lecture_id=assignment_lecture_id , user=request.user , user_name=user_profile.name , assignment_name=assignment_name , assignment_type=assignment_type)
        new_assignment.save()


        # Create Assignment Part Objects 


        lecture_parts_number = lecture.parts_number
        part_number = lecture_parts_number + 1


        new_part = Part.objects.create(lecture_id=assignment_lecture_id , assignment_id=new_assignment.assignment_id , user=request.user , user_name=request.user.username , type='assignment'  , title=assignment_name , part_number=part_number , visible=True , original=True)
        new_part.save()
        lecture.parts_number = lecture.parts_number + 1
        lecture.save()


        # Create Part Object For Each User In The Platform And Edit Lecture Object
        students = Profile.objects.all()
        for x in students:
            student_user = User.objects.get(username=x.username)
            create_part_object = StudentPartObject.objects.create(part_id=new_part.part_id , lecture_id=new_part.lecture_id , assignment_id=new_assignment.assignment_id , user=student_user , user_name=student_user.username , type='assignment'  , title=new_part.title , part_number=new_part.part_number , visible=new_part.visible)
            create_part_object.save()

            student_lecture_object = StudentLectureObject.objects.get(user=student_user , lecture_id=new_part.lecture_id)
            student_lecture_object.parts_number = student_lecture_object.parts_number + 1
            student_lecture_object.save()
        # Create Part Object For Each User In The Platform And Edit Lecture Object


        # Create Assignment Part Objects 
        

        return redirect('/lecture/' + str(Lecture.objects.get(id=assignment_lecture_id).id) + '/assignment/' + str(new_part.part_id) )
