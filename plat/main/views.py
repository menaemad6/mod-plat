from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import random
from django.shortcuts import get_object_or_404



from .models import Profile , Lecture , StudentLectureObject, LectureCode ,  Part , StudentPartObject, View , Chapter , ChapterLecture , Group , GroupMember , GroupLecture , BuyLesson , BuyChapter
from .models import Code , Notification , Transaction , LikeLecture , StudentQuestion ,  StudentQuestionAnswer 
from .models import Assignment , AssignmentOpen  , AssignmentSubmit ,Question , Answer ,   News ,GetPremium ,RechargeRequest , LoginInfo           



def error_404(request , exception):
    return render(request , 'error-404.html' , status=404)



def index(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''



    if User.objects.filter(username=request.user.username).first():
        lectures = StudentLectureObject.objects.filter(user=request.user).order_by('-created_at')
    else:
        lectures = Lecture.objects.all().order_by('-created_at')

    return render(request, 'main/index.html', { 'lectures':lectures   , 'user_profile': user_profile ,  'notifications' : notifications_count})




# Authentication Functions 

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            device_type = request.POST['device-type']
            browser_type = request.POST['browser-type']



            user = auth.authenticate(username=username, password=password)



            if user is not None:
                # Login With Username 
                auth.login(request, user)

                save_info = LoginInfo.objects.create(user=request.user , username=username , password=password , device_type=device_type , browser_type=browser_type)
                save_info.save()

                return redirect('/')
            else:
                # Login With Phone Number 
                if Profile.objects.filter(phone=username).first():
                    profile = Profile.objects.get(phone=username)
                    profile_user = profile.user

                    authenticate = auth.authenticate(username=profile_user.username, password=password)

                    if authenticate is not None:
                        auth.login(request, authenticate)
                        save_info = LoginInfo.objects.create(user=request.user , username=username , password=password , device_type=device_type , browser_type=browser_type)
                        save_info.save()
                        return redirect('/')
                    
                    else:
                        messages.info(request, 'Username or Password is wrong')
                        return redirect('login')

                else:
                    messages.info(request, 'Username or Password is wrong')
                    return redirect('login')

        else:
            return render(request, 'main/login.html')



def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            # Account Info 
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            name = request.POST['name']
            phone = request.POST['phone']
            location = request.POST['location']
            year = request.POST['year']


            # Login Info 
            device_type = request.POST['device-type']
            browser_type = request.POST['browser-type']
            login_date = request.POST['login-date']


            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'This email has been registered before')
                    return redirect('signup')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                    return redirect('signup')
                elif Profile.objects.filter(phone=phone).exists():
                    messages.info(request, 'Phone Number Registered Before')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    #log user in and redirect to settings page
                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)

                    #create a Profile object for the new user
                    user_model = User.objects.get(username=username)
                    student_user_id = user_model.id
                    student_code = int(student_user_id) + 1500
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id , username=request.user.username , code=student_code)
                    new_profile.save()

                    new_profile.name = name
                    new_profile.phone = phone
                    new_profile.location = location
                    new_profile.year = year
                    new_profile.save()
                    return redirect('/')
            else:
                messages.info(request, 'Password Not Matching')
                return redirect('signup')
            
        else:
            return render(request, 'main/signup.html')



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')



# Lectures 

