from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class UserAccount(AbstractUser):
    user_id=models.BigAutoField(primary_key=True)
    email=models.EmailField(unique=True)
    user_name=models.CharField(max_length=150, unique=True)
    phone=models.CharField(max_length=20, unique=True)
    password=models.CharField(max_length=128)

    def __str__(self):
        return self.user_name
    
class UserProfile(models.Model):
    user=models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    age=models.PositiveIntegerField()
    weight=models.FloatField()
    height=models.FloatField()
    BMI=models.FloatField()
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_name}'s Profile"
    
class Task(models.Model):
    task_id=models.BigAutoField(primary_key=True)
    user_id=models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    description=models.TextField()
    priority=models.CharField(max_length=50) # user sets priority of the task(e.g;high,medium, low,etc)
    created_at=models.DateTimeField(auto_now_add=True) # automatically added when task is created
    category=models.CharField(max_length=100) # user defined category for the task (e.g., work, personal, workout, etc.)
    completed=models.BooleanField(default=False) #indicates whether the task is completed or not
    due_date=models.DateTimeField() #user set due date for the task 

    def __str__(self):
        return self.title
    
class Workout(models.Model):
    task_id=models.ForeignKey(Task, on_delete=models.CASCADE) # workout is part of tasks
    user_id=models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    workout_id=models.BigAutoField(primary_key=True)
    workout_type=models.CharField(max_length=100) # user defined type of workout (e.g., cardio, yoga, etc.)
    duration=models.PositiveIntegerField() # duration of the workout in minutes
    calories_burned=models.FloatField() # estimated calories burned during the workout
    date=models.DateTimeField(auto_now_add=True) # automatically added when workout is created

    def __str__(self):
        return f"{self.workout_type} - {self.user_id.user_name}"
    
class Bodystats(models.Model):
    user_id=models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    recorded_date=models.DateField(auto_now_add=True) # automatically added when body stats are recorded
    weight=models.FloatField() # weight of the user at the time of recording body stats
    height=models.FloatField() # height of the user at the time of recording body stats
    BMI=models.FloatField() # BMI based on weight and height at the time of recording body stats

    def __str__(self):
        return f"{self.user_id.user_name}'s Body Stats on {self.recorded_date}"