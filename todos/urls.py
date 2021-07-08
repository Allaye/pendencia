from django.urls import path
from todos import views

urlpatterns = [
    path('create/', views.CreateTodoApiView.as_view(), name='create'),
    path('retrive/', views.RetriveTodoApiView.as_view(), name='retrive'),
    path('doget/', views.CreateRetriveApiView.as_view(), name='create_retrive'),
    path('updelget/<int:id>/', views.RetriveUpdateDeleteApiView.as_view(), name='update_delete_retrive')
]