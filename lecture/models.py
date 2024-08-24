from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime
from .validators import result_file


DEGREE = [
	('Select Position','Select Position'),
	('Bsc','Bsc'),
	('Masters','Masters'),
	('PhD','PhD'),]


GENDER = [
	('Select Gender','Select Gender'),
	('Female','Female'),
	('Male','Male'),]


PROGRAMME = [
    ('Select Programme','Select Programme'),
    ('Bsc','Bsc'),
    ('CEP','CEP'),
    ('Masters','Masters'),
    ('PhD','PhD'),
    ('Sandwich','Sandwich'),]


YEAR = [
    ('Select Year','Select Year'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ]

TASK = [
    ('Select Task','Select Task'),
    ('Assignment','Assignment'),
    ('Handout','Handout'),
    ('Quiz','Quiz'),
    ('Pin','Pin'),]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pics =  models.ImageField(upload_to='Pictures/', blank=True)
    phone = models.IntegerField(blank = False, default=000000000000)
    degree = models.CharField(max_length=100, choices=DEGREE, default='Select Position')
    gender = models.CharField(max_length=100, choices=GENDER, default='Select Gender')
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
    	return f"{self.user.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.first_name} {self.user.last_name}")
            # Ensure the slug is unique
            original_slug = self.slug
            queryset = Profile.objects.all()
            counter = 1
            while queryset.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class Lecturer_View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    programme = models.CharField(max_length=100, choices=PROGRAMME, default='Select Programme')
    year = models.CharField(max_length=100, choices=YEAR, default='Select Year')
    task = models.CharField(max_length=100, choices=TASK, default='Select Task')
    upload =  models.FileField(upload_to='docs/', blank=True,validators=[result_file])
    number_of_student = models.IntegerField(blank=True,default=000000000000)
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.programme}-{self.year}-{self.task}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.programme}-{self.year}-{self.task}"


class Assignment_Answers(models.Model):
    question = models.ForeignKey(Lecturer_View, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False)
    reg_number = models.IntegerField(blank=False) 
    ass_upload =  models.FileField(upload_to='docs/', blank=False,validators=[result_file])
    score = models.IntegerField(blank=True,default=000000000000)
    is_opened = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.reg_number}")
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name}-{self.reg_number}"

    def ass_score(self):
        return self.score


    def Total(self):
        return ass_score() + quiz_score()


class Quiz_Answers(models.Model):
    question = models.ForeignKey(Lecturer_View, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False)
    reg_number = models.IntegerField(blank=False) 
    quiz_upload =  models.FileField(upload_to='docs/', blank=False,validators=[result_file])
    score = models.IntegerField(blank=True,default=000000000000)
    is_opened = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.reg_number}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}-{self.reg_number}"

    def quiz_score(self):
        return self.score


class Scratch_Pin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    programme = models.CharField(max_length=100, choices=PROGRAMME, default='Select Programme')
    year = models.CharField(max_length=100, choices=YEAR, default='Select Year')
    task = models.CharField(max_length=100, choices=TASK, default='Select Task')
    student_reg = models.IntegerField(blank=True,default=000000000000)
    number = models.IntegerField(blank=True,default=000000000000)
    usage_count = models.PositiveIntegerField(default=0)
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.number}"


   