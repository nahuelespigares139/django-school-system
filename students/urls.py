from django.urls import path

from .views import student_list, StudentDeleteView, StudentDetailView, StudentUpdateView, StudentCreateView

urlpatterns = [
  path('list', student_list, name='student-list'),
  path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
  path('create/', StudentCreateView.as_view(), name='student-create'),
  path('<int:pk>/update/', StudentUpdateView.as_view(), name='student-update'),
  path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student-delete'),

  #path('upload/', student_bulk_upload, name='student-upload'),

]
