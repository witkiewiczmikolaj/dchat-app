from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile, Friend, ChatMessage
from .forms import ChatMessageForm
from django.http import JsonResponse, HttpResponseNotFound
import json
import django
# Create your views here.

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/chats')
        else:
            messages.success(request, "There was an error, try again.")
            return redirect('/login_user')
    else:
        return render(request, "dchatapp/login.html", {})
    
def logoutUser(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('/login_user')

def index(request):
    if request.user.is_authenticated:
        user = request.user.profile
        friends = user.friends.all()
        context = {"user": user, "friends": friends}
        return render(request, "dchatapp/index.html", context)
    else:
        return HttpResponseNotFound("LOGIN FIRST!")

def detail(request, pk):
    if request.user.is_authenticated:
        friend = Friend.objects.get(profile_id=pk)
        user = request.user.profile
        profile = Profile.objects.get(id=friend.profile.id)
        chats = ChatMessage.objects.all()
        rec_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
        rec_chats.update(seen=True)
        form = ChatMessageForm()
        if request.method == "POST":
            form = ChatMessageForm(request.POST)
            if form.is_valid():
                chat_message = form.save(commit=False)
                chat_message.msg_sender = user
                chat_message.msg_receiver = profile
                chat_message.save()
                return redirect("detail", pk=friend.profile.id)
        context = {"friend": friend, "form": form, "user": user,
                "profile": profile, "chats": chats, "num": rec_chats.count()}
        return render(request, "dchatapp/detail.html", context)
    else:
        return HttpResponseNotFound("LOGIN FIRST!")

def sentMessages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_msg = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=profile, seen=False)
    return JsonResponse(new_chat_msg.body, safe=False)

def receivedMessages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    arr = []
    chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)

def chatNotification(request):
    user = request.user.profile
    friends = user.friends.all()
    arr = []
    for friend in friends:
        chats = ChatMessage.objects.filter(msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)

def friends(request):
    if request.user.is_authenticated:
        user = request.user.profile
        friends = user.friends.all()
        act_friends = []
        for friend in friends:
            act_friends.append(friend.profile)
        all_friends = list(Profile.objects.all())
        new_friends = [friend for friend in all_friends if friend not in act_friends]
        new_friends.remove(user)
        context = {"user": user, "friends": new_friends}
        return render(request, "dchatapp/friends.html", context)
    else:
        return HttpResponseNotFound("LOGIN FIRST!")

def addFriend(request):
    data = json.loads(request.body)
    friend_name = data["name"]
    user_id = Profile.objects.get(name=friend_name)
    friend = Friend.objects.get(profile=user_id.id)
    user_name = request.user.profile.name
    try:
        for user in Profile.objects.filter(name=user_name): 
            user.friends.add(friend)
            response = True
    except django.core.exceptions.FieldError:
        response = False
    return JsonResponse(response, safe=False)

def settings(request):
    if request.user.is_authenticated:
        user = request.user.profile
        context = {"user": user}
        return render(request, "dchatapp/settings.html", context)
    else:
        return HttpResponseNotFound("LOGIN FIRST!")

def changeName(request):
    data = json.loads(request.body)
    new_name = data["name"]
    try:
        user = Profile.objects.filter(name=request.user.profile) 
        user.update(name=new_name)
        response = True
    except AttributeError:
        response = False
    
    return JsonResponse(response, safe=False)

def changeNum(request):
    data = json.loads(request.body)
    num = data["num"]
    try:
        user = Profile.objects.filter(name=request.user.profile) 
        user.update(num=num)
        response = True
    except AttributeError:
        response = False
    return JsonResponse(response, safe=False)

def getNum(request):
    user = Profile.objects.get(name=request.user.profile)
    num = user.num
    return JsonResponse(num, safe=False)