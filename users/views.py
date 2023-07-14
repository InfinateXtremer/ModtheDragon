from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect,render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Author
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            Author_instance = Author.objects.create(user=user_instance, display_name=user_instance.username)
            Author_instance.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Welcome {username}, Your account is created')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profilepage(request):
    return render(request,'users/profile.html')


