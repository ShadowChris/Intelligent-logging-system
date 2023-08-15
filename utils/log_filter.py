import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Download required NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

def extract_keywords_and_phrases(user_question):
    # Tokenize and part-of-speech tag the user question
    tokens = word_tokenize(user_question)
    print('tokens', tokens)

    tagged_tokens = pos_tag(tokens)

    # Identify keywords and phrases based on part-of-speech tags
    keywords = []
    for i, (token, pos) in enumerate(tagged_tokens):
        if pos in ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            # Nouns and verbs are likely to be relevant keywords
            keywords.append(token.lower())
    print('pos',keywords)

    # Remove stopwords
    stopwords_list = set(stopwords.words('english'))
    keywords = [keyword for keyword in keywords if keyword not in stopwords_list]
    print('stop',keywords)
    return keywords

def count_keywords_in_logs(logs, keywords):
    keyword_counts = []
    for log in logs:
        count = sum(1 for keyword in keywords if keyword in log.lower())
        keyword_counts.append((log, count))
    return keyword_counts

def get_logs_with_keyword_counts(logs, keywords):
    keyword_counts = count_keywords_in_logs(logs, keywords)
    logs_with_keywords = [(log, count) for log, count in keyword_counts if count > 0]
    return logs_with_keywords


log_file = 'nginx.txt'
with open(log_file, 'r') as f:
    logs = f.readlines()
log_content = '\n'.join(logs)

user_question = "Can you analyse the logs with error of no such file or directory in the log and tell me how to solve them?"
keywords = extract_keywords_and_phrases(user_question)

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer(vocabulary=keywords)

# Fit and transform the log content
tfidf_matrix = vectorizer.fit_transform([log_content])

# Convert the result to a DataFrame
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

# Filter out the important keywords based on a threshold (e.g., 0.1)
threshold = 0.1
important_keywords = list(tfidf_df.loc[:, tfidf_df.gt(threshold).any()].columns)
print('important:',important_keywords)

logs_with_keyword_counts = get_logs_with_keyword_counts(logs, important_keywords)

return_logs = []
for log, count in logs_with_keyword_counts:
    return_logs.append(log)
    print(log)
return_log = '\n'.join(return_logs)