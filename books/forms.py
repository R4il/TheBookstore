from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'body', 'anonymous']
        labels = {
            'title': 'The review Title',
            'anonymous': 'Do you wish to remain anonymous?',
        }
        help_texts = {
            'rating': '1-5 rating.',
            'anonymous': 'shhhh?',
        }
        error_messages = {
            'rating': {
                'max_length': "Please, input a number between 1 and 5.",
            },
        }

    def clean_rating(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get("rating") > 5 or cleaned_data.get("rating") < 0:
            raise forms.ValidationError("Rating most be between 0 and 5")
        return cleaned_data['rating']
