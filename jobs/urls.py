from django.urls import path
from jobs.views import (
    employer_jobs_view, add_job_view, edit_job_view, delete_job_view, explore_jobs_view,
    save_job_view, unsave_job_view, like_job_view, dislike_job_view, apply_job_view,applications_view
)

urlpatterns = [
    path('employer/jobs/', employer_jobs_view, name='employer_jobs'),
    path('employer/jobs/add/', add_job_view, name='add_job'),
    path('employer/jobs/<int:job_id>/edit/', edit_job_view, name='edit_job'),
    path('employer/jobs/<int:job_id>/delete/', delete_job_view, name='delete_job'),
    path('employer/jobs/<int:job_id>/applications/', applications_view, name='view_applications'),
    path('explore-jobs/', explore_jobs_view, name='explore_jobs'),
    path('jobs/<int:job_id>/save/', save_job_view, name='save_job'),
    path('jobs/<int:job_id>/unsave/', unsave_job_view, name='unsave_job'),
    path('jobs/<int:job_id>/like/', like_job_view, name='like_job'),
    path('jobs/<int:job_id>/dislike/', dislike_job_view, name='dislike_job'),
    path('jobs/<int:job_id>/apply/', apply_job_view, name='apply_job'),
]
