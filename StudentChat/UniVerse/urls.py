from django.urls import path
from . import views 

urlpatterns = [
    path('', views.Main.as_view(), name="main"),
    path('login', views.Login.as_view(), name="login"),
    path('register', views.Register.as_view(), name="register"),
    path('logout', views.Logout.as_view(), name="logout"),
    path('chats', views.AllChats.as_view(), name="chats"),
    path('classes', views.classes.as_view(), name="classes"),
    path('flashcard', views.flashcard.as_view(), name="flashcard"),
    path('account', views.account.as_view(), name="account"),
    path('chat_person/<int:id>', views.ChatPerson.as_view(), name="chat_person")
]
