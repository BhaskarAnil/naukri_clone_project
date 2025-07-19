from django import forms
from .models import CompanyReview


class CompanyReviewForm(forms.ModelForm):
    review_text = forms.CharField(
        label='Your Review',
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Write your review...'
        })
    )

    class Meta:
        model = CompanyReview
        fields = ['review_text']
