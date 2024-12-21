from django.urls import path
from . import views     
    
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    
    path('login', views.login,name='login'),
    path('delete_pie', views.delete_pie),
    path('new_pies/<int:baker_id>', views.new_pies),
    path('all_pies', views.all_pies, name='all_pies'),
    path('update_pie', views.update_pie, name='update_pie'),
    
    path('logout', views.logout, name='logout'),

    
    
    
    
    path('pies/<int:pie_id>', views.pie_card),
    path('pies/edit/<int:pie_id>', views.edit_pie),
    path('vote_pie/<int:pie_id>', views.vote_pie),
    
    
]
