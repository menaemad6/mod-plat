from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save




User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    id_user = models.IntegerField()
    username = models.CharField(max_length=100, blank=True)


    name = models.CharField(max_length=100, blank=True , null=True)
    image = models.ImageField(upload_to='profile_images', default='blank-profile-picture.jpg' , blank=True , null=True)
    phone = models.CharField(max_length=100, blank=True , null=True)
    school = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    class years(models.TextChoices):
        first = 'first',
        second = 'second',
        third = 'third',
        none = 'none',
    year = models.CharField(max_length=25, choices=years.choices, default=years.none,  blank=True , null=True)

    money = models.IntegerField(editable=True , default='0')
    no_of_buys = models.IntegerField(default=0)


    # Roles 
    public = models.BooleanField(default=True)
    join_date = models.DateTimeField(default=datetime.now)
    premium = models.BooleanField(default=True)
    instructor = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)



    code = models.CharField(blank=True , max_length=100)



    
    def __str__(self):
        return self.user.username





class Lecture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)





    title = models.CharField(blank=True , max_length=100)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='lecture_images' , default='blank-lecture.jpeg')
    price = models.IntegerField(default=0)


    code = models.CharField(blank=True , max_length=100 ,  null=True)
    visible = models.BooleanField(default=True)

    parts_number = models.IntegerField(default=0)
    no_of_buys = models.IntegerField(default=0)
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)

    teacher_name = models.CharField(max_length=100 ,blank=True , null=True)
    teacher_img = models.ImageField(upload_to='teacher_images' , blank=True , null=True)

    duration = models.IntegerField(default=0)

    
    class years(models.TextChoices):
        first = 'first',
        second = 'second',
        third = 'third',
    year = models.CharField(max_length=25, choices=years.choices, null=True ,  blank=True)

    class types(models.TextChoices):
        normal = 'normal',
        chapter = 'chapter',
        group = 'group',
    type = models.CharField(max_length=25, choices=types.choices, default=types.normal,  blank=True)




    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = ("Lecture")
        verbose_name_plural = ("Lectures")
    
    
    def save(self , *args , **kwargs):
        if not self.slug :
            self.slug = slugify(self.id)
        super(Lecture , self).save( *args , **kwargs)

    def __str__(self):
        return self.title 


class StudentLectureObject(models.Model):
    object_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    lecture_id = models.CharField(max_length=100 , blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)

    parts_number = models.IntegerField(default=0)

    title = models.CharField(blank=True , max_length=100)
    image = models.ImageField(upload_to='lecture_images' , default='blank-lecture.jpeg')
    price = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)

    purchased = models.BooleanField(default=False)

    object = models.BooleanField(default=True)

    class years(models.TextChoices):
        first = 'first',
        second = 'second',
        third = 'third',
    year = models.CharField(max_length=25, choices=years.choices, default=years.first,  blank=True)
    
    created_at = models.DateTimeField(default=datetime.now)



    class Meta:
        verbose_name = ("Student Lecture Object")
        verbose_name_plural = ("Student Lecture Objects")

    def __str__(self):
        return self.user_name + " - " + self.title



class LectureCode(models.Model):
    code_id = models.CharField(max_length=8 , blank=True , null=True)
    lecture_id = models.CharField(max_length=100 , blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    teacher = models.CharField(max_length=100 , blank=True )
    
    qr_code = models.ImageField(upload_to='qr-codes' , default='blank-lecture.jpeg')
    total_students_number = models.IntegerField(default=0)
    used_times = models.IntegerField(default=0)

    valid = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.code_id 

    class Meta:
        verbose_name = ("Lecture Code")
        verbose_name_plural = ("Lecture Codes")



class Part(models.Model):
    part_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    lecture_id = models.CharField(max_length=500)

    assignment_id = models.CharField(max_length=500 , blank=True)
    assignment_questions_number = models.IntegerField(default=0)
    assignment_total_applicants = models.IntegerField(default=0)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)

    title = models.CharField(blank=True , max_length=100)
    part_number = models.IntegerField(default=1)

    class types(models.TextChoices):
        video = 'video',
        link = 'link',
        assignment = 'assignment',
        file = 'file' ,
    type = models.CharField(max_length=25, choices=types.choices, blank=True)



    visible = models.BooleanField(default=True)
    duration = models.IntegerField(default=0)

    video = models.FileField(upload_to='lectures' , blank=True)
    video_url = models.CharField(blank=True , max_length=100)
    youtube_url = models.CharField(blank=True , max_length=100)

    views = models.IntegerField(default=0)
    views_limit = models.IntegerField(default=0)

    active = models.BooleanField(default=False)
    original = models.BooleanField(default=True)

    # If Part Is A Link 
    link = models.CharField(blank=True , max_length=500)

    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title


