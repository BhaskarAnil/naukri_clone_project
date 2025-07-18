from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import Company
from .models import CompanyReview, ReviewReply, ReviewLike
from .forms import CompanyReviewForm


@login_required(login_url='login')
def employer_reviews_view(request):
    user = request.user
    if not user.is_employer:
        return redirect('home')

    company = getattr(user, 'company', None)
    if not company:
        return redirect('employer_profile')

    reviews = company.reviews.select_related('user').prefetch_related('replies__user', 'likes').all()
    liked_review_ids = set(ReviewLike.objects.filter(user=user, review__in=reviews).values_list('review_id', flat=True))
    for review in reviews:
        review.user_has_liked = review.review_id in liked_review_ids

    employer_name = user.username
    initials = ''.join([x[0] for x in employer_name.split()]).upper()[:2]

    return render(request, 'reviews/employer_reviews.html', {
        'company': company,
        'reviews': reviews,
        'employer_name': employer_name,
        'employer_initials': initials,
    })


@login_required(login_url='login')
def companies_reviews_view(request, company_id):
    user = request.user
    jobseeker_name = user.username
    initials = ''.join([x[0] for x in jobseeker_name.split()]).upper()[:2]
    company = get_object_or_404(Company, pk=company_id)
    reviews = CompanyReview.objects.filter(company=company).select_related('user').prefetch_related('replies__user', 'likes')
    user_review = reviews.filter(user=user).first()
    other_reviews = reviews.exclude(user=user)
    liked_review_ids = set(ReviewLike.objects.filter(user=user, review__in=other_reviews).values_list('review_id', flat=True))
    for review in other_reviews:
        review.user_has_liked = review.review_id in liked_review_ids

    add_form = None
    edit_form = None

    if user_review:
        if request.method == 'POST':
            edit_form = CompanyReviewForm(request.POST, instance=user_review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('reviews', company_id=company.company_id)
        else:
            edit_form = CompanyReviewForm(instance=user_review)
    else:
        if request.method == 'POST':
            add_form = CompanyReviewForm(request.POST)
            if add_form.is_valid():
                new_review = add_form.save(commit=False)
                new_review.user = user
                new_review.company = company
                new_review.save()
                return redirect('reviews', company_id=company.company_id)
        else:
            add_form = CompanyReviewForm()

    return render(request, 'reviews/reviews_view.html', {
        'company': company,
        'reviews': reviews,
        'user_review': user_review,
        'other_reviews': other_reviews,
        'add_form': add_form,
        'edit_form': edit_form,
        'jobseeker_name': jobseeker_name,
        'jobseeker_initials': initials,
    })


@login_required(login_url='login')
def add_reply(request, review_id):
    review = get_object_or_404(CompanyReview, pk=review_id)
    reply_text = request.POST.get('reply_text', '').strip()
    if reply_text:
        ReviewReply.objects.create(
            review=review,
            user=request.user,
            reply_text=reply_text
        )
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('reviews', company_id=review.company.company_id)



@login_required(login_url='login')
def like_review(request, review_id):
    review = get_object_or_404(CompanyReview, pk=review_id)
    ReviewLike.objects.get_or_create(review=review, user=request.user)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('reviews', company_id=review.company.company_id)



@login_required(login_url='login')
def unlike_review(request, review_id):
    review = get_object_or_404(CompanyReview, pk=review_id)
    ReviewLike.objects.filter(review=review, user=request.user).delete()
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('reviews', company_id=review.company.company_id)


@login_required(login_url='login')
def delete_review(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    review = CompanyReview.objects.filter(company=company, user=request.user).first()
    if review:
        review.delete()
    return redirect('reviews', company_id=company_id)
    return redirect(request.META.get('HTTP_REFERER', reverse('explore_jobs')))

