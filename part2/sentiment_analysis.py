# we seek to fine-tune the BERT model to classify post from subreddit r/wallstreetbets to have a sentiment score with range [-100, 100]

#################################### Data retrieval - DONE ####################################
import os
import sys
import pandas as pd

folder_path = r"..\\part1\\out"

# getting list of all files in the folder
files = os.listdir(folder_path)

df = pd.DataFrame()
#df.head()
#print(df)

for file in files:
    #print(file)
    # reading the csv file using pandas
    single_df = pd.read_csv(folder_path + "\\" + file)

    #print(single_df.head())
    #single_df = single_df[['content']]
    # dropping all null values
    single_df = single_df.dropna(how='any')
    
    df = pd.concat([df, single_df], axis=0, ignore_index=True)
    
    """
    print("general df:")
    print(df.shape)
    df.info()
    df.describe()
    """

required_cols = ['date', 'source', 'title', 'content']

for rc in required_cols:
    if rc not in df.columns:
        print(f"{rc} is not in th df")
        sys.exit(0)

#df.to_csv("df.csv")

print("*Data retrieval done*")

#################################### Data preprocessing - ####################################
import re

# filtering out any links/ irrelevant content
def remove_urls(original_text):
    # url pattern from re
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    
    # replacing all url with nothing
    text_without_urls = url_pattern.sub('', original_text)
    
    # removing any extra whitespace
    text_without_urls = re.sub(r'\s+', ' ', text_without_urls).strip()
    
    return text_without_urls

# filtering out any non-iteratable objects
def filter_preprocess(original_text):
    # 
    
    return ""
    

df['content'] = df['content'].apply(remove_urls)

print("*Data preprocessing done*")

#################################### Data passing - DONE ####################################
from textblob import TextBlob

def get_sentiment(content):
    tb = TextBlob(content)
    return (tb.sentiment.polarity) * 100

# run sentiment analysis and save to col     
df['polarity'] = df['content'].apply(get_sentiment)

# if want to include subjectivity:
"""
def get_sentiment(content):
    tb = TextBlob(content)
    return (tb.sentiment.polarity) * 100, tb.sentiment.subjectivity

# run sentiment analysis and save to col     
df['polarity'], df['subjectivity'] = zip(*df['content'].apply(get_sentiment))
"""

print("*Data passing done*") # essentially more little training

#################################### Aggregating - DONE ####################################
import datetime as dt

# first sorting the date
df['date'] = pd.to_datetime(df['date'])

df.sort_values(by='date', ignore_index=True)

# making a new df for daily_sentiment_score
sentiment_df = pd.DataFrame(columns=['date','daily_sentiment_score'])
sentiment_df['date'] = df[['date']]
sentiment_df.drop_duplicates(ignore_index=True)

#print(df.shape)
#print(sentiment_df.shape)
"""
# aggregating based on the formula given in doc
def get_daily_sentiment_score(date):
    postv_num = 0
    negtv_num = 0
    #print(date)
    #print(df[df['date'] == date])
    matching_rows = df[df['date'] == date]
    
    for idx, row in matching_rows.iterrows():
        #print(row)
        if row['polarity'] > 0:
            postv_num += 1
        elif row['polarity'] < 0:
            negtv_num += 1
            
        # else neutral: ignore

    return ((postv_num - negtv_num) / (postv_num + negtv_num)) * 100 if postv_num + negtv_num > 0 else 0
   """ 
# aggregating based on a formula devised, using the average
#  sent an email regarding this matter if it is alowed
def get_daily_sentiment_score(date):
    total_score = 0
    total_num = 0
    #print(date)
    #print(df[df['date'] == date])
    matching_rows = df[df['date'] == date]
    
    for idx, row in matching_rows.iterrows():
        #print(row)
        total_score += row['polarity']
        total_num += 1
        # else neutral: ignore
    
    return total_score / total_num
   

#print(get_daily_sentiment_score(sentiment_df.loc[1, 'date']))

sentiment_df['daily_sentiment_score'] = sentiment_df['date'].apply(get_daily_sentiment_score)

"""

# just testing
for idx, row in sentiment_df.iterrows():
    print(row)
    if idx > 10:
        break
"""

df.to_csv(".\\out\\combined_sentiment_results.csv")
sentiment_df.to_csv(".\\out\\daily_sentiment_score.csv")

print("*Aggregating done*")