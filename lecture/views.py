from django.shortcuts import render,redirect,get_object_or_404
from .forms import (PYT,SignUpForm,MoreSignUpForm,LoginForm,AS,QP,
	SearchForm,AA,QuizAA,QS,PinForm, PinFilter,Scratch_Pin_Form,EmailForm,
	Lec_Pin)
from .models import (Profile,Lecturer_View,Assignment_Answers,Quiz_Answers,Scratch_Pin)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.contrib import messages
from itertools import chain
import random
from .decorators import PinCode,Prevent_Manual_Access
import csv
import io
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils.http import url_has_allowed_host_and_scheme


def LandPage(request):
	return render(request, 'folder/landpage.html')

def LecturePin(request):
	form = Lec_Pin(request.POST)
	if form.is_valid():
		pin = form.cleaned_data.get("pin")
		if pin == "deptlecture":
			return redirect("lecture:login")
		else:
			messages.info(request,"Incorrect Pin, Try Again")	
			return redirect("lecture:lp")
	return render(request, 'folder/lecture_pin.html',{'form':form})


@PinCode
def StudentPage(request):
	profile = Profile.objects.all()
	paginator = Paginator(profile,12)

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)  
	
	try:
		page_obj = paginator.page(page_number)
	except PageNotAnInteger:
		page_obj = paginator.page(1)
	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)


	return render(request, "folder/home.html",{'page_obj':page_obj})

@Prevent_Manual_Access
def DetailPage(request, slug):
	profile = get_object_or_404(Profile, slug=slug)
	if request.method == 'POST':
		form = PYT(request.POST)
		if form.is_valid():
			programme_option = form.cleaned_data['programme']
			username = profile.user
			year_option = form.cleaned_data['year']
			task_option = form.cleaned_data['task']

			filtering = Lecturer_View.objects.all().filter(user=username,programme=programme_option, year=year_option, task=task_option)
			if filtering.exists():
				new_task = Lecturer_View.objects.get(user=username,programme=programme_option, year=year_option, task=task_option)
				return redirect('lecture:task', slug=new_task.slug)

			else:
				messages.info(request,f"Your lecturer has not uploaded any {task_option} for {programme_option} {year_option}")

			
	else:
		form = PYT()
	return render(request, "folder/detail.html",{'form': form, 'profile':profile})


def Task_View(request, slug):
    task = Lecturer_View.objects.get(slug=slug)
    if 'assignment' in request.POST:
    	form = AA(request.POST, files=request.FILES)

    	if form.is_valid():
    		name = form.cleaned_data['name']
    		reg_number = form.cleaned_data['reg_number']
    		ass_upload = form.cleaned_data['ass_upload']

    		form_qus = form.save(commit=False)
    		form_qus = Assignment_Answers(question=task, name=name, reg_number=reg_number, ass_upload=ass_upload)
    		form_qus.save()
    		messages.info(request,f"{name} with registration number {reg_number}, your assignment has been submitted")
    		return redirect('lecture:student')


    else:
    	form = AA()

    if 'quiz' in request.POST:
    	form_q = QuizAA(request.POST, files=request.FILES)

    	if form_q.is_valid():
    		name = form_q.cleaned_data['name']
    		reg_number = form_q.cleaned_data['reg_number']
    		quiz_upload = form_q.cleaned_data['quiz_upload']

    		form_qus = form_q.save(commit=False)
    		form_qus = Quiz_Answers(question=task, name=name, reg_number=reg_number, quiz_upload=quiz_upload)
    		form_qus.save()
    		messages.info(request,f"{name} with registration number {reg_number}, your quiz has been submitted")
    		return redirect('lecture:student')

    else:
    	form_q = QuizAA()

    return render(request, 'folder/task_detail.html', {'task': task,"form":form,"form_q":form_q})