class StudentPartObject(models.Model):
    object_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    part_id = models.CharField(max_length=500)
    lecture_id = models.CharField(max_length=500)


    assignment_id = models.CharField(max_length=500 , blank=True)
    assignment_questions_number = models.IntegerField(default=0)
    assignment_total_applicants = models.IntegerField(default=0)
    assignment_user_percentage = models.IntegerField(default=0)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)

    title = models.CharField(blank=True , max_length=100)
    part_number = models.IntegerField(default=1)

    class types(models.TextChoices):
        video = 'video',
        link = 'link',
        assignment = 'assignment',
        file = 'file' ,
    type = models.CharField(max_length=25, choices=types.choices, blank=True)


    visible = models.BooleanField(default=True)
    duration = models.IntegerField(default=0)

    part_total_views = models.IntegerField(default=0)

    views = models.IntegerField(default=0)
    views_limit = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.title + ' ( ' + self.user_name + ' ) ' 


class View(models.Model):
    view_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    student_part_object_id = models.CharField(max_length=500)
    part_id = models.CharField(max_length=500)
    lecture_id = models.CharField(max_length=500)


    title = models.CharField(blank=True , max_length=100)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)


    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title + ' ( ' + self.user_name + ' ) ' 
    


class Chapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)


    title = models.CharField(blank=True , max_length=100)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='chapter_images' , default='none.jpeg')
    price = models.IntegerField(default=0)
    code = models.CharField(blank=True , max_length=100 ,  null=True)


    no_of_buys = models.IntegerField(default=0)
    no_of_lectures = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)



    class years(models.TextChoices):
        first = 'first',
        second = 'second',
        third = 'third',
    year = models.CharField(max_length=25, choices=years.choices, default=years.first,  blank=True)
    
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = ("Chapter")
        verbose_name_plural = ("Chapters")
    
    
    def save(self , *args , **kwargs):
        if not self.slug :
            self.slug = slugify(self.id)
        super(Chapter , self).save( *args , **kwargs)

    def __str__(self):
        return self.title + ' ( ' + self.user + ' ) ' 

class ChapterLecture(models.Model):
    chapter_id = models.CharField(max_length=100, blank=True)
    lecture_id = models.CharField(max_length=100, blank=True)

    image = models.ImageField(upload_to='lecture_images' , default='none.jpeg')
    title = models.CharField(blank=True , max_length=100)
    teacher_name = models.CharField(max_length=100 ,blank=True , null=True)
    teacher_img = models.ImageField(upload_to='teacher_images' , blank=True , null=True)

    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = ("Chapter Lecture")
        verbose_name_plural = ("Chapter Lectures")
    

    def __str__(self):
        return self.title + ' Added To ' + self.chapter_id 





class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)

    title = models.CharField(blank=True , max_length=100)
    image = models.ImageField(upload_to='group_images', blank=True)
    code = models.CharField(blank=True , max_length=100 )
    created_at = models.DateTimeField(default=datetime.now)

    no_of_lectures = models.IntegerField(default=0)
    no_of_students = models.IntegerField(default=0)

    class years(models.TextChoices):
        first = 'first',
        second = 'second',
        third = 'third',
    year = models.CharField(max_length=25, choices=years.choices, default=years.first,  blank=True)


    link = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = ("Group")
        verbose_name_plural = ("Groups")
    
    
    def save(self , *args , **kwargs):
        if not self.slug :
            self.slug = slugify(self.id)
        super(Group , self).save( *args , **kwargs)

    def __str__(self):
        return self.title + ' ( ' + self.year + ' ) ' 

class GroupMember(models.Model):
    member_name = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)
    image = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')

    group_id = models.CharField(max_length=100, blank=True)
    group_title = models.CharField(max_length=100, blank=True)
    group_image = models.ImageField(upload_to='group_images', blank=True)


    created_at = models.DateTimeField(default=datetime.now)
    
    class Meta:
        verbose_name = ("Group Member")
        verbose_name_plural = ("Group Members")
    

    def __str__(self):
        return self.member_name + ' Joined ' + self.group_title 

