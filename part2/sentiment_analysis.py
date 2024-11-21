# we seek to fine-tune the BERT model to classify post from subreddit r/wallstreetbets to have a sentiment score with range [-100, 100]

#################################### Data retrieval - DONE ####################################
import os
import sys
import pandas as pd

folder_path = r"C:\\Users\\user\\Desktop\\CSE472\\Project 2\\out"

# getting list of all files in the folder
files = os.listdir(folder_path)

df = pd.DataFrame()
#df.head()
#print(df)

for file in files:
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


for idx, row in df.iterrows():
    print(row)
    if idx > 10:
        break
        
df.to_csv("test_ftuned_model_res.csv")


print("*Data passing done*") # essentially more little training