def LectureReg(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		more_form = MoreSignUpForm(request.POST,files=request.FILES)

		if form.is_valid and more_form.is_valid():
			user = form.save()
			pro = more_form.save(commit=False)
			pro.user = user
			pro.save()
			login(request,user)
			return redirect("lecture:lv") 
	else:
		form = SignUpForm()
		more_form = MoreSignUpForm()
	return render(request, "folder/lectureReg.html",{"form":form, "more_form":more_form})


def Scratch_Pin_List(request):
	ss = Scratch_Pin.objects.all()
	if request.method == 'POST':
		form = PinFilter(request.POST)

		if form.is_valid():
			programme = form.cleaned_data['programme']
			year = form.cleaned_data['year']
			ss_filter = Scratch_Pin.objects.filter(programme=programme, year=year)


			
			return redirect("lecture:lv") 
	else:
		form = PinFilter()
		
	
	return render(request, "folder/pin_list.html",{"ss":ss})


@login_required(login_url='/lecturer_login')
def LecturerView(request):
	ss = Scratch_Pin.objects.all()
	
	user = request.user
	fasle =False
	profile = Profile.objects.filter(user=user)
	

	ll_model = Lecturer_View.objects.all()
	aa_model = Assignment_Answers.objects.all()
	ll = ll_model.values_list('slug')
	aa = aa_model.values_list('question')

	notifications_ass =Assignment_Answers.objects.filter(is_opened=False)
	notifications_ass_count =notifications_ass.count()

	
	notifications_quiz =Quiz_Answers.objects.filter(is_opened=False)
	notifications_quiz_count =notifications_quiz.count()

	if request.method == 'POST':
		form = PYT(request.POST,request.FILES)
		if form.is_valid():
			programme = form.cleaned_data['programme']
			year = form.cleaned_data['year']
			task = form.cleaned_data['task']
			number = form.cleaned_data['number_of_student']
			if programme == "Select Programme" or year == "Select Year" or task == "Select Task":
				messages.info(request, "please input the adequate fields")
				return redirect('lecture:lv')

			elif task == "Pin" and number != "":
				cards = []
				for i in range(0,number):
				    n = (random.randint(10000000,30000000))
				    # print(cards)
				    cards.append(Scratch_Pin(user=request.user,number=n,programme=programme, task=task, year=year))
				scratch_card = Scratch_Pin.objects.bulk_create(cards)
				messages.info(request, f"""Scratch cards for {programme} {year} has been generated sucessfully sucessfully""")
				return redirect('lecture:lv')
			    

			else:
				new_option = Lecturer_View(programme=programme, task=task, year=year)
				new_option = form.save(commit=False)
				new_option.user = request.user
			
				new_option.save()
				messages.info(request, f"""Your {task} for {programme} {year} has been uploaded sucessfully""")
		
	else:
		form = PYT()
	
	return render(request, "folder/lectureView.html",{"form":form,'profile':profile,"notifications_ass_count":notifications_ass_count, "notifications_quiz_count":notifications_quiz_count,"ss":ss})

@login_required(login_url='/lecturer_login')
def Assignment_List(request):
	ass_list =Assignment_Answers.objects.filter(is_opened=False)
	
	
	if request.method == 'POST':
		form = QP(request.POST,request.FILES)
		if form.is_valid():
			programme = form.cleaned_data['programme']
			year = form.cleaned_data['year']
			task = form.cleaned_data['task']
			lecture_view = Lecturer_View(programme=programme, year=year,task=task)

			
			quiz_list =Quiz_Answers.objects.filter(is_opened=True)
			ass_li =Assignment_Answers.objects.filter(is_opened=True)
			ass = [instance for instance in ass_li]

			print(ass)
			print(lecture_view)
			
			if lecture_view:
				return redirect("lecture:aqss")
	else:
		form = QP()
	return render(request, "folder/assignment.html",{"ass_list":ass_list,'form':form})

@login_required(login_url='/lecturer_login')
def Assignment_Quiz_Score_One(request):
	lec = Lecturer_View.objects.all()
	# ass = Assignment_Answers.objects.filter(question=lecture_view,is_opened=True)
	qq = Quiz_Answers.objects.all()
	combine = []

	for lecture_view in lec:
		ass = Assignment_Answers.objects.filter(question=lecture_view,is_opened=True)
		ques = Quiz_Answers.objects.filter(question=lecture_view,is_opened=True)
		
		for ass in ass:
		    try:
		    	score=ques.get(name=ass.name, reg_number=ass.reg_number).score
		    except Quiz_Answers.DoesNotExist:
		    	score = 0

		    total_score = ass.score + score

		    if total_score >= 70:
		    	grade ='A'

		    elif total_score >= 60:
		    	grade ='B'

		    elif total_score >= 50:
		    	grade ='C'

		    elif total_score >= 40:
		    	grade ='E'

		    else:
		    	grade ='F'


		    combine.append({"ass_name": ass.name, "ass_reg_number": ass.reg_number,"ass_score": ass.score,"score":score,"total_score":total_score,"grade":grade})

	return render(request, "folder/assignment_quiz.html",{"combine":combine,"ques":ques})


def Send_Result(request):
	if request.method == 'POST':
		form = EmailForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']

			

	else:
		form=EmailForm()

	return render(request, "folder/send.html",{"form":form})


def send_student_assignment(request):
    # Create an in-memory buffer for the CSV file
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    
    # Write the header row
    writer.writerow(['Name', 'Registration Number', 'Exam Score', 'Quiz Score', 'Total', "Grade"])
    
    # Retrieve data from both models
    lec = Lecturer_View.objects.all()
    combine = []

    for lecture_view in lec:
    	ass = Assignment_Answers.objects.filter(question=lecture_view,is_opened=True)
    	ques = Quiz_Answers.objects.filter(question=lecture_view,is_opened=True)

    	for ass in ass:
    		try:
    			score=ques.get(name=ass.name, reg_number=ass.reg_number).score
    		except Quiz_Answers.DoesNotExist:
    			score = 0


    		total_score = ass.score + score


    		if total_score >= 70:
    			grade ='A'

    		elif total_score >= 60:
    			grade ='B'

    		elif total_score >= 50:
    			grade ='C'

    		elif total_score >= 40:
    			grade ='E'


    		else:
    			grade ='F'



    		writer.writerow([
    			ass.name, 
    			ass.reg_number,
    			ass.score,
    			score,
    			total_score,
    			grade])
    
    # Get CSV content from buffer
    csv_content = csv_buffer.getvalue()
    csv_buffer.close()
    
    # Create email message
    email = EmailMessage(
        'Subject: Student Result',
        'Please find the attached student result.',
        'kelechinwekes94@gmail.com',
        ['kelechinwekes94@gmail.com'],
    )
    
    # Attach CSV file
    email.attach('export.csv', csv_content, 'text/csv')
    
    # Send email
    email.send()
    
    return HttpResponse('Student result sent via email.')





def send_student_quiz(request):
    # Create an in-memory buffer for the CSV file
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    
    # Write the header row
    writer.writerow(['Name', 'Registration Number', 'Exam Score', 'Quiz Score', 'Total', "Grade"])
    
    # Retrieve data from both models
    lec = Lecturer_View.objects.all()
    combine = []

    for lecture_view in lec:
    	ass = Assignment_Answers.objects.filter(question=lecture_view,is_opened=True)
    	ques = Quiz_Answers.objects.filter(question=lecture_view,is_opened=True)

    	for ques in ques:
    		try:
    			score=ass.get(nameques.name, reg_numberques.reg_number).score
    		except Quiz_Answers.DoesNotExist:
    			score = 0


    		total_score= ques.score + score


    		if total_score >= 70:
    			grade ='A'

    		elif total_score >= 60:
    			grade ='B'

    		elif total_score >= 50:
    			grade ='C'

    		elif total_score >= 40:
    			grade ='E'


    		else:
    			grade ='F'



    		writer.writerow([
    			ques.name, 
    			ques.reg_number,
    			ques.score,
    			score,
    			total_score,
    			grade])
    
    # Get CSV content from buffer
    csv_content = csv_buffer.getvalue()
    csv_buffer.close()
    
    # Create email message
    email = EmailMessage(
        'Subject: Student Result',
        'Please find the attached student result.',
        'kelechinwekes94@gmail.com',
        ['kelechinwekes94@gmail.com'],
    )
    
    # Attach CSV file
    email.attach('export.csv', csv_content, 'text/csv')
    
    # Send email
    email.send()
    
    return HttpResponse('Student result sent via email.')
\


@login_required(login_url='/lecturer_login')
def Assignment_Quiz_Score_Two(request):
	lec = Lecturer_View.objects.all()
	# ass = Assignment_Answers.objects.filter(question=lecture_view,is_opened=True)
	qq = Quiz_Answers.objects.all()
	combine = []

	# Create a dictionary for student data with scores
    
	for lecture_view in lec:
		ass = Assignment_Answers.objects.filter(question=lecture_view,is_opened=True)
		ques = Quiz_Answers.objects.filter(question=lecture_view,is_opened=True)
		
		for ques in ques:
		    try:
		    	score=ass.get(name=ques.name, reg_number=ques.reg_number).score
		    except Assignment_Answers.DoesNotExist:
		    	score = 0

		    total_score = ques.score + score

		    if total_score >= 70:
		    	grade ='A'

		    elif total_score >= 60:
		    	grade ='B'

		    elif total_score >= 50:
		    	grade ='C'

		    elif total_score >= 40:
		    	grade ='E'

		    else:
		    	grade ='F'


		    combine.append({"ass_name": ques.name, "ass_reg_number": ques.reg_number,"ass_score": ques.score,"score":score,"total_score":total_score,"grade":grade})

	return render(request, "folder/assignment_quiz.html",{"combine":combine,"ques":ques})


def Send_Result(request):
	if request.method == 'POST':
		form = EmailForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']

	else:
		form=EmailForm()

	
	return render(request, "folder/send.html",{"form":form,})


@login_required(login_url='/lecturer_login')
def Assignment_Score(request,slug):
	user = request.user
	ass =Assignment_Answers.objects.filter(is_opened=False)
	ass_list =Assignment_Answers.objects.get(slug=slug)
	if request.method == 'POST':
		form = AS(request.POST,request.FILES,instance= ass_list)
		if form.is_valid():
			form.save()

			ass_update = ass
			ass_update = form.save(commit=False)
			ass_update.is_opened = True
			ass_update.save()
			return redirect('lecture:assignment')
	else:
		form = AS()
	return render(request, "folder/assignment_score.html",{'form':form})

@login_required(login_url='/lecturer_login')
def Assignment_Histories(request):
	user = request.user
	ass = Lecturer_View.objects.filter(user=user, task="Assignment")
	form = QP(request.POST,request.FILES)
	if request.method == 'POST':
		if form.is_valid():
			programme = form.cleaned_data['programme']
			year = form.cleaned_data['year']
			task = form.cleaned_data['task']
			
			assi = Lecturer_View.objects.filter(user=user, task="Assignment",programme=programme, year=year)
			
			if assi:
				return render(request,"folder/ahlist.html",{"assi":assi})
		else:
			messages.info(request,f"You have not given out assignment")
			return redirect('lecture:ahist')
	else:
		form=QP()
	return render(request, 'folder/ass_his.html',{'form':form,"ass":ass})


@login_required(login_url='/lecturer_login')
def Quiz_List(request):
	user = request.user
	quiz_list =Quiz_Answers.objects.filter(is_opened=False)
	
	if request.method == 'POST':
		form = QP(request.POST,request.FILES)
		if form.is_valid():
			programme = form.cleaned_data['programme']
			year = form.cleaned_data['year']
			task = form.cleaned_data['task']
			
			lecture_view = Lecturer_View.objects.filter(programme=programme, year=year,task=task)
			if lecture_view:
				return redirect("lecture:aqssl")
	else:
		form = QP()
	return render(request, "folder/quiz.html",{"quiz_list":quiz_list,'form':form})

@login_required(login_url='/lecturer_login')
def Quiz_Score(request,slug):
	user = request.user
	quiz =Quiz_Answers.objects.filter(is_opened=False)
	quiz_list =Quiz_Answers.objects.get(slug=slug)

	if request.method == 'POST':
		form = QS(request.POST,request.FILES,instance= quiz_list)
		if form.is_valid():
			form.save()

			quiz_update = quiz
			quiz_update = form.save(commit=False)
			quiz_update.is_opened = True
			quiz_update.save()
			return redirect('lecture:quiz')
	else:
		form = QS()
	return render(request, "folder/quiz_score.html",{'form':form})



@login_required(login_url='/lecturer_login')
def Quiz_Histories(request):
	user = request.user
	ass = Lecturer_View.objects.filter(user=user, task="Quiz")
	form = QP(request.POST,request.FILES)
	if request.method == 'POST':
		if form.is_valid():
			programme = form.cleaned_data['programme']
			year = form.cleaned_data['year']
			task = form.cleaned_data['task']
			
			assi = Lecturer_View.objects.filter(user=user, task="Quiz",programme=programme, year=year)
			
			if assi:
				return render(request,"folder/qhlist.html",{"assi":assi})
		else:
			messages.info(request,f"You have not given out quiz")
			return redirect('lecture:qhist')


	else:
		form=QP()
	return render(request, 'folder/qui_his.html',{'form':form,"ass":ass})



def LecturerLogin(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']


		user = authenticate(request, username=username, password=password)
		if user is not None:
			form=login (request, user)
			messages.success(request, f"Welcome {username} !!!")
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))

			else:
				return redirect('lecture:lv')
		else:
			messages.success(request, "Wrong username or password.. please try again")
	form = LoginForm() 
	return render(request, "folder/login.html", {"form":form})

# @PinCode
def PinView(request):
	if request.method == 'POST':
		pin = request.POST.get('pin')
		reg = request.POST.get('reg_number')
		print(pin)
		print(reg)

		try:
			scratch_n = Scratch_Pin.objects.get(number=pin)
			print(scratch_n)

			if scratch_n.student_reg != reg:
				scratch_n.student_reg = reg
				scratch_n.save()
				messages.success(request, "Your pin has been associated with this registration number")


			else:
				messages.success(request, "Please input the pin on your scratch card")
				return redirect("lecture:pin")

		except Scratch_Pin.DoesNotExist:
			return redirect("lecture:pin")
	return render(request, 'folder/pin.html')
       
        
def logoutUser(request):
    logout(request)
    messages.success(request, "You just logged out, see you soon!!!")
    return redirect('lecture:home')

    
# Create your views here.


def SearchBar(request):
	query = request.GET.get("query")
	if query:
		result = Profile.objects.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query))
		print(result)
		context = {'result':result,'query':query}
	

		return render(request,"folder/search.html",context)

