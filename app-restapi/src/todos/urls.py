from django.urls import path

from todos import views

urlpatterns=[
    path('', views.TodosAPIView.as_view(), name='todos'),
    path('<int:id>/', views.TodoDetailAPIView.as_view(), name='todo'),
    # Yukarıdaki iki satır yeterli fakat elde örnek olması için aşağıda ki satırları silmedim
    path('create/', views.CreateTodoAPIView.as_view(), name='create'),
    path('list/', views.ListTodoAPIView.as_view(), name='list'),
]