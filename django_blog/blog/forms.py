from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):

    tags = forms.CharField(
        required=False,
        help_text="Separate tags with commas (e.g., 'django, web development, python')"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
    
    def __init__(self, *args, **kwargs):
        """ Prepopulate tags when editing a post """
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # If updating a post
            self.fields['tags'].initial = ', '.join(tag.name for tag in self.instance.tags.all())

    def save(self, commit=True):
        """ Override save to handle tags """
        post = super().save(commit=False)
        tags_list = [tag.strip() for tag in self.cleaned_data['tags'].split(',') if tag.strip()]  # ✅ Clean input
        post.save()  # Save post first
        post.tags.set(tags_list)  # ✅ Assign tags
        return post

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

    def clean_text(self):
        content = self.cleaned_data.get('content')
        if len(content) < 5:
            raise forms.ValidationError("comment must be at least 5 characters long.")
        return content