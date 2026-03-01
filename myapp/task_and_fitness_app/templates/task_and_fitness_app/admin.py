from django.contrib import admin
from .models import UserAccount, UserProfile, Task, Workout, Bodystats

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(Workout)
admin.site.register(Bodystats)