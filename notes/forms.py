from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Note, Review

class SignUpForm(UserCreationForm):
    """User registration form with email field."""
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class LoginForm(AuthenticationForm):
    """User login form."""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class NoteUploadForm(forms.ModelForm):
    """Form for uploading a new note."""
    
    class Meta:
        model = Note
        fields = ['title', 'description', 'branch', 'year', 'subject', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'year': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_file(self):
        """Validate file size and type."""
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 10MB.')
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed.')
        return file


class ReviewForm(forms.ModelForm):
    """Form for adding a review/rating to a note."""
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional: Share your thoughts...'}),
        }
