from django.shortcuts import render, redirect
from .models import Feedback
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .forms import FeedbackForm
from .utils import get_sentiment

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
    # Fetch all feedback
    feedbacks = Feedback.objects.all().order_by('-created_at')

    # Sentiment counts (Pie chart)
    sentiment_counts_qs = Feedback.objects.values('sentiment').annotate(count=Count('sentiment'))
    sentiment_counts = list(sentiment_counts_qs)

    # Daily feedback count (Line chart for last 7 days)
    today = timezone.now().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    daily_counts = []

    for day in last_7_days:
        count = Feedback.objects.filter(created_at__date=day).count()
        daily_counts.append({'day': day.strftime("%Y-%m-%d"), 'count': count})

    return render(request, 'feedback/dashboard.html', {
        'feedbacks': feedbacks,
        'sentiment_counts': sentiment_counts,
        'daily_counts': daily_counts,
    })
