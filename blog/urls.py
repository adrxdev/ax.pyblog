from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('post/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('post/<int:pk>/report/', views.report_post, name='report'),
    path('category/<str:category>/', views.blog_category, name='blog_category'),


    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Blog CRUD URLs
    path('create/', views.blog_create, name='blog_create'),
    path('edit/<int:pk>/', views.blog_edit, name='blog_edit'),
    path('delete/<int:pk>/', views.blog_delete, name='blog_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
