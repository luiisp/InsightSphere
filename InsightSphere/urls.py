
from django.urls import path
from app_InsightSphere import views
from django.contrib import admin
from app_InsightSphere.views import NewChannel,Delete,Menu,Home,Login,NewAcc,Anonim,Logout,Channel_V,User_V


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', Login.as_view(), name='custom_login'),
    path('new/', NewAcc.as_view(), name='newacc'),
    path('logout/', Logout.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('anonim/',Anonim.as_view(), name='anonim'),
    path('menu/',Menu.as_view(), name='menu'),
    path('c/<str:username>/<int:channel_id>/', Channel_V.as_view(), name='channel_detail'),
    path('@<str:username>', User_V.as_view(), name='user_detail'),
    path('newc/',NewChannel.as_view(),name='newchannel'),
    path('delete/<int:channel_id>/', Delete.as_view(), name='delete')

]