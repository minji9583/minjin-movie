from django import forms
from .models import Comment, Score

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ('score',)