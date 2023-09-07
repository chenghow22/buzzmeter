# Setup and import library
!pip install langdetect
from langdetect import detect
import re

# Remove blanks from comments
df['comment'] = df['comment'].str.strip()

# Remove unclosed "
df['comment'] = df['comment'].apply(lambda x: re.sub(r'(?<!")"(?!")', '', x))

# Filter out non-English comments
def is_english(s):
    try:
        return detect(s) == 'en'
    except:
        return False

df = df[df['comment'].apply(is_english)]

# Function to remove emoji
!pip install demoji
import demoji

def handle_emoji(string):
    emojis = demoji.findall(string)
    for emoji in emojis:
        string = string.replace(emoji, " " + emojis[emoji].split(":")[0])
    return string

def handle_emoji_in_dataframe(df, column_name):
    # Create a copy of the DataFrame
    df_copy = df.copy()

    # Iterate through the DataFrame and update the specified column
    for index, row in df_copy.iterrows():
        df_copy.at[index, column_name] = handle_emoji(row[column_name])

    return df_copy

# Remove the emoji
df = handle_emoji_in_dataframe(df, 'comment')

# function to removing urls
import re

def remove_url_from_string(text):
    text = re.sub(r"http\S+", "", text)
    return text

# Function to remove URLs from a DataFrame column
def remove_urls_in_df(df, column_name):
    # Create a copy of the DataFrame
    df_copy = df.copy()

    # Apply the remove_url_from_string function to the specified column in the copy
    df_copy[column_name] = df_copy[column_name].apply(remove_url_from_string)

    return df_copy

df = remove_urls_in_df(df, 'comment')

# Remove duplicates
df = df.drop_duplicates(subset=["comment"], keep= 'first')