from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import FileUploadForm
from .models import UploadedFile
from .pdf_utils import extract_text_from_pdf
from .utils import summarize_with_bart, calculate_stats, generate_word_frequency_plot, generate_sentence_length_distribution_plot
import re
from django.shortcuts import render

from .utils import (
    summarize_with_bart,
    calculate_stats,
    generate_word_frequency_plot,
    generate_sentence_length_distribution_plot,
    calculate_rouge_score,
)
def viewer(request, pk):
    return render(request, 'core/viewer.html', {'pk': pk})
# core/views.py
from django.shortcuts import render

def analyze(request, pk):
    # Add your logic to analyze the document using pk
    return render(request, 'core/analyze.html', {'pk': pk})


def home(request):
    summary = None
    file_error = None
    word_count = sentence_count = 0
    word_freq_plot = sentence_length_plot = None
    original_text = ""
    summary_ratio = 0.0
    rouge_scores = {}
    original_length = summary_length = 0

    if request.method == "POST":
        text_input = request.POST.get("text_input", "")
        action = request.POST.get("action", "")
        doc_file = request.FILES.get("doc_file")
        user_role = request.POST.get("user_role", "")

        if action == "personalized":
            if text_input:
                original_text = text_input
            elif doc_file and doc_file.name.endswith(".pdf"):
                uploaded = UploadedFile(file=doc_file)
                uploaded.save()
                original_text = extract_text_from_pdf(uploaded.file.path)
            else:
                file_error = "Please provide either text input or a PDF file."

            if original_text:
                summary = summarize_with_bart(original_text)
                word_count, sentence_count = calculate_stats(summary)
                word_freq_plot = generate_word_frequency_plot(original_text)
                sentence_length_plot = generate_sentence_length_distribution_plot(original_text)

                # Length stats
                original_length = len(original_text)
                summary_length = len(summary)
                summary_ratio = round(summary_length / original_length, 2) if original_length else 0.0

                # ROUGE scores
                rouge_scores = calculate_rouge_score(original_text, summary)

    context = {
        "summary": summary,
        "file_error": file_error,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "word_freq_plot": word_freq_plot,
        "sentence_length_plot": sentence_length_plot,
        "original_text": original_text,
        "summary_ratio": summary_ratio,
        "rouge_scores": rouge_scores,
        "original_length": original_length,
        "summary_length": summary_length,
    }

    return render(request, "core/home.html", context)
