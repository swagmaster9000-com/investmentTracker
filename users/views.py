from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import SignUpForm

User = get_user_model()

# ---------- SIGNUP ----------
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)   # create session
            return redirect('dashboard')

        return render(request, "users/signup.html", {"form": form})

    form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


# ---------- LOGIN ----------
def login_view(request):
    error = None

    if request.method == "POST":
        identifier = request.POST.get("username")
        password = request.POST.get("password")

        # Try username first
        user = authenticate(request, username=identifier, password=password)

        # Try email fallback
        if user is None:
            try:
                real_user = User.objects.get(email=identifier)
                user = authenticate(request, username=real_user.username, password=password)
            except User.DoesNotExist:
                user = None

        # DEBUG
        print("AUTH RESULT:", user)

        # If authentication succeeded
        if user is not None:
            login(request, user)
            return redirect("dashboard")

        error = "Invalid username, email, or password."

    return render(request, "users/login.html", {"error": error})



# ---------- LOGOUT ----------
def logout_view(request):
    logout(request)
    return redirect('/users/login/')


# ---------- FORGOT PASSWORD ----------
def forgot_password(request):
    if request.method == 'POST':
        identifier = request.POST.get('username')

        # Try username or email
        user = (
            User.objects.filter(username=identifier).first() or
            User.objects.filter(email=identifier).first()
        )

        if user:
            return redirect('reset_password', username=user.username)
        else:
            messages.error(request, 'User not found.')

    return render(request, 'users/forgot_password.html')


# ---------- RESET PASSWORD ----------
def reset_password(request, username):
    user = User.objects.filter(username=username).first()

    if not user:
        return render(request, 'users/reset_password.html', {"error": "Invalid user"})

    if request.method == "POST":
        new_password = request.POST.get('password')
        user.set_password(new_password)
        user.save()

        messages.success(request, "Password reset successfully.")
        return redirect('login')

    return render(request, 'users/reset_password.html', {"username": username})