class GroupLecture(models.Model):
    group_id = models.CharField(max_length=100, blank=True)
    lecture_id = models.CharField(max_length=100, blank=True)

    image = models.ImageField(upload_to='lecture_images' , default='none.jpeg')
    title = models.CharField(blank=True , max_length=100)
    teacher_name = models.CharField(max_length=100 ,blank=True , null=True)
    teacher_img = models.ImageField(upload_to='teacher_images' , blank=True , null=True)

    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = ("Group Lecture")
        verbose_name_plural = ("Group Lectures")
    

    def __str__(self):
        return self.title + ' Added To ' + self.group_id 







class BuyLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)
    user_image = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')

    lecture_id = models.CharField(max_length=500)
    lecture_title = models.CharField(max_length=100 ,  blank=True)


    lecture_value = models.IntegerField(editable=True , default='0' , blank=True)

    created_at = models.DateTimeField(default=datetime.now)

    class methods(models.TextChoices):
        wallet = 'wallet',
        code = 'code',
        lecture_code = 'lecture_code',
        chapter = 'chapter',
        group = 'group',
        admin = 'admin',
        link = 'link',
    method = models.CharField(max_length=25, choices=methods.choices, default=methods.code, blank=True)
    link = models.CharField(max_length=100 ,  blank=True)

    def __str__(self):
        return self.user_name + ' Purchased ' + self.lecture_title + " ( " + self.lecture_id + " )  "

    class Meta:
        verbose_name = ("Lecture Purchase")
        verbose_name_plural = ("Lecture Purchases")

class BuyChapter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)
    user_image = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')

    chapter_id = models.CharField(max_length=500)
    chapter_title = models.CharField(max_length=100 ,  blank=True)

    created_at = models.DateTimeField(default=datetime.now)

    class methods(models.TextChoices):
        wallet = 'wallet',
        code = 'code',
        chapter_code = 'chapter_code',
    method = models.CharField(max_length=25, choices=methods.choices, default=methods.code, blank=True)


    def __str__(self):
        return self.user_name + ' Purchased ' + self.chapter_title + " ( " + self.chapter_id + " )  "

    class Meta:
        verbose_name = ("Chapter Purchase")
        verbose_name_plural = ("Chapter Purchases")





class Code(models.Model):
    code_id = models.CharField(max_length=8 , blank=True , null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    teacher = models.CharField(max_length=100 , blank=True )
    money = models.IntegerField()

    student = models.CharField(max_length=100 , blank=True )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.code_id + '    -   ' + str(self.active)

    class Meta:
        verbose_name = ("Code")
        verbose_name_plural = ("Codes")




class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)



    class notification_types(models.TextChoices):
        charge = 'charge',
        purchase = 'purchase',
        withdraw = 'withdraw',
        like = 'like',
        buy = 'buy',
        comment = 'comment',
        reply = 'reply',
    
    notification_type = models.CharField(max_length=25, choices=notification_types.choices,  blank=True , null=True)

    class purchase_types(models.TextChoices):
        code = 'code',
        wallet = 'wallet'
    purchase_type = models.CharField(max_length=25, choices=purchase_types.choices,  blank=True)

    created_at = models.DateTimeField(default=datetime.now)



    # If Notification Type Is purchase
    lecture = models.CharField(max_length=100 , blank=True)
    money = models.IntegerField(editable=True , default='0' , blank=True)
    wallet = models.IntegerField(editable=True , default='0' , blank=True)

    # If Notification Type Is Comment Or Reply
    second_user = models.CharField(max_length=100 , blank=True)

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = ("Notification")
        verbose_name_plural = ("Notifications")


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)


    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)


    lecture = models.CharField(max_length=100 , blank=True)
    money = models.IntegerField(editable=True , default='0' , blank=True)
    wallet = models.IntegerField(editable=True , default='0' , blank=True)

    value = models.IntegerField(editable=True , default='0' , blank=True , null=True)

    class transaction_types(models.TextChoices):
        charge = 'charge',
        purchase = 'purchase'
    transaction_type = models.CharField(max_length=25, choices=transaction_types.choices,  blank=True , null=True)

    class purchase_types(models.TextChoices):
        code = 'code',
        wallet = 'wallet'
    purchase_type = models.CharField(max_length=25, choices=purchase_types.choices,  blank=True)

    created_at = models.DateTimeField(default=datetime.now)



    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = ("Transaction")
        verbose_name_plural = ("Transactions")






