# Setup and install library
!pip install nltk spacy wordcloud matplotlib

import nltk
import spacy
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Download NLTK resources (if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')

# Load the spaCy model (you can choose a different language model if needed)
nlp = spacy.load("en_core_web_sm")

# add customised stop words
from nltk.corpus import stopwords

new_stopwords = ["good","better","pro","Pro","able","first","First","new","New","thanks","Thanks","bit","device","way","years","product","products","tech","Tech","much","href=","%","hands","hand","oculus","meta","headset", "people", "apple", "eyes","eye","smiling","smile","joy","face","tears","thing", "things", "video","videos","#","review","quest","=","&#39;"] # adjust if necessary

stpwrd = nltk.corpus.stopwords.words('english')
stpwrd.extend(new_stopwords)

# Extracting data from BigQuery

from google.colab import auth
auth.authenticate_user()
print('Authenticated')

%%bigquery --project project-id --verbose df
SELECT
*
FROM project-id.dataset.table # update dataset table name as required

df_positive = df.query("sentiment == 'POS'")
df_negative = df.query("sentiment == 'NEG'")

# Define the text input
text_positive = df_positive.comment
text_negative = df_negative.comment

# Putting the comment list into an integer
text_string_pos = " ".join(text_positive)
text_string_neg = " ".join(text_negative)

# Tokenize the text using NLTK
from nltk.tokenize import word_tokenize

tokens_pos = word_tokenize(text_string_pos)
tokens_neg = word_tokenize(text_string_neg)

filtered_tokens_pos = [words for words in tokens_pos if not words in stpwrd]
filtered_tokens_neg = [words for words in tokens_neg if not words in stpwrd]

# Split the long text into smaller chunks (max. limit is 1000000)
chunk_size = 500000

long_pos_text = " ".join(filtered_tokens_pos)
chunks = [long_pos_text[i:i+chunk_size] for i in range(0, len(long_pos_text), chunk_size)]

# Filter positive nouns using spaCy
filtered_pos_noun_tokens = []
for chunk in chunks:
    doc = nlp(chunk)
    for token in doc:
        if token.pos_ == "NOUN":
            filtered_pos_noun_tokens.append(token.text.lower()) # Convert to lowercase for consistency

# Filter positive adj using spaCy
filtered_pos_adj_tokens = []
for chunk in chunks:
    doc = nlp(chunk)
    for token in doc:
        if token.pos_ == "ADJ":
            filtered_pos_adj_tokens.append(token.text.lower()) # Convert to lowercase for consistency

long_neg_text = " ".join(filtered_tokens_neg)
chunks = [long_neg_text[i:i+chunk_size] for i in range(0, len(long_neg_text), chunk_size)]

# Filter negative nouns using spaCy
filtered_neg_noun_tokens = []
for chunk in chunks:
    doc = nlp(chunk)
    for token in doc:
        if token.pos_ == "NOUN":
            filtered_neg_noun_tokens.append(token.text.lower()) # Convert to lowercase for consistency

# Filter negative adj using spaCy
filtered_neg_adj_tokens = []
for chunk in chunks:
    doc = nlp(chunk)
    for token in doc:
        if token.pos_ == "ADJ":
            filtered_neg_adj_tokens.append(token.text.lower()) # Convert to lowercase for consistency

from collections import Counter

# positive nouns and adj word frequency
pos_nouns_freq = Counter(filtered_pos_noun_tokens)
pos_adj_freq = Counter(filtered_pos_adj_tokens)

# negative nouns and adj word frequency
neg_nouns_freq = Counter(filtered_neg_noun_tokens)
neg_adj_freq = Counter(filtered_neg_adj_tokens)

# wordcloud setup
pos_nouns_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(pos_nouns_freq)
pos_adj_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(pos_adj_freq)

print("***** POSITIVE nouns word cloud *****")
# Display the nouns word cloud
plt.figure(figsize=(10, 5))
plt.imshow(pos_nouns_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

print("***** POSITIVE adj word cloud *****")
# Display the adj word cloud
plt.figure(figsize=(10, 5))
plt.imshow(pos_adj_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# wordcloud setup
neg_nouns_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(neg_nouns_freq)
neg_adj_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(neg_adj_freq)

print("***** NEGATIVE nouns word cloud *****")
# Display the nouns word cloud
plt.figure(figsize=(10, 5))
plt.imshow(neg_nouns_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

print("***** NEGATIVE adj word cloud *****")
# Display the adj word cloud
plt.figure(figsize=(10, 5))
plt.imshow(neg_adj_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Get the top 10 most common positive nouns
top_10_pos_nouns = pos_nouns_freq.most_common(10)

# Get the top 10 most common positive adj
top_10_pos_adj = pos_adj_freq.most_common(10)

# Display the top 10 positive nouns and their frequencies
print("top 10 most common positive nouns:")
for word, freq in top_10_pos_nouns:
    print(f"{word}: {freq}")

print('*'*50)

# Display the top 10 positive adj and their frequencies
print("top 10 most common positive adj:")
for word, freq in top_10_pos_adj:
    print(f"{word}: {freq}")

# Get the top 10 most common negative nouns
top_10_neg_nouns = neg_nouns_freq.most_common(10)

# Get the top 10 most common negative adj
top_10_neg_adj = neg_adj_freq.most_common(10)

# Display the top 10 negative nouns and their frequencies
print("top 10 most common negative nouns:")
for word, freq in top_10_neg_nouns:
    print(f"{word}: {freq}")

print('*'*50)

# Display the top 10 negative adj and their frequencies
print("top 10 most common negative adj:")
for word, freq in top_10_neg_adj:
    print(f"{word}: {freq}")

# TODO: Set project_id to your Google Cloud Platform project ID.
import pandas_gbq
project_id = 'project-id'

# TODO: Set table_id to the full destination table ID (including the dataset ID).
destination_table_1 = 'project-id.dataset.table1'
destination_table_2 = 'project-id.dataset.table2'
destination_table_3 = 'project-id.dataset.table3'
destination_table_4 = 'project-id.dataset.table4'

# Convert the word frequency count dictionary into dataframe (input requirement of to_gbp function)
pos_nouns_freq = pd.DataFrame.from_dict(dict(pos_nouns_freq), orient='index', columns=['count'])
pos_adj_freq = pd.DataFrame.from_dict(dict(pos_adj_freq), orient='index', columns=['count'])
neg_nouns_freq = pd.DataFrame.from_dict(dict(neg_nouns_freq), orient='index', columns=['count'])
neg_adj_freq = pd.DataFrame.from_dict(dict(neg_adj_freq), orient='index', columns=['count'])

pos_nouns_freq.reset_index(inplace=True,names="word")
pos_adj_freq.reset_index(inplace=True,names="word")
neg_nouns_freq.reset_index(inplace=True,names="word")
neg_adj_freq.reset_index(inplace=True,names="word")

pandas_gbq.to_gbq(pos_nouns_freq,
                  destination_table_1,
                  project_id=project_id,
                  chunksize=None, # I have tried with several chunk sizes, it runs faster when it's one big chunk (at least for me)
                  if_exists='replace', # Use the if_exists argument to dictate whether to 'fail', 'replace' or 'append' if the destination table already exists. The default value is 'fail'.
                  verbose=False
                  )

pandas_gbq.to_gbq(pos_adj_freq,
                  destination_table_2,
                  project_id=project_id,
                  chunksize=None, # I have tried with several chunk sizes, it runs faster when it's one big chunk (at least for me)
                  if_exists='replace', # Use the if_exists argument to dictate whether to 'fail', 'replace' or 'append' if the destination table already exists. The default value is 'fail'.
                  verbose=False
                  )

pandas_gbq.to_gbq(neg_nouns_freq,
                  destination_table_3,
                  project_id=project_id,
                  chunksize=None, # I have tried with several chunk sizes, it runs faster when it's one big chunk (at least for me)
                  if_exists='replace', # Use the if_exists argument to dictate whether to 'fail', 'replace' or 'append' if the destination table already exists. The default value is 'fail'.
                  verbose=False
                  )

pandas_gbq.to_gbq(neg_adj_freq,
                  destination_table_4,
                  project_id=project_id,
                  chunksize=None, # I have tried with several chunk sizes, it runs faster when it's one big chunk (at least for me)
                  if_exists='replace', # Use the if_exists argument to dictate whether to 'fail', 'replace' or 'append' if the destination table already exists. The default value is 'fail'.
                  verbose=False
                  )