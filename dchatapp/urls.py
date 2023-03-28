from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('friend/<str:pk>', views.detail, name = "detail"),
    path('sent_msg/<str:pk>', views.sentMessages, name = "sent_msg"),
    path('rec_msg/<str:pk>', views.receivedMessages, name = "rec_msg"),
    path('notification', views.chatNotification, name = "notification"),
    path('friends', views.friends, name = "friends"),
    path('add_friend', views.addFriend, name = "add_friend"),
    path('settings', views.settings, name = "settings"),
    path('change_name', views.changeName, name = "change_name"),
    path('change_num', views.changeNum, name = "change_num"),
    path('get_num', views.getNum, name = "get_num"),
    path('login_user', views.loginUser, name = "login_user"),
    path('logout_user', views.logoutUser, name = "logout_user"),
]