class LikeLecture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)
    user_image = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')

    lecture_id = models.CharField(max_length=500)


    liked_at = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.user_name + ' Liked ' + self.lecture_id

    class Meta:
        verbose_name = ("Like")
        verbose_name_plural = ("Likes")



class StudentQuestion(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    lecture_id = models.CharField(max_length=500 , blank=True)


    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)
    user_image = models.ImageField(upload_to='profile_images' , blank=True , null=True)

    commented_to = models.CharField(max_length=100 , blank=True)

    comment = models.CharField(max_length=500)


    created_at = models.DateTimeField(default=datetime.now)


    no_of_likes = models.IntegerField(default=0)  
    no_of_answers = models.IntegerField(default=0)  

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = ("Student Question")
        verbose_name_plural = ("Student Questions")

class StudentQuestionAnswer(models.Model):
    answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    question_id = models.CharField(max_length=500)


    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)
    user_image = models.ImageField(upload_to='profile_images' , blank=True , null=True)


    answered_to = models.CharField(max_length=100 , blank=True)

    question_text = models.CharField(max_length=500 , blank=True)
    answer = models.CharField(max_length=500 , blank=True)


    created_at = models.DateTimeField(default=datetime.now)


    no_of_likes = models.IntegerField(default=0)  

    def __str__(self):
        return self.user + ' Replyed On ' + self.question_id

    class Meta:
        verbose_name = ("Student Question Answer")
        verbose_name_plural = ("Student Question Answer")













class Assignment(models.Model):
    assignment_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    # If Related To an lecture 
    lecture_id = models.CharField(max_length=500 , blank=True ,default='none')

    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)

    assignment_name = models.CharField(max_length=100 , blank=True)

    questions_count = models.IntegerField(default=0)
    no_of_applicants = models.IntegerField(editable=True , default='0' , blank=True)

    class assignment_types(models.TextChoices):
        test = 'test',
        homework = 'homework',
    assignment_type = models.CharField(max_length=25, choices=assignment_types.choices,  blank=True)
    created_at = models.DateTimeField(default=datetime.now)


    minutes = models.IntegerField(default=0)
    
    slug = models.SlugField(blank=True, null=True)
    def save(self , *args , **kwargs):
        if not self.slug :
            self.slug = slugify(self.assignment_id)
        super(Assignment , self).save( *args , **kwargs)

    def __str__(self):
        return self.assignment_name

    class Meta:
        verbose_name = ("Assignment")
        verbose_name_plural = ("Assignments")

class AssignmentOpen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)

    assignment_id = models.CharField(max_length=500)
    assignment_name = models.CharField(max_length=100 , blank=True)
    questions_count = models.IntegerField(default=0)



    start_at = models.DateTimeField(default=datetime.now)


    minutes = models.IntegerField(default=0)

    timer_minutes = models.IntegerField(default=0)
    timer_seconds = models.IntegerField(default=0)



    def __str__(self):
        return self.user_name + ' Opened ' + self.assignment_name

    class Meta:
        verbose_name = ("Assignment Start")
        verbose_name_plural = ("Assignment Starts")

class AssignmentSubmit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)

    assignment_id = models.CharField(max_length=500)
    assignment_name = models.CharField(max_length=100 , blank=True)
    questions_count = models.IntegerField(default=0)


    true_answers = models.IntegerField(default=0)
    false_answers = models.IntegerField(default=0)


    opened_at = models.CharField(max_length=100 , blank=True)
    submited_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user_name + ' Submited ' + self.assignment_name

    class Meta:
        verbose_name = ("Assignment Submit")
        verbose_name_plural = ("Assignment Submits")




