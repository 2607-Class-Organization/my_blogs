from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='hello'), 
   path('about', views.about, name='about'), 
   path('contact', views.contact, name='contact'), 
   path('blogs', views.blogs, name='blogs'), 
   path('blogs/<slug:slug>', views.blog_detail, name='blog_detail'), 
   path( "blogs/create/", views.create_post, name="create_post" ), 
   path( "blogs/<int:post_id>/edit/", views.edit_post, name="edit_post" ),
]
