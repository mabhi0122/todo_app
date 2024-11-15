from django.urls import path
from mainapp import views

urlpatterns = [
    # path('', views.HomeView.as_view(), name= 'home'),
    path('', views.todo_tasks, name='todo_list'),
    path('update-task/', views.update_task, name='update-task'),
    path('delete-task/<int:id>', views.DeleteView.as_view(), name='delete-task'),
    path('update-task/<int:id>', views.UpdateView.as_view(), name='update-task'),
    path('detail-view/<int:pk>', views.DetailTaskView.as_view(), name='detail-view'),

    path('completed/', views.completed_tasks, name="completed-tasks"),
    path('incompleted/', views.incompleted_tasks, name="incompleted-tasks"),


]
