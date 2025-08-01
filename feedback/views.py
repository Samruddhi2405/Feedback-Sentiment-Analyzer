from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Count
from .forms import FeedbackForm
from .utils import get_sentiment
from .models import Feedback
from datetime import timedelta

def home(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.sentiment = get_sentiment(feedback.text)
            feedback.created_at = timezone.now()
            feedback.save()
            return redirect('thank_you')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/home.html', {'form': form})

def thank_you(request):
    return render(request, 'feedback/thank_you.html')

def dashboard(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')

    sentiment_counts = (
        feedbacks.values('sentiment')
        .annotate(count=Count('sentiment'))
        .order_by()
    )

    last_7_days = timezone.now() - timedelta(days=7)
    feedbacks_last_week = feedbacks.filter(created_at__gte=last_7_days)
    daily_counts = (
        feedbacks_last_week.extra({'day': "date(created_at)"}).values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    return render(request, 'feedback/dashboard.html', {
        'feedbacks': feedbacks,
        'sentiment_counts': sentiment_counts,
        'daily_counts': daily_counts,
    })
