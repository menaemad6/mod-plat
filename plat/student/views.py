from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import random
from django.shortcuts import get_object_or_404



from main.models import Profile , Lecture , StudentLectureObject, LectureCode ,  Part , StudentPartObject, Chapter , ChapterLecture , Group , GroupMember , GroupLecture , BuyLesson , BuyChapter
from main.models import Code , Notification , Transaction , LikeLecture , StudentQuestion ,  StudentQuestionAnswer 
from main.models import Assignment , AssignmentOpen  , AssignmentSubmit ,Question , Answer ,   News ,GetPremium ,RechargeRequest , LoginInfo           



# Main Page 

@login_required(login_url='login')
def main(request, pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''



    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    purchased_lectures = BuyLesson.objects.filter(user=profile.user)


    zero = 0

    payments = 0
    for x in purchased_lectures:
        payments = payments + x.lecture_value

    



    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'profile': profile,
        'profile_object': profile_object,
        'notifications' : notifications_count ,

        'payments' : payments,
    }

    if request.user.username == pk:
        return render(request, 'profile/main.html', context)
    else:
        if user_profile.instructor == True:
            return render(request, 'profile/main.html', context)
        else:
            return redirect('/profile/' + request.user.username)


# Wallet Start
@login_required(login_url='login')
def wallet_recharge(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    


    return render(request, 'profile/wallet-recharge.html' , {'user_profile': user_profile , 'notifications' : notifications_count })



@login_required(login_url='login')
def wallet_subscriptions(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    return render(request, 'profile/wallet-subscriptions.html' , {'user_profile': user_profile , 'notifications' : notifications_count })


@login_required(login_url='login')
def wallet_transactions(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    return render(request, 'profile/wallet-transactions.html' , {'user_profile': user_profile , 'notifications' : notifications_count })
# Wallet End


# Groups Start
@login_required(login_url='login')
def groups(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    return render(request, 'profile/groups.html' , {'user_profile': user_profile , 'notifications' : notifications_count })


@login_required(login_url='login')
def group(request , pk , gr):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    group = Group.objects.get(id=gr)


    return render(request, 'profile/group.html' , {'user_profile': user_profile , 'notifications' : notifications_count })
# Groups Start


# Accounts Start

@login_required(login_url='login')
def account(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)



    return render(request, 'profile/account.html' , {'profile':profile , 'user_profile': user_profile , 'notifications' : notifications_count })


@login_required(login_url='login')
def connections(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''
        

    


    return render(request, 'profile/connections.html' , {'user_profile': user_profile , 'notifications' : notifications_count })


@login_required(login_url='login')
def login_history(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    if LoginInfo.objects.filter(user=profile.user).first():
        logins = LoginInfo.objects.filter(user=profile.user)
    else:
        logins = ''


    return render(request, 'profile/login-history.html' , {'logins':logins , 'user_profile': user_profile , 'notifications' : notifications_count })
# Accounts End







# Notifications And Inbox Start
@login_required(login_url='login')
def notifications(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    return render(request, 'profile/notifications.html' , {'user_profile': user_profile , 'notifications' : notifications_count })

@login_required(login_url='login')
def inbox(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    return render(request, 'profile/inbox.html' , {'user_profile': user_profile , 'notifications' : notifications_count })
# Notifications And Inbox End





# Student Section Start
@login_required(login_url='login')
def lectures(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if StudentLectureObject.objects.filter(user=request.user).first():
        lectures = StudentLectureObject.objects.filter(user=request.user).order_by('-created_at')
    else:
        lectures = ''

    return render(request, 'profile/lectures.html' , {'lectures':lectures ,'user_profile': user_profile , 'notifications' : notifications_count })

@login_required(login_url='login')
def homeworks(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    return render(request, 'profile/homeworks.html' , {'user_profile': user_profile , 'notifications' : notifications_count })

@login_required(login_url='login')
def exams(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    return render(request, 'profile/exams.html' , {'user_profile': user_profile , 'notifications' : notifications_count })

@login_required(login_url='login')
def statistics(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    return render(request, 'profile/statistics.html' , {'user_profile': user_profile , 'notifications' : notifications_count })
# Student Section End




# Functions 
@login_required(login_url='register')
def code_charge_function(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    if request.method == 'POST':
        code = request.POST['code']
        destination = request.POST['destination']

        if Code.objects.filter(code_id=code).first():
            valid_code = Code.objects.get(code_id=code)
            valid_code_money = valid_code.money
            user_profile.money = user_profile.money + valid_code_money



            user_profile.save()
            user_object.save()
            text = 'yes'
            new_notification = Notification.objects.create(user=request.user ,user_name=request.user.username , notification_type='charge' ,purchase_type='code' )
            new_notification.save()

            valid_code.active = False
            valid_code.student = request.user.username
            valid_code.save()

            messages.info(request, 'تم شحن مبلغ ' + str(valid_code.money) + ' جنية في محفظنك بنجاح')
            if destination == 'profile-recharge-page':
                return redirect('/profile/' + str(request.user) + '/wallet/recharge')
            
            if destination == 'profile-main-page':
                return redirect('/profile/' + str(request.user))

        else:
            messages.info(request, 'الكود الذي ادخلته غير صالح او مستخدم من قبل')
            if destination == 'profile-recharge-page':
                return redirect('/profile/' + str(request.user) + '/wallet/recharge')
            
            if destination == 'profile-main-page':
                return redirect('/profile/' + str(request.user))

