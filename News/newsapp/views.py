from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import NewsPost

def home(request):
    news_posts = NewsPost.objects.all().order_by('-uploaded_at')  # Fetch all posts, newest first
    return render(request, 'home.html', {'news_posts': news_posts})

def signup(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validation: Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('signup')

        # Create a new user
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # Automatically log the user in after signup
        authenticate(request, username=username, password=password1)
        login(request, user)

        messages.success(request, "Your account has been created successfully. You are now logged in.")
        return redirect('home')  # Redirect to home page after signup and login

    return render(request, 'auth/signup.html')


def logins(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=user_name, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'auth/login.html')

############### LOGOUT ###############3
    
def logouts(request):
    logout(request)
    return redirect('login')



########## New Post ###############


@login_required
def newPost(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        
        NewsPost.objects.create(user=user, title=title, desc=desc)
        messages.success(request, "Post Uploaded Successfully")
        
        return redirect('newpost')
        
        
    return render(request, 'new_post.html')


############## Display details of the news ##########################
@login_required
def news_detail(request, pk):
    news = get_object_or_404(NewsPost, pk=pk)
    return render(request, "news_details.html", {'news':news})



@login_required
def uploadedPost(request):
    # Retrieve the posts uploaded by the logged-in user
    uploaded_news = NewsPost.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # If the form is submitted, delete the post
        post_id = request.POST.get('delete_id')
        post = get_object_or_404(NewsPost, pk=post_id)

        # Check if the post belongs to the logged-in user
        if post.user == request.user:
            post.delete()
            messages.success(request, "Post deleted successfully.")
            return redirect('uploaded_post')  # Redirect to the uploaded posts page after deletion
        
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('uploaded_post')

    return render(request, 'uploaded_post.html', {'news': uploaded_news})



@login_required
def editPost(request, pk):
    # Retrieve the post to be edited
    post = get_object_or_404(NewsPost, pk=pk)

    # Check if the logged-in user is the owner of the post
    if post.user != request.user:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('uploaded_post')

    # Handle the POST request (form submission)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.desc = request.POST.get('desc')
        post.save()
        messages.success(request, "Post updated successfully.")
        return redirect('uploaded_post')

    return render(request, 'edit_post.html', {'post': post})