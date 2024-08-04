from django.shortcuts import render, redirect
from .models import Question, Option, Response
from django.http import HttpResponse
import matplotlib.pyplot as plt
from collections import defaultdict
import io
import urllib, base64

def survey_view(request, page=1):
    questions = Question.objects.all()[(page-1)*5:page*5]
    if request.method == 'POST':
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option:
                Response.objects.create(option_id=selected_option)
        if page < 4:
            return redirect('survey', page=page+1)
        else:
            return redirect('results')
    return render(request, 'survey.html', {'questions': questions, 'page': page})

def results_view(request):
    responses = Response.objects.all()
    trait_counts = defaultdict(int)

    traits = {
        "Neuroticism": ["Very Accurate", "Moderately Accurate"],
        "Extraversion": ["Very Accurate"],
        "Openness to Experience": ["Very Accurate", "Moderately Accurate", "Neither Accurate Nor Inaccurate"],
        "Agreeableness": ["Very Inaccurate", "Moderately Inaccurate"],
        "Conscientiousness": ["Moderately Inaccurate", "Very Inaccurate", "Neither Accurate Nor Inaccurate"]
    }

    for response in responses:
        option_text = response.option.text
        for trait, relevant_responses in traits.items():
            if option_text in relevant_responses:
                trait_counts[trait] += 1

    labels = list(trait_counts.keys())
    counts = list(trait_counts.values())
    colors = ['purple', 'blue', 'pink', 'yellow', 'green']

    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color=colors)
    plt.xlabel('Personality Traits')
    plt.ylabel('Count')
    plt.title('Survey Responses by Personality Traits')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'results.html', {'data': uri})

