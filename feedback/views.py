from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .utils import get_sentiment
from .models import Feedback

def home(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.sentiment = get_sentiment(feedback.text)
            feedback.save()
            return redirect('thank_you')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/home.html', {'form': form})

def thank_you(request):
    return render(request, 'feedback/thank_you.html')
