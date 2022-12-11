from django.urls import path, include
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, Login, RegisterPage, UserPasswordChangeView, UserPasswordChangeDoneView, update_profile
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', update_profile, name='profile'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('change-password/', UserPasswordChangeView.as_view(), name='password-change-view'),
    path('change-password/done/', UserPasswordChangeDoneView.as_view(), name='password-change-done-view'),   
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name='task-delete'),
]   +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)