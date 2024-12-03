from django.shortcuts import render
from .models import Word
import random

def typing_test(request):
    words = list(Word.objects.all())
    selected_words = random.sample(words, 10)  # Select 10 random words
    return render(request, 'tutor/typing_test.html', {'words': selected_words})