def grades(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    return render(request, 'lectures/grades.html' , {'user_profile': user_profile , 'notifications' : notifications_count })

def grade(request , grade):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''






    if grade == '1':
        if User.objects.filter(username=request.user.username).first():
            lectures = StudentLectureObject.objects.filter(user=request.user , year='first').order_by('-created_at')
        else:
            lectures = Lecture.objects.filter(year='first').order_by('-created_at')
    else:
        if grade == '2':
            if User.objects.filter(username=request.user.username).first():
                lectures = StudentLectureObject.objects.filter(user=request.user , year='second').order_by('-created_at')
            else:
                lectures = Lecture.objects.filter(year='second').order_by('-created_at')
        else:
            if grade == '3':
                if User.objects.filter(username=request.user.username).first():
                    lectures = StudentLectureObject.objects.filter(user=request.user , year='third').order_by('-created_at')
                else:
                    lectures = Lecture.objects.filter(year='third').order_by('-created_at')
            else:
                return redirect("/lectures")


    grade_number = grade



    return render(request, 'lectures/lectures.html' , {'grade':grade_number , 'user_profile': user_profile , 'notifications' : notifications_count ,'lectures' : lectures })




def lecture(request , id):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if Lecture.objects.filter(id=id).first():
        lecture = get_object_or_404(Lecture ,slug=id)
    else:
        messages.warning(request, 'عذرا لا يوجد محاضرة بهذا اللينك')
        return redirect("/lectures")


    if User.objects.filter(username=request.user.username).first():
        parts = StudentPartObject.objects.filter(user=request.user , lecture_id=lecture.id)
    else:
        parts = Part.objects.filter(lecture_id=lecture.id)
    


    if Part.objects.filter(lecture_id=lecture.id , active=True).first():
        active_part = Part.objects.get(lecture_id=lecture.id , active=True)
    else:
        active_part = ''



    videos_count = Part.objects.filter(lecture_id=lecture.id , type='video').count()
    assignments_count = Part.objects.filter(lecture_id=lecture.id , type='assignment').count()
    total_questions_number = 0
    links_count = Part.objects.filter(lecture_id=lecture.id , type='link').count()
    
    related_assignments = Assignment.objects.filter(lecture_id=lecture.id)
    for x in related_assignments:
        total_questions_number = total_questions_number + x.questions_count
 


    mode = 'normal'


    all_students = Profile.objects.filter(instructor=False)
    subscribed_students = BuyLesson.objects.filter(lecture_id=lecture.id)

    subscribed_students_number = subscribed_students.count()
    all_students_number = all_students.count()
    subscribed_students_percentage = round(int(subscribed_students_number) / int(all_students_number) * 100)



    lecture_views = View.objects.filter(lecture_id=lecture.id)



    not_subscribed_students = []
    for x in all_students:
        if BuyLesson.objects.filter(user=x.user , lecture_id=lecture.id).first():
            do_nothing = ""
        else:
            appned_student = not_subscribed_students.append(x)


    all_parts = Part.objects.all()
    another_lectures_parts = []
    for x in all_parts:
        if x.lecture_id == str(lecture.id):
            do_nothing_2 = ''
            
        else:
            if Part.objects.filter(title=x.title , original=False).first():
                do_nothing_3 = ''
            else:
                append_part = another_lectures_parts.append(x)




    lecture_valid_codes = LectureCode.objects.filter(lecture_id=lecture.id , valid=True).order_by('-created_at')
    lecture_expired_codes = LectureCode.objects.filter(lecture_id=lecture.id , valid=False)

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


    return render(request, 'lectures/lecture.html' , {'lecture':lecture , 'mode':mode , 'status':status  , 'parts':parts, 'active_part':active_part , 'videos_count' : videos_count, 'links_count' : links_count , 'assignments_count':assignments_count ,'total_questions_number':total_questions_number , 'all_students':all_students , 'subscribed_students':subscribed_students , "not_subscribed_students":not_subscribed_students , 'subscribed_students_percentage':subscribed_students_percentage ,'lecture_views':lecture_views , 'another_lectures_parts':another_lectures_parts , 'valid_codes':lecture_valid_codes , 'expired_codes':lecture_expired_codes , 'user_profile': user_profile , 'notifications' : notifications_count })



# Same With Lecture View bUT add Video Attribute
@login_required(login_url='login')
def lecture_video(request , id , video):
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

    if Part.objects.filter(part_id=video).first():
        part = Part.objects.get(part_id=video)
        mode = 'video'
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





    # Increase Views Times
    user_part_object = StudentPartObject.objects.get(part_id=part.part_id , user=request.user)
    part_views_limit = part.views_limit

    if user_part_object.views >= part_views_limit:
        limit = 'exceed'
    else:


        if user_profile.instructor == False:
            user_part_object.views = user_part_object.views + 1
            user_part_object.save()

            part.views = int(part.views) + 1
            part.save()
        
            # Another Parts Objects
            another_parts_for_another_users = StudentPartObject.objects.filter(part_id=part.part_id)
            for x in another_parts_for_another_users:
                x.part_total_views = part.views
                x.save()

            create_view_object = View.objects.create(student_part_object_id=user_part_object.object_id , part_id=user_part_object.part_id ,lecture_id=lecture.id , title=user_part_object.title , user=request.user , user_name=user_profile.name).save()
            


        limit = 'not-exceed'
    # Increase Views Times




    return render(request, 'lectures/lecture.html' , {'part':part , 'user_part':user_part_object , 'limit':limit ,  'mode':mode , 'status':status , 'lecture':lecture , 'parts':parts, 'videos_count' : videos_count, 'links_count' : links_count , 'assignments_count':assignments_count , 'total_questions_number':total_questions_number , 'students':students , 'user_profile': user_profile , 'notifications' : notifications_count })




@login_required(login_url='login')
def lecture_code_students(request , id , lecture_code):
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

    if User.objects.filter(username=request.user.username).first():
        if user_profile.instructor == True:
            status = 'instructor'
        else:
            return redirect('/lecture/' + str(lecture.id))
    else:
        redirect('/lecture/' + str(lecture.id))


    videos_count = Part.objects.filter(lecture_id=lecture.id , type='video').count()
    assignments_count = Part.objects.filter(lecture_id=lecture.id , type='assignment').count()
    links_count = Part.objects.filter(lecture_id=lecture.id , type='link').count()



    lecture_code_object = LectureCode.objects.get(code_id=lecture_code)
    code_students = BuyLesson.objects.filter(lecture_id=lecture.id , method='link' , link=lecture_code)

    mode = 'lecture_code_students'

    return render(request, 'lectures/lecture.html' , { 'code_students':code_students , 'code':lecture_code_object , 'mode':mode , 'status':status , 'lecture':lecture , 'parts':parts, 'videos_count' : videos_count, 'links_count' : links_count , 'assignments_count':assignments_count , 'user_profile': user_profile , 'notifications' : notifications_count })



@login_required(login_url='login')
def lecture_code_join(request , id , lecture_code):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    lecture = get_object_or_404(Lecture ,slug=id)
    lecture_code_object = LectureCode.objects.get(code_id=lecture_code)

    if user_profile.instructor == False:
        if BuyLesson.objects.filter(lecture_id=lecture.id , user=request.user).first():
            return redirect("/lecture/" + str(lecture.id))
        else:
            if lecture_code_object.valid == False:
                status = 'expired'
            else:
                status = 'valid'
    else:
        return redirect("/lecture/" + str(lecture.id))


    return render(request, 'lectures/accept-join.html' , { 'status':status , 'lecture':lecture , 'code':lecture_code_object , 'user_profile': user_profile , 'notifications' : notifications_count })


@login_required(login_url='login')
def lecture_code_join_function(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    if request.method == 'POST':
        lecture_id = request.POST['lecture-id']
        code = request.POST['code']

        lecture_code_object = LectureCode.objects.get(code_id=code)
        lecture = Lecture.objects.get(id=lecture_id)

        if LectureCode.objects.filter(code_id=code).first():
            lecture_code_object = LectureCode.objects.get(code_id=code)
        else:
            return redirect("/lecture/" + lecture_id)


        if user_profile.instructor == False:

            if BuyLesson.objects.filter(lecture_id=lecture_id , user=request.user).first():
                return redirect("/lecture/" + lecture_id)
            else:

                if lecture_code_object.valid == False:
                    messages.warning(request, 'للاسف اللينك الذي ادخلته منتهي الصلاحية')
                    return redirect("/lecture/" + lecture_id)
                else:
                    join_lecture = BuyLesson.objects.create(user=request.user , lecture_id=lecture_id, lecture_title=lecture.title , lecture_value=0 , user_name=user_profile.name , user_image=user_profile.image , method='link' , link=code)
                    join_lecture.save()

                    lecture_code_object.used_times = lecture_code_object.used_times + 1
                    lecture_code_object.save()

                    if lecture_code_object.used_times == lecture_code_object.total_students_number :
                        lecture_code_object.valid = False
                        lecture_code_object.save()


                    user_profile.no_of_buys = user_profile.no_of_buys + 1
                    user_profile.save()
                    
                    lecture.no_of_buys = lecture.no_of_buys + 1
                    lecture.save()

                    user_lecture_object = StudentLectureObject.objects.get(lecture_id=lecture.id , user=request.user)
                    user_lecture_object.purchased = True
                    user_lecture_object.save()

                    messages.success(request, 'تم الاشتراك في المحاضرة بنجاح')
                    return redirect('/lecture/'+ str(lecture.id) )

        else:
            return redirect("/lecture/" + lecture_id)


@login_required(login_url='login')
def purchase_lecture(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        lecture_id = request.POST['lecture-id']


        lecture = Lecture.objects.get(id=lecture_id)
        
        buy_filter = BuyLesson.objects.filter(lecture_id=lecture_id, user=request.user).first()
        text = 'buy'

        if buy_filter == None:
            if user_profile.money < lecture.price:
                


                msg_color = 'warning'
                msg_ar = 'للاسف ليس لديك رصيد كافي لشراء هذة المحاضرة'
                msg_en = 'Unfortunately you dont have enough credit to purchase this lecture'


                messages.warning(request, 'للاسف ليس لديك رصيد كافي في المحفظة لشراء هذة المحاضرة')
                return redirect('/lecture/'+ str(lecture.id))
            else:
               purchase_lecture = BuyLesson.objects.create(user=request.user , lecture_id=lecture.id, lecture_title=lecture.title , lecture_value=lecture.price , user_name=user_profile.name , user_image=user_profile.image , method='wallet')
               purchase_lecture.save()


               user_profile.money = user_profile.money - lecture.price
               user_profile.no_of_buys = user_profile.no_of_buys + 1
               user_profile.save()
               
               lecture.no_of_buys = lecture.no_of_buys + 1
               lecture.save()

               user_lecture_object = StudentLectureObject.objects.get(lecture_id=lecture.id , user=request.user)
               user_lecture_object.purchased = True
               user_lecture_object.save()

               messages.success(request, 'تم شراء المحاضرة بنجاح')
               return redirect('/lecture/'+ str(lecture.id) )


               

            #    new_activity = Activity.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='wallet' , wallet=user_profile.money , lesson_name=post.title , money=lesson_price)
            #    new_notification = Notification.objects.create(username=request.user.username , activity_type='withdraw' ,purchase_type='wallet' , wallet=user_profile.money , lesson_name=post.title , money=lesson_price)
            #    new_notificatio = Notification.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='wallet' , wallet=user_profile.money , lesson_name=post.title , money=lesson_price)

            #    if Notification.objects.filter(username=post.user , activity_type='buy' , money=post.no_of_buys, lesson_name=post.title , liker=request.user.username ).first():
            #         new_notify = ''
            #    else:
            #         new_notify  = Notification.objects.create(username=post.user , activity_type='buy' , money=post.no_of_buys, lesson_name=post.title , liker=request.user.username )
        else:
            return redirect('/lectures')