class Question(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    assignment_id = models.CharField(max_length=500)
    assignment_name = models.CharField(max_length=500 , blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)



    question_number = models.IntegerField(default=0 , blank=True)
    class types(models.TextChoices):
        normal = 'normal',
        image_ar = 'image_ar',
        image_en = 'image_en',
    question_type = models.CharField(max_length=25, choices=types.choices, default=types.normal,  blank=True , null=True)



    question = models.CharField(max_length=100 , blank=True)
    question_image = models.ImageField(upload_to='questions', default='blank-profile-picture.png' , blank=True , null=True)
    true = models.CharField(max_length=100 , blank=True)
    answer1 = models.CharField(max_length=100 , blank=True)
    answer2 = models.CharField(max_length=100 , blank=True)
    answer3 = models.CharField(max_length=100 , blank=True)
    answer4 = models.CharField(max_length=100 , blank=True)


    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.assignment_name + ' - ' +  self.question + ' - ' + self.true 

    class Meta:
        verbose_name = ("Assignment Question")
        verbose_name_plural = ("Assignment Questions")

class Answer(models.Model):
    answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    assignment_id = models.CharField(max_length=500)
    assignment_name = models.CharField(max_length=500 , blank=True)
    question_id = models.CharField(max_length=500)
    question_number = models.IntegerField(default=0 , blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)
    


    question = models.CharField(max_length=100 , blank=True)
    question_image = models.ImageField(upload_to='questions', default='blank-profile-picture.png' , blank=True , null=True)
    question_true = models.CharField(max_length=100 , blank=True)
    answer1 = models.CharField(max_length=100 , blank=True)
    answer2 = models.CharField(max_length=100 , blank=True)
    answer3 = models.CharField(max_length=100 , blank=True)
    answer4 = models.CharField(max_length=100 , blank=True)


    answered = models.BooleanField(default=False)
    true = models.BooleanField(default=False)
    answer = models.CharField(max_length=100 , blank=True)


    created_at = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.question + ' - ' + self.username + ' - (True Answer= ' + self.question_true + ' )  -    ' + self.answer

    class Meta:
        verbose_name = ("Assignment Answer")
        verbose_name_plural = ("Assignment Answers")












class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)

    title = models.CharField(max_length=40 , blank=True)
    caption = models.TextField(max_length=1000 , blank=True)
    date = models.DateTimeField(("join date"),default=datetime.now)

# If Image 
    image = models.ImageField( upload_to='news/' , verbose_name=("News Image") , blank=True ,  null=True)

    slug = models.SlugField(blank=True , null=True  , allow_unicode=True , unique=True)
    def save(self , *args , **kwargs):
        if not self.slug :
            self.slug = slugify(self.title)
            super(News , self).save(*args , **kwargs)


    def __str__(self):
        return self.title


    class Meta:
        verbose_name = ("New")
        verbose_name_plural = ("News")

class GetPremium(models.Model):
    user = models.OneToOneField(User, verbose_name=("user"), on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True , null=True)
    email = models.CharField(max_length=200, blank=True , null=True)

    class years(models.TextChoices):
        first = 'first',
        second = 'second',
        third = 'third',

    year = models.CharField(max_length=25, choices=years.choices, default=years.first,  blank=True)

    class Meta:
        verbose_name = ("Registration")
        verbose_name_plural = ("Premium Registrations")

    def __str__(self):
        return  '%s' %(self.name)

class RechargeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)

    amount = models.CharField(max_length=500)
    sender_number = models.CharField(max_length=100 , blank=True)
    wallet_number = models.CharField(max_length=100 , blank=True)
    created_at = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.user_name + ' Requested ' + self.amount

    class Meta:
        verbose_name = ("Recharge")
        verbose_name_plural = ("Recharges")

class LoginInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    username = models.CharField(max_length=100 , blank=True)
    password = models.CharField(max_length=100 , blank=True)

    device_type = models.CharField(max_length=100 , blank=True)
    browser_type = models.CharField(max_length=100 , blank=True)
    
    time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user
    
    class Meta:
        verbose_name = ("Login Info")
        verbose_name_plural = ("Login Infos")



class Theme(models.Model):
    theme_id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    user = models.ForeignKey(User, on_delete=models.CASCADE , blank=True , null=True)
    user_name = models.CharField(max_length=100 , blank=True)

    name = models.CharField(max_length=500 , blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    number = models.IntegerField(default=1)
    active = models.BooleanField(default=False)

    class logo_types(models.TextChoices):
        text = 'text',
        image = 'image',
    logo_type = models.CharField(max_length=25, choices=logo_types.choices, default=logo_types.text,  blank=True , null=True)
    logo_title = models.CharField(max_length=500 , blank=True)
    logo_image = models.ImageField(upload_to='logo_images' , blank=True , null=True)

    primary_color = models.CharField(max_length=500 , blank=True)
    secondary_color = models.CharField(max_length=500 , blank=True)


    home_page_image_1 = models.ImageField(upload_to='theme_images' , blank=True , null=True)
    home_page_image_2 = models.ImageField(upload_to='theme_images' , blank=True , null=True)
    home_page_image_3 = models.ImageField(upload_to='theme_images' , blank=True , null=True)


    def __str__(self):
        return self.name + ' ( ' + self.user_name + ' ) ' 
