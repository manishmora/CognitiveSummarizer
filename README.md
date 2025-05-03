# Cognitive Summarizer

## Project Overview

**Cognitive Summarizer** is a Django-based web application designed to automatically summarize technical reports and long documents. Leveraging powerful AI models, including **BART** and **Gemini**, the application condenses documents into concise summaries while retaining the most important details. It also provides detailed performance metrics and visualizations to evaluate the summarization process, making it an ideal tool for anyone working with large technical documents.

### Key Features:

- **AI-Powered Summarization**: Uses machine learning models to summarize long texts, focusing on retaining essential content.
- **Evaluation Metrics**: Provides performance metrics, such as ROUGE scores, and compares the lengths of the original and summarized text.
- **Interactive UI**: A clean and responsive interface designed with **Tailwind CSS** to provide an optimal user experience.
- **Document Viewer**: Displays the original document and the generated summary side by side.
- **Download and Copy**: Users can download the summarized text or copy it directly to their clipboard.
- **Error Handling**: Handles issues like empty document uploads gracefully, providing feedback to users.

---

## Installation Guide

To set up the **Cognitive Summarizer** locally, follow these steps:

### Prerequisites:

- **Python 3.x** (Recommended: Python 3.8 or higher)
- **pip** (Python package manager)
- **Django 5.x**
- **Git** (for version control)
- **A text editor** (e.g., Visual Studio Code, PyCharm)


Features and Functionality
1. Document Summarization
The core feature of the application is its ability to summarize documents using AI models. Users can upload documents (e.g., PDFs, text files) and receive a summary that highlights key points and content.

The application uses the BART model or Gemini (if integrated) for text summarization. You can easily switch between models or add new ones as required.

2. Evaluation Metrics
After summarization, the application provides a summary evaluation section, showing:

Original Text Length: Number of characters in the original document.

Summarized Text Length: Number of characters in the summarized text.

ROUGE Scores: A measure of the quality of the generated summary compared to a reference summary. ROUGE scores include precision, recall, and F1-score.

These metrics are shown in a dashboard-like view.

3. Visualizations
Word Frequency Distribution: A chart showing the frequency of the most common words in the original document.

Sentence Length Distribution: A visualization of the length of sentences in the original text.

These visualizations provide deeper insights into the structure and content of the document.

4. User Interface
The interface is designed with Tailwind CSS, offering a sleek, modern look.

Responsive layout ensures the application is usable across desktop and mobile devices.

The document viewer presents the original text on one side and the summarized content on the other for comparison.

Buttons for actions like Copy, Download, and Clear make interacting with the summarized content easy.

Usage
Uploading a Document: Click on the "Upload" button to choose a document file for summarization.

Viewing Summaries: After uploading the document, the application will show the summarized content on the right side of the viewer.

Metrics Display: Below the document viewer, the summary metrics, including the word frequency distribution and sentence length distribution, are displayed in an organized format.

Evaluation and Download: You can download or copy the summary using the provided buttons.

Contributing
If you'd like to contribute to this project, feel free to fork the repository and create a pull request. You can also open issues for bugs or feature requests.

When contributing:

Follow the PEP 8 style guide for Python code.

Write meaningful commit messages.

Ensure that your code is tested and does not break any existing functionality.

Acknowledgments
Django for building the web application framework.

BART and Gemini models for their powerful text summarization capabilities.

Tailwind CSS for a clean and responsive front-end.

OpenAI for providing advanced language models.
