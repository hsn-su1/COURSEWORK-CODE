from django.shortcuts import render , redirect
from django.views import View
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync # used to convert asynchronous layer functions to synchronus as we are writing in synchronusly
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User # used to add user details to django administration database
from . import models
from django.db.models import Q

# Create your views here.

class Main(View):
    def get(self, request):

        if request.user.is_authenticated:
            return redirect("chats")

        return render(request=request, template_name="UniVerse/main.html")
    
class Login(View):
    def get(self, request):
        return render(request=request, template_name="UniVerse/login.html")  
    
    def post(self, request):

        data = request.POST.dict()
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request=request, username=username, password=password)
        if user != None:
            login(request=request, user=user)
            return redirect("chats")

        context = {"error":"Incorrect login details."}
        return render(request=request, template_name="UniVerse/login.html", context=context)   # context allows template to access calues inside the context dictionary

class Register(View):
    def get(self, request):
        return render(request=request, template_name="UniVerse/register.html")  
    
    def post(self, request):

        context = {}
        
        data = request.POST.dict()
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        try:
            new_user = User()
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.username = username
            new_user.email = email
            new_user.set_password(password)
            new_user.save()

            user = authenticate(request=request, username=username, password=password)
            if user != None:
                login(request=request, user=user)
                return redirect("chats")
        except:
            context.update({"error":"Username or email already in use."})

        return render(request=request, template_name="UniVerse/register.html", context=context)  

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("main")
    
class flashcard(View):
    def get(self, request):

        if request.user.is_authenticated:
             return render(request=request, template_name="UniVerse/flashcard.html")

        return render(request=request, template_name="UniVerse/main.html")
    
class classes(View):
    def get(self, request):

        if request.user.is_authenticated:
             return render(request=request, template_name="UniVerse/classes.html")

        return render(request=request, template_name="UniVerse/main.html")

class account(View):
    def get(self, request):

        if request.user.is_authenticated:
             return render(request=request, template_name="UniVerse/account.html")

        return render(request=request, template_name="UniVerse/main.html")
    
class AllChats(View):
    def get(self, request):

        if request.user.is_authenticated:

            users = User.objects.all()

            context = {"user":request.user,
                       "users":users}

            return render(request=request, template_name="UniVerse/chats.html", context=context) # context allows template to access values inside the context dictionary
        
        return redirect("main")

class ChatPerson(View):
    def get(self, request, id): 

        person = User.objects.get(id=id)
        me = request.user
        messages = models.Message.objects.filter(Q(from_whom=me , to_whom=person) | Q(from_whom=person , to_whom=me)).order_by("date" , "time")

        other_user = models.UserChannel.objects.get(user=person)

        data = {"type":"recevier_function",
                "type_of_data":"the_messages_have_been_seen_from_the_other"}
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(other_user.channel_name, data)

        messages_have_not_been_seen = models.Message.objects.filter(from_whom=person, to_whom=me)
        messages_have_not_been_seen.update(has_been_seen=True)

        context = {"person":person,
                   "me":me,
                   "messages":messages}

        return render(request=request, template_name="UniVerse/chat_person.html", context=context)  
