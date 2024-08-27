from django.urls import path
from .views import (StudentPage,LectureReg,DetailPage,Assignment_Quiz_Score_One,
	Assignment_List,Assignment_Score,LecturerView,logoutUser,LecturerLogin,
	SearchBar,Task_View,Quiz_List,Quiz_Score,Assignment_Quiz_Score_One,
	PinView,send_student_assignment,Scratch_Pin_List,Send_Result,Assignment_Quiz_Score_Two,
	Assignment_Histories,Quiz_Histories,send_student_quiz,LandPage,LecturePin)
from django.views.generic import ListView
from django.contrib.auth import views as auth_views
# from . views import *


app_name = 'lecture'
urlpatterns =[
path(r'', LandPage, name='home'), 
path(r'lecturer_secret_pin', LecturePin, name='lp'),
path(r'student_view', StudentPage, name='student'),
path(r'lecturer_view', LecturerView, name='lv'),
path(r'lecturer-registration-page', LectureReg, name='lecReg'),
path(r'<slug>/lecturer_page', DetailPage, name='detPage'),
path(r'lecturer_login',LecturerLogin, name='login'),
path(r'search_bar/',SearchBar, name='search'),
path(r'<slug>/task', Task_View, name='task'),
path(r'logout', logoutUser, name='logout'),
path(r'list-of-assignments', Assignment_List, name='assignment'),
path(r'<slug>/assignment_score', Assignment_Score, name='ass_score'),
path(r'assignment_quiz_score_result', Assignment_Quiz_Score_One, name='aqss'),
path(r'assignment_quiz_score_result_ii', Assignment_Quiz_Score_Two, name='aqssl'),
path(r'list-of-quiz', Quiz_List, name='quiz'),
path(r'<slug>/quiz_score', Quiz_Score, name='quiz_score'),
path(r'scratch_card', PinView, name='pin'),
path(r'student_result_sent', send_student_assignment, name='student_result'),
path(r'student_result_sent_email', send_student_quiz, name='student_result_e'),
path(r'scratch_card_list', Scratch_Pin_List, name='pin_list'),
path(r'enter_email_address', Send_Result, name='send'),
path(r'assignment_histories', Assignment_Histories, name='ahist'),
path(r'quiz_histories', Quiz_Histories, name='qhist'),










]
