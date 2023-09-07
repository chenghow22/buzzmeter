# Setup and install library
import pandas_gbq
import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize

# Import data from BigQuery
from google.colab import auth
auth.authenticate_user()
print('Authenticated')

%%bigquery --project-id --verbose df
SELECT
*
FROM project-id.dataset.table1 # update dataset table name as required

# Data cleaning
def clean (text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, ' ') # Remove Punctuation
    lowercased = text.lower() # Lower Case
    tokenized = word_tokenize(lowercased) # Tokenize
    words_only = [word for word in tokenized if word.isalpha()] # Remove numbers
    stop_words = set(stopwords.words('english')) # Make stopword list
    new_stopwords = ["year","look","well","cool","im","woow","hand","something","excited","lol","using","red","day","iphone","valve","say","bought","next","hope","feature","product","need","thank","thanks","wait","great","best","love","got","see","ar","amazing","getting","mine","grinning","first","future","facebook","meta","device","psvr","oculus","man","href","anything","better","never","good","want","way","cry","also","going","company","get","na","really","buy","still","gon","make","use","even","know","cry","much","headset", "face","tear","tears","joy","br","smiling","eye","eyes","like","one","vr","vision","pro","would","think","heart","laughing","look","could","quot","hand","tech","go","people", "apple", "thing", "things", "video","videos","#","br","review","quest","=","&#39;"] # adjust if necessary
    stpwrd = nltk.corpus.stopwords.words('english')
    stpwrd.extend(new_stopwords)
    without_stopwords = [word for word in words_only if not word in stpwrd] # Remove Stop Words
    lemma=WordNetLemmatizer() # Initiate Lemmatizer
    lemmatized = [lemma.lemmatize(word) for word in without_stopwords] # Lemmatize
    cleaned = ' '.join(lemmatized) # Join back to a string
    return cleaned

# Apply to all texts
df['clean_text'] = df.comment.apply(clean)

# Vectorization and topic modelling
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()

data_vectorized = vectorizer.fit_transform(df_pos['clean_text'])

lda_model = LatentDirichletAllocation(n_components=3)

lda_vectors = lda_model.fit_transform(data_vectorized)

def print_topics(model, vectorizer):
    for idx, topic in enumerate(model.components_):
        print("Topic %d:" % (idx))
        print([(vectorizer.get_feature_names_out()[i], topic[i])
                        for i in topic.argsort()[:-10 - 1:-1]])

print_topics(lda_model, vectorizer)