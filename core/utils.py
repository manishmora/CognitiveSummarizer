from transformers import pipeline
import re
from nltk.tokenize import sent_tokenize
import plotly.graph_objects as go
import plotly.express as px
import nltk
from nltk import FreqDist

# Load the pre-trained BART model for summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def split_text_into_chunks(text, max_chunk_words=400):
    """
    Splits text into smaller chunks based on sentence boundaries.
    Useful when the input exceeds token limits.
    """
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_words = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        if current_words + word_count <= max_chunk_words:
            current_chunk.append(sentence)
            current_words += word_count
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_words = word_count

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_with_bart(text):
    """
    Summarizes the input text using BART (facebook/bart-large-cnn).
    """
    if not text.strip():
        return "No content provided to summarize."

    try:
        # Split text into chunks if it's too large
        chunks = split_text_into_chunks(text)
        summaries = []
        
        for chunk in chunks:
            # Perform the summarization
            summary = summarizer(chunk)
            summaries.append(summary[0]['summary_text'])
        
        return " ".join(summaries) if summaries else "Summary could not be generated."
    except Exception as e:
        return f"Error summarizing with BART: {str(e)}"

def highlight_main_content(summary, text_input):
    """
    Highlights the first sentence of the summary in yellow.
    """
    try:
        if not summary.strip():
            return "No summary available."

        first_sentence = summary.split('.')[0]
        if first_sentence:
            highlighted_summary = f"<span class='highlight'>{first_sentence}.</span>{summary[len(first_sentence)+1:]}"
            return highlighted_summary
        return summary
    except Exception as e:
        return f"Error: {str(e)}"

def calculate_stats(text):
    """
    Calculate word count and sentence count in the provided text.
    """
    word_count = len(re.findall(r'\w+', text))
    sentence_count = len(re.findall(r'[.!?]', text))
    return word_count, sentence_count


def format_as_bullet_points(summary):
    """
    Converts the summary text into a list of bullet points, ensuring each bullet point 
    is followed by the next sentence in the next line.
    """
    sentences = sent_tokenize(summary)
    bullet_points = ""
    for sentence in sentences:
        if sentence.strip():
            bullet_points += f"• {sentence.strip()}\n\n"  # Add bullet point followed by the sentence
            bullet_points += "\n\n"  # Add a blank line after each bullet point
    return bullet_points


# Ensure necessary NLTK data is downloaded
nltk.download('punkt')

def generate_word_frequency_plot(text):
    """
    Generate a plot for the frequency of words in the provided text.
    """
    words = re.findall(r'\w+', text.lower())
    freq_dist = FreqDist(words)
    word_freq = list(freq_dist.items())
    
    # Sort by frequency
    word_freq.sort(key=lambda x: x[1], reverse=True)

    # Extract top 10 most frequent words
    top_words = word_freq[:10]
    words, counts = zip(*top_words)

    fig = go.Figure(data=[go.Bar(x=words, y=counts)])
    fig.update_layout(
        title="Top 10 Most Frequent Words",
        xaxis_title="Words",
        yaxis_title="Frequency",
        template="plotly_dark"
    )

    return fig.to_html(full_html=False)

def generate_sentence_length_distribution_plot(text):
    """
    Generate a histogram plot for sentence length distribution.
    """
    sentences = nltk.sent_tokenize(text)
    sentence_lengths = [len(nltk.word_tokenize(sentence)) for sentence in sentences]

    fig = px.histogram(
        x=sentence_lengths,
        labels={'x': 'Sentence Length (in words)'},
        title="Sentence Length Distribution",
        template="plotly_dark"
    )
    return fig.to_html(full_html=False)

from rouge_score import rouge_scorer

def calculate_rouge_score(reference_summary, generated_summary):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference_summary, generated_summary)
    return scores

# ... previous imports ...

# Simulated Gemini-like format: bullet points + bolded keywords
def format_as_bullet_points(summary):
    sentences = sent_tokenize(summary)
    bullet_points = []
    for sentence in sentences:
        if sentence.strip():
            # Bold first keyword (heuristic: first noun or significant word)
            words = sentence.strip().split()
            if words:
                words[0] = f"{words[0]}"
                sentence = " ".join(words)
            bullet_points.append(f"• {sentence}")
    return "\n\n".join(bullet_points)


def format_summary_by_role(summary, role):
    """
    Format the summary based on user role.
    """
    summary = format_as_bullet_points(summary)

    if role == "manager":
        return f"🔹 **Manager Overview:**\n\n{summary}"
    elif role == "client":
        return f"📌 **Client Highlights:**\n\n{summary}"
    elif role == "researcher":
        return f"🧠 **Research Summary:**\n\n{summary}"
    else:  # default: engineer or unknown
        return f"🔧 **Technical Summary:**\n\n{summary}"


def summarize_with_bart(text, role=None):
    """
    Summarizes the input text using BART (facebook/bart-large-cnn).
    """
    if not text.strip():
        return "No content provided to summarize."

    try:
        chunks = split_text_into_chunks(text)
        summaries = [summarizer(chunk)[0]['summary_text'] for chunk in chunks]
        combined_summary = " ".join(summaries)

        return format_summary_by_role(combined_summary, role)
    except Exception as e:
        return f"Error summarizing with BART: {str(e)}"


def calculate_summary_length_ratio(original_text, summary_text):
    """
    Calculates the ratio of summary length to original text length in words.
    """
    original_words = len(re.findall(r'\w+', original_text))
    summary_words = len(re.findall(r'\w+', summary_text))
    if original_words == 0:
        return 0
    return round(summary_words / original_words, 2)


# Rest remains unchanged...
