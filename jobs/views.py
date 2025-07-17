from django.contrib.auth.decorators import login_required
from jobs.models import Job
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from jobs.forms import JobForm
from profiles.models import Company
from django.urls import reverse
from django.db.models import Count
from jobs.models import SavedJob, LikedJob, DislikedJob, Application

@login_required(login_url='login')
def employer_jobs_view(request):
    user = request.user
    employer_name = user.username
    initials = ''.join([x[0] for x in employer_name.split()]).upper()[:2]
    jobs = Job.objects.filter(company__user=user).annotate(likes_count=Count('liked_by'), applications_count=Count('applications'))
    return render(request, 'jobs/my_jobs.html', {'user': user, 'jobs': jobs, 'employer_name': employer_name, 'employer_initials': initials})


@login_required(login_url='login')
def add_job_view(request):
    user = request.user
    employer_name = user.username
    initials = ''.join([x[0] for x in employer_name.split()]).upper()[:2]
    company = Company.objects.filter(user=user).first()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.is_active = True  
            job.save()
            return redirect('employer_jobs')
    else:
        form = JobForm()
    return render(request, 'jobs/add_job.html', {'form': form, 'user': user, 'employer_name': employer_name, 'employer_initials': initials})


@login_required(login_url='login')
def delete_job_view(request, job_id):
    user = request.user
    job = get_object_or_404(Job, pk=job_id, company__user=user)
    job.delete()
    return redirect('employer_jobs')


# edit job view for employers
@login_required(login_url='login')
def edit_job_view(request, job_id):
    user = request.user
    employer_name = user.username
    initials = ''.join([x[0] for x in employer_name.split()]).upper()[:2]
    job = get_object_or_404(Job, pk=job_id, company__user=user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer_jobs')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/add_job.html', {
        'form': form,
        'user': user,
        'edit_mode': True,
        'job': job
    , 'employer_name': employer_name, 'employer_initials': initials})

@login_required(login_url='login')
def explore_jobs_view(request):
    jobs = Job.objects.order_by('-posted_at')
    user = request.user
    jobseeker_name = user.username
    initials = ''.join([x[0] for x in jobseeker_name.split()]).upper()[:2]
    filter_type = request.GET.get('filter', 'all')
    job_ids = [job.job_id for job in jobs]
    applied_ids = set(Application.objects.filter(user=user, job_id__in=job_ids).values_list('job_id', flat=True))
    saved_ids = set(SavedJob.objects.filter(user=user, job_id__in=job_ids).values_list('job_id', flat=True))
    liked_ids = set(LikedJob.objects.filter(user=user, job_id__in=job_ids).values_list('job_id', flat=True))
    disliked_ids = set(DislikedJob.objects.filter(user=user, job_id__in=job_ids).values_list('job_id', flat=True))
    if filter_type == 'applied':
        jobs = Job.objects.filter(job_id__in=applied_ids).order_by('-posted_at')
    elif filter_type == 'saved':
        jobs = Job.objects.filter(job_id__in=saved_ids).order_by('-posted_at')
    elif filter_type == 'liked':
        jobs = Job.objects.filter(job_id__in=liked_ids).order_by('-posted_at')
    elif filter_type == 'disliked':
        jobs = Job.objects.filter(job_id__in=disliked_ids).order_by('-posted_at')
    else:
        jobs = Job.objects.all().order_by('-posted_at')
    for job in jobs:
        job.is_applied = job.job_id in applied_ids
        job.is_saved = job.job_id in saved_ids
        job.is_liked = job.job_id in liked_ids
        job.is_disliked = job.job_id in disliked_ids
    return render(request, 'jobs/explore_jobs.html', {'jobs': jobs, 'user': user,'filter_type': filter_type, 'jobseeker_name': jobseeker_name, 'jobseeker_initials': initials})
@login_required(login_url='login')
def save_job_view(request, job_id):
    user = request.user
    job = get_object_or_404(Job, pk=job_id)
    SavedJob.objects.get_or_create(user=user, job=job)
    return redirect(request.META.get('HTTP_REFERER', reverse('explore_jobs')))

@login_required(login_url='login')
def unsave_job_view(request, job_id):
    user = request.user
    job = get_object_or_404(Job, pk=job_id)
    SavedJob.objects.filter(user=user, job=job).delete()
    return redirect(request.META.get('HTTP_REFERER', reverse('explore_jobs')))

@login_required(login_url='login')
def like_job_view(request, job_id):
    user = request.user
    job = get_object_or_404(Job, pk=job_id)
    LikedJob.objects.get_or_create(user=user, job=job)
    DislikedJob.objects.filter(user=user, job=job).delete()
    return redirect(request.META.get('HTTP_REFERER', reverse('explore_jobs')))

@login_required(login_url='login')
def dislike_job_view(request, job_id):
    user = request.user
    job = get_object_or_404(Job, pk=job_id)
    DislikedJob.objects.get_or_create(user=user, job=job)
    LikedJob.objects.filter(user=user, job=job).delete()
    return redirect(request.META.get('HTTP_REFERER', reverse('explore_jobs')))

@login_required(login_url='login')
def apply_job_view(request, job_id):
    user = request.user
    job = get_object_or_404(Job, pk=job_id)
    Application.objects.get_or_create(user=user, job=job)
    return redirect(request.META.get('HTTP_REFERER', reverse('explore_jobs')))
@login_required(login_url='login')
def applications_view(request,job_id):
    employer_name = request.user.username
    initials = ''.join([x[0] for x in employer_name.split()]).upper()[:2]
    job = get_object_or_404(Job,pk=job_id)
    applications = Application.objects.filter(job=job).select_related('user__profile')
    return render(request, 'jobs/applications.html', {'applications': applications, 'employer_name': employer_name, 'employer_initials': initials})