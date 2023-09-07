# Setup and install library
!pip install transformers[torch] accelerate
!pip install pysentimiento
from pysentimiento import create_analyzer

# Create analyzers for sentiment, hate speech, and irony
sentiment_analyzer = create_analyzer(task="sentiment", lang="en")
hate_speech_analyzer = create_analyzer(task="hate_speech", lang="en")
irony_analyzer = create_analyzer(task="irony", lang="en")
emotion_analyzer = create_analyzer(task="emotion", lang="en")

import pandas as pd
from pysentimiento import create_analyzer

# Create analyzers for sentiment, hate speech, irony, and emotion
sentiment_analyzer = create_analyzer(task="sentiment", lang="en")
hate_speech_analyzer = create_analyzer(task="hate_speech", lang="en")
irony_analyzer = create_analyzer(task="irony", lang="en")
emotion_analyzer = create_analyzer(task="emotion", lang="en")

# Define a list of emotions
emotions_list = ['joy', 'sadness', 'anger', 'surprise', 'disgust', 'fear','others']

# Initialize lists to store results
sentiments = []
sentiment_probs = []
hate_speech_results = []
hate_speech_probs = []
irony_results = []
irony_probs = []
emotion_results = []
emotions_probs = {emotion: [] for emotion in emotions_list}

# Analyze each comment and extract results
for text in df['comment']:
    # Sentiment analysis
    sentiment_result = sentiment_analyzer.predict(text)
    sentiment = sentiment_result.output
    sentiment_prob = sentiment_result.probas[sentiment]

    # Hate speech analysis
    hate_speech_result = hate_speech_analyzer.predict(text)
    hate_speech_result_output = ", ".join(hate_speech_result.output)  # Convert list to string
    hate_speech_prob = hate_speech_result.probas.get(hate_speech_result_output, 0.0)

    # Irony analysis
    irony_result = irony_analyzer.predict(text)
    irony = irony_result.output
    irony_prob = irony_result.probas[irony]

    # Emotion analysis
    emotion_result = emotion_analyzer.predict(text)
    emotion_output = emotion_result.output
    emotion_probabilities = emotion_result.probas

    # Append results to lists
    sentiments.append(sentiment)
    sentiment_probs.append(sentiment_prob)
    hate_speech_results.append(hate_speech_result_output)
    hate_speech_probs.append(hate_speech_prob)
    irony_results.append(irony)
    irony_probs.append(irony_prob)

    # Append emotion output and probabilities to respective lists
    emotion_results.append(emotion_output)
    for emotion in emotions_list:
        emotions_probs[emotion].append(emotion_probabilities.get(emotion, 0.0))

# Add new columns to the DataFrame
df['sentiment'] = sentiments
df['sentiment_prob'] = sentiment_probs
df['hate_speech'] = hate_speech_results
df['hate_speech_prob'] = hate_speech_probs
df['irony'] = irony_results
df['irony_prob'] = irony_probs

# Add columns for emotion output and their probabilities
df['emotion_output'] = emotion_results
for emotion in emotions_list:
    df[emotion] = emotions_probs[emotion]

# Save or display the updated DataFrame
# df.to_csv("xxx.csv", index=False)
print(df.head())  # Display the first few rows

# Histogram to compare the sentiments
px.histogram(df,x='sentiment')
