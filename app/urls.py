from app.views import index, login, logout, test, test_creator, total, user_result
from django.urls import path  
  
app_name = 'app'  
urlpatterns = [  
    path('', index, name='index'),  
	path('login/', login, name='login'),  
	path('logout/', logout, name='logout'),  
	path('test_creator/', test_creator, name='test_creator'),
	path('test/<int:pk>', test, name='test'),
	path('test/<int:pk>/total', total, name='total'),
	path('test/<int:pk>/total/<int:user_id>', user_result, name='user_result'),

]