from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Home / Dashboard
    path('', views.dashboard_view, name='home'),

    # User profile
    path('profile/', views.user_profile_view, name='user_profile'),

    # Tasks
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task_view, name='create_task'),
    path('tasks/complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),

    # Workouts
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/create/', views.create_workout, name='create_workout'),
    path('workouts/edit/<int:workout_id>/', views.edit_workout, name='edit_workout'),
    path('workouts/delete/<int:workout_id>/', views.delete_workout, name='delete_workout'),

    # Body Stats
    path('body-stats/', views.body_stats_list, name='body_stat_list'),
    path('body-stats/add/', views.add_body_stats, name='add_body_stat'),
    path('body-stats/edit/<int:stat_id>/', views.edit_body_stat, name='edit_body_stat'),
    path('body-stats/delete/<int:stat_id>/', views.delete_body_stat, name='delete_body_stat'),
]