from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate, logout 
from .models import UserAccount,  UserProfile, Task, Workout, Bodystats
from django.shortcuts import get_object_or_404

# Create your views here.

# Signup view to create a new user account and log the user in
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Create a new user account
        user = UserAccount.objects.create_user(username=username, password=password, email=email, phone=phone)
        user.save()

        # Log the user in and redirect to the home page
        login(request, user)
        return redirect('home')

    return render(request, 'task_and_fitness_app/signup.html')   

# Login view to authenticate the user and log them in
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'task_and_fitness_app/login.html', {'error': 'Invalid username or password'})

    return render(request, 'task_and_fitness_app/login.html')


# User profile view to display and update user profile information
@login_required
def user_profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        BMI = request.POST.get('BMI')

        UserProfile.objects.update_or_create(
            user=request.user, 
            defaults={
                'age':age,
                'weight':weight,
                'height':height,
                'BMI':BMI,
                }
        )

    return render(request, 'task_and_fitness_app/user_profile.html', {'user_profile': user_profile})

# logout view to log the user out and redirect to the login page
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_task_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        category = request.POST.get('category')
        created_at = request.POST.get('created_at')
        due_date = request.POST.get('due_date')
        completed = request.POST.get('completed', False)
        Task.objects.create(
            user_id=request.user,
            title=title,
            description=description,
            priority=priority,
            category=category,
            created_at=created_at,
            due_date=due_date,
            completed=False if not completed else True
        )
        return redirect('task_list')

    return render(request, 'task_and_fitness_app/create_task.html')

# list tasks 
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    return render(request, 'task_and_fitness_app/task_list.html', {'tasks': tasks})

@login_required
def create_workout(request):
    task = Task.objects.filter(user=request.user)

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        workout_type = request.POST.get('workout_type')
        duration = request.POST.get('duration')
        calories_burned = request.POST.get('calories_burned')

        task = Task.objects.get(task_id=task_id, user=request.user)

        Workout.objects.create(
            user=request.user,
            task_id=task,
            workout_type=workout_type,
            duration=duration,
            calories_burned=calories_burned
        )
        return redirect('workout_list')

    return render(request, 'task_and_fitness_app/create_workout.html', {'tasks': task})

@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user).order_by('-date')
    return render(request, 'task_and_fitness_app/workout_list.html', {'workouts': workouts})

@login_required
def add_body_stats(request):
    if request.method == 'POST':
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        #BMIformula: weight (kg) / (height (m)^2)
        height_in_m = height / 100
        BMI = weight / (height_in_m ** 2)


        Bodystats.objects.create(
            user=request.user,
            weight=weight,
            height=height,
            BMI=round(BMI, 2)
        )
        return redirect('body_stats_list')

    return render(request, 'task_and_fitness_app/add_body_stats.html')

#list body stats
@login_required
def body_stats_list(request):
    body_stats = Bodystats.objects.filter(user=request.user).order_by('-recorded_date')
    return render(request, 'task_and_fitness_app/body_stats_list.html', {'body_stats': body_stats})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('task_list')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.due_date = request.POST.get("due_date")
        task.save()
        return redirect("task_list")

    return render(request, "task_and_fitness_app/edit_task.html", {"task": task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "task_and_fitness_app/delete_task.html", {"task": task})


@login_required
def edit_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    tasks = Task.objects.filter(user=request.user)

    if request.method == "POST":
        task_id = request.POST.get("task")
        workout.workout_type = request.POST.get("workout_type")
        workout.duration = request.POST.get("duration")
        workout.calories_burned = request.POST.get("calories_burned")
        workout.task = Task.objects.get(id=task_id, user=request.user)
        workout.save()
        return redirect("workout_list")

    return render(request, "task_and_fitness_app/edit_workout.html", {"workout": workout, "tasks": tasks})


@login_required
def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)

    if request.method == "POST":
        workout.delete()
        return redirect("workout_list")

    return render(request, "task_and_fitness_app/delete_workout.html", {"workout": workout})

@login_required
def edit_body_stat(request, stat_id):
    stat = get_object_or_404(Bodystats, id=stat_id, user=request.user)

    if request.method == "POST":
        weight = float(request.POST.get("weight"))
        height = float(request.POST.get("height"))
        height_in_m = height / 100
        bmi = weight / (height_in_m ** 2)

        stat.weight = weight
        stat.height = height
        stat.bmi = round(bmi, 2)
        stat.save()

        return redirect("body_stat_list")

    return render(request, "task_and_fitness_app/edit_body_stat.html", {"stat": stat})


@login_required
def delete_body_stat(request, stat_id):
    stat = get_object_or_404(Bodystats, id=stat_id, user=request.user)

    if request.method == "POST":
        stat.delete()
        return redirect("body_stat_list")

    return render(request, "task_and_fitness_app/delete_body_stat.html", {"stat": stat})

@login_required
def dashboard_view(request):
    user = request.user

    tasks = Task.objects.filter(user=user).order_by("due_date")
    workouts = Workout.objects.filter(user=user).order_by("-date")
    body_stats = Bodystats.objects.filter(user=user).order_by("-recorded_date")

    # Latest body stat
    latest_stat = body_stats.first() if body_stats.exists() else None

    context = {
        "tasks": tasks,
        "workouts": workouts,
        "body_stats": body_stats,
        "latest_stat": latest_stat
    }
    return render(request, "task_and_fitness_app/dashboard.html", context)