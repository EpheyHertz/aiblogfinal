from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name="home" ),
    path('login/',views.user_login,name="login" ),
    path('contact/',views.contact,name="contact" ),
    path('dashboard/',views.dashboard,name="dashboard" ),
    path('register/',views.user_signup,name="signup" ),
    path('logout/',views.user_logout,name="logout" ),
    path('generateblog/',views.generate_blog,name="generateblog" ),
    path('blog-posts/',views.blog_list,name="blog_list" ),
    path('blog-details/<uuid:pk>/',views.blog_details,name="blog_details" ),
    path('deleteblog/<uuid:blog_id>/', views.delete_blog, name='delete_blog'),
]
