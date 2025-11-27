from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.db.models import Q, Count, Avg
from .models import Note, Review
from .forms import SignUpForm, LoginForm, NoteUploadForm, ReviewForm


def home(request):
    """Home page view showing recent notes and statistics."""
    recent_notes = Note.objects.all()[:6]
    total_notes = Note.objects.count()
    total_downloads = sum(note.download_count for note in Note.objects.all())
    
    context = {
        'recent_notes': recent_notes,
        'total_notes': total_notes,
        'total_downloads': total_downloads,
    }
    return render(request, 'home.html', context)


def note_list(request):
    """List all notes with filtering and search."""
    notes = Note.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        notes = notes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(subject__icontains=search_query)
        )
    
    # Filter by branch
    branch_filter = request.GET.get('branch', '')
    if branch_filter:
        notes = notes.filter(branch=branch_filter)
    
    # Filter by year
    year_filter = request.GET.get('year', '')
    if year_filter:
        notes = notes.filter(year=year_filter)
    
    context = {
        'notes': notes,
        'search_query': search_query,
        'branch_filter': branch_filter,
        'year_filter': year_filter,
        'branch_choices': Note.BRANCH_CHOICES,
        'year_choices': Note.YEAR_CHOICES,
    }
    return render(request, 'notes/note_list.html', context)


def note_detail(request, pk):
    """Detail view for a single note with reviews."""
    note = get_object_or_404(Note, pk=pk)
    reviews = note.reviews.all()
    
    # Handle review submission
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            existing_review = Review.objects.filter(note=note, user=request.user).first()
            if existing_review:
                messages.warning(request, 'You have already reviewed this note.')
            else:
                review = review_form.save(commit=False)
                review.note = note
                review.user = request.user
                review.save()
                messages.success(request, 'Review added successfully!')
                return redirect('note_detail', pk=pk)
    else:
        review_form = ReviewForm()
    
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(note=note, user=request.user).exists()
    
    context = {
        'note': note,
        'reviews': reviews,
        'review_form': review_form,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'notes/note_detail.html', context)


import os

@login_required
def download_note(request, pk):
    """Download a note file and increment download count."""
    note = get_object_or_404(Note, pk=pk)
    
    note.download_count += 1
    note.save()
    
    try:
        return FileResponse(note.file.open('rb'), as_attachment=True, filename=os.path.basename(note.file.name))
    except Exception as e:
        messages.error(request, f'Error downloading file: {str(e)}')
        return redirect('note_detail', pk=pk)


@login_required
def upload_note(request):
    """Upload a new note (requires authentication)."""
    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploader = request.user
            note.save()
            messages.success(request, 'Note uploaded successfully!')
            return redirect('dashboard')
    else:
        form = NoteUploadForm()
    
    return render(request, 'notes/upload_note.html', {'form': form})


@login_required
def dashboard(request):
    """User dashboard showing their uploaded notes and statistics."""
    user_notes = Note.objects.filter(uploader=request.user)
    total_uploads = user_notes.count()
    total_downloads = sum(note.download_count for note in user_notes)
    user_reviews = Review.objects.filter(user=request.user)
    
    context = {
        'user_notes': user_notes,
        'total_uploads': total_uploads,
        'total_downloads': total_downloads,
        'user_reviews': user_reviews,
    }
    return render(request, 'notes/dashboard.html', context)


def signup_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def delete_note(request, pk):
    """Delete a note uploaded by the current user."""
    note = get_object_or_404(Note, pk=pk)
    
    if request.user != note.uploader:
        messages.error(request, 'You are not authorized to delete this note.')
        return redirect('note_detail', pk=pk)
    
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully.')
        return redirect('dashboard')
    
    return redirect('note_detail', pk=pk)
