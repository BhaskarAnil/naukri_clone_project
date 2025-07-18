from profiles.models import Company, User
from django.db import models

class CompanyReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id', related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', related_name='company_reviews')
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('company', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} review for {self.company.company_name}"


class ReviewReply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    review = models.ForeignKey(CompanyReview, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_replies')
    reply_text = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply by {self.user.username} on review {self.review_id}"


class ReviewLike(models.Model):
    like_id = models.AutoField(primary_key=True)
    review = models.ForeignKey(CompanyReview, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')

    def __str__(self):
        return f"{self.user.username} liked review {self.review_id}"


