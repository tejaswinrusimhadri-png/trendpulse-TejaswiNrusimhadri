#Task1:Load the Json file
#Load the JSON file from the data/ folder into a Pandas DataFrame
#Print how many rows were loaded
from datetime import datetime
import time
import pandas as pd
from pandas.api.types import is_integer_dtype
import os
filepath=f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
df_stories=pd.read_json(filepath)
#Loaded 122 stories from data/trends_20240115.json
print(f"Loaded{df_stories.shape[0]} stories from {filepath}")
#print(df_stories.size[0])
 
 #Task2 Cleaning the data
 #Duplicates — remove any rows with the same post_id
#duplicate_stories=df_stories.duplicated(subset='post_id',keep=False).sum()
#print(f"number of duplicates stories are:{duplicate_stories}")
if df_stories['post_id'].duplicated().any():
    #Drop duplicates (keep first occurrence)
    df_stories = df_stories.drop_duplicates(subset='post_id', keep='first')
    print(f"After removing duplicates:{df_stories}")
else:
    print("No Duplicates existed")
print(f"After removing duplicates {df_stories.shape[0]}")
#Missing values — drop rows where post_id, title, or score is missing
df_checkna=df_stories[['post_id','title','score']].isna().sum().sum()
if df_checkna:
    df_stories = df_stories.dropna(subset=['post_id', 'title', 'score'])   
else:
    print("No null values existed in post_id, title, or score")

print(f"After removing nulls {df_stories.shape[0]}")
#Data types — make sure score and num_comments are integers
print(df_stories.info())
cols_to_check=['score','num_comments']
for col in cols_to_check:
    print(f"Data type of {col} :{df_stories[col].dtype}")
    if not is_integer_dtype(df_stories[col]):
        print(f"chnaging the {col} datatype to Integer")
        df_stories[col] = pd.to_numeric(df_stories[col], errors='coerce').astype('Int64')

#Low quality — remove stories where score is less than 5
df_stories = df_stories[df_stories['score'] >= 5]
print(f"after removing score less than 5 Total rows are {df_stories.shape[0]}")

#Whitespace — strip extra spaces from the title column
df_stories['title']=df_stories['title'].str.strip()
print("Removed extra spaces from title column")

print(df_stories.head(5))

#Task 3 3 — Save as CSV (6 marks)
#Save the cleaned DataFrame to data/trends_clean.csv
#Print a confirmation message with the number of rows saved
#Also print a quick summary: how many stories per category

os.makedirs('data', exist_ok=True)
df_stories.to_csv('data/trends_clean.csv', index=False)
print(f"saved {df_stories.shape[0]} stories to data/trends_clean.csv file")

#Also print a quick summary: how many stories per category
print(df_stories['category'].value_counts())