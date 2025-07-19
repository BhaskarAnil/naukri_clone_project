# Explore Companies view for jobseekers
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm, ProfileForm, CompanyForm
from .models import Company, CompanyFollows
from jobs.models import Application, Job, SavedJob
from reviews.models import CompanyReview
from .forms import RegisterForm, LoginForm, ProfileForm, CompanyForm
# register view

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
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
    user = request.user
    company = getattr(user, 'company', None)
    job_post_count = Job.objects.filter(company=company).count()
    total_applications = Application.objects.filter(
        job__company=company).count()
    followers_count = CompanyFollows.objects.filter(company=company).count()
    context = {
        'employer_name': employer_name,
        'employer_initials': initials,
        'job_post_count': job_post_count,
        'total_applications': total_applications,
        'followers_count': followers_count,
    }
    return render(request, 'profiles/employer_home.html', context)

# jobseeker home view


@login_required(login_url='login')
def home_view(request):
    user = request.user
    saved_jobs_count = SavedJob.objects.filter(user=user).count()
    applied_jobs_count = Application.objects.filter(user=user).count()
    jobseeker_name = user.username

    initials = ''.join([x[0] for x in jobseeker_name.split()]).upper()[:2]
    return render(request, 'profiles/home.html', {'jobseeker_name': jobseeker_name, 'jobseeker_initials': initials, 'saved_jobs_count': saved_jobs_count, 'applied_jobs_count': applied_jobs_count})

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
        'profile': profile, 'jobseeker_name': jobseeker_name, 'jobseeker_initials': initials,
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
# explore companies view


def companies_view(request):
    user = request.user
    jobseeker_name = user.username
    initials = ''.join([x[0] for x in jobseeker_name.split()]).upper()[:2]
    if not request.user.is_authenticated or getattr(request.user, 'is_employer', False):
        return redirect('home')
    companies = Company.objects.all()
    company_ids = [company.company_id for company in companies]
    followed_companies_ids = set(CompanyFollows.objects.filter(
        user=user, company_id__in=company_ids).values_list('company_id', flat=True))
    for company in companies:
        company.is_followed = company.company_id in followed_companies_ids
    return render(request, 'profiles/companies.html', {'companies': companies, 'jobseeker_name': jobseeker_name, 'jobseeker_initials': initials, })
# follow companies view


@login_required(login_url='login')
def companies_follow_view(request, company_id):
    user = request.user
    company = get_object_or_404(Company, pk=company_id)
    CompanyFollows.objects.get_or_create(user=user, company=company)
    return redirect(request.META.get('HTTP_REFERER', reverse('companies')))
# unfollow companies view


@login_required(login_url='login')
def companies_unfollow_view(request, company_id):
    user = request.user
    company = get_object_or_404(Company, pk=company_id)
    CompanyFollows.objects.filter(user=user, company=company).delete()
    return redirect(request.META.get('HTTP_REFERER', reverse('companies')))
