from django.urls import path
from .views import employer_reviews_view, companies_reviews_view, delete_review, add_reply, like_review, unlike_review

urlpatterns = [
    path('employer/reviews/', employer_reviews_view, name='employer_reviews'),
    path('companies/<int:company_id>/reviews/', companies_reviews_view, name='reviews'),
    path('companies/<int:company_id>/reviews/delete/', delete_review, name='delete_review'),
    path('reviews/<int:review_id>/reply/', add_reply, name='add_reply'),
    path('reviews/<int:review_id>/like/', like_review, name='like_review'),
    path('reviews/<int:review_id>/unlike/', unlike_review, name='unlike_review'),
]

