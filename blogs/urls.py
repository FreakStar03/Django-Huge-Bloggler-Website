from django.urls import path

from . import views
from .views import add_blog

from .feeds import LatestPostsFeed

urlpatterns = [
    path('', views.redirecthome, name='redirect'),
    path('add_blog/', add_blog, name='add_blog'),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path('signup_login/', views.signup_login, name="signup_login"),
    path('logout/', views.logout, name="logout"),
    path('<slug:genre>/', views.PostList,name='home'),
    path('search/<slug:search_data>', views.SearchList, name='search'),
   # path('files/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:genre>/<slug:slug>/', views.post_detail, name='post_detail'),
]

