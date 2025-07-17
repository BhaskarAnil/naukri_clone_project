
# Explore Companies view for jobseekers
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm, ProfileForm, CompanyForm
from .models import Profile, Company
from .forms import RegisterForm, LoginForm, ProfileForm, CompanyForm

# register view 
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            # if there are errors
            return render(request, 'profiles/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'profiles/register.html', {'form': form})
# employer registration view
def employer_register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form.fields['is_employer'].initial = True
        if form.is_valid():
            form.cleaned_data['is_employer'] = True
            form.save()
            return redirect('login')
        else:
            # Always show company_name field for employer registration
            form.fields['is_employer'].initial = True
            return render(request, 'profiles/employer_register.html', {'form': form})
    else:
        form = RegisterForm(initial={'is_employer': True})
    return render(request, 'profiles/employer_register.html', {'form': form})

# login view for jobseekers and employers
def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'is_employer') and request.user.is_employer:
            return redirect('employer_home')
        else:
            return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            user = form.cleaned_data['user']
            if hasattr(user, 'is_employer') and user.is_employer:
                return redirect('employer_home')
            else:
                return redirect('home')
        else:
            return render(request, 'profiles/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'profiles/login.html', {'form': form})
# employer home view
@login_required(login_url='login')
def employer_home_view(request):
    employer_name = request.user.username
    initials = ''.join([x[0] for x in employer_name.split()]).upper()[:2]
    context = {
        'employer_name': employer_name,
        'employer_initials': initials,
    }
    return render(request, 'profiles/employer_home.html', context)

# jobseeker home view
@login_required(login_url='login')
def home_view(request):
    jobseeker_name = request.user.username
    initials = ''.join([x[0] for x in jobseeker_name.split()]).upper()[:2]
    return render(request, 'profiles/home.html',{'jobseeker_name':jobseeker_name, 'jobseeker_initials':initials})

# logout view
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

# profile view for jobseekers
@login_required(login_url='login')
def profile_view(request):
    user = request.user
    jobseeker_name = user.username
    initials = ''.join([x[0] for x in jobseeker_name.split()]).upper()[:2]
    if user.is_employer:
        return redirect('employer_home')
    profile = getattr(user, 'profile', None)
    if request.method == 'POST':
        if 'delete' in request.POST:
            user.delete()
            return redirect('register')
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/profile.html', {
        'user': user,
        'form': form,
        'profile': profile,'jobseeker_name':jobseeker_name, 'jobseeker_initials':initials,
    })

# employer profile view
@login_required(login_url='login')
def employer_profile_view(request):
    user = request.user
    employer_name = user.username
    initials = ''.join([x[0] for x in employer_name.split()]).upper()[:2]
    if not user.is_employer:
        return redirect('profile')
    company = getattr(user, 'company', None)
    if not company:
        company = Company.objects.create(user=user)
    if request.method == 'POST':
        if 'delete' in request.POST:
            user.delete()
            return redirect('register')
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('employer_profile')
    else:
        form = CompanyForm(instance=company)
    context = {
        'employer_name': employer_name,
        'employer_initials': initials,
        'user': user,
        'form': form,
        'company': company,
    }
    return render(request, 'profiles/employer_profile.html', context)
def companies_view(request):
    user = request.user
    jobseeker_name = user.username
    initials = ''.join([x[0] for x in jobseeker_name.split()]).upper()[:2]
    if not request.user.is_authenticated or getattr(request.user, 'is_employer', False):
        return redirect('home')
    companies = Company.objects.all()
    return render(request, 'profiles/companies.html', {'companies': companies,'jobseeker_name':jobseeker_name, 'jobseeker_initials':initials,})