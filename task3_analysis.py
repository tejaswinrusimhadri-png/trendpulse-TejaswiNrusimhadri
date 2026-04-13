#Task1 — Load and Explore (4 marks)
#Load data/trends_clean.csv into a Pandas DataFrame
import os

import numpy as np
import pandas as pd
df_stories=pd.read_csv("data/trends_clean.csv")

#Print the shape of the DataFrame (rows and columns)
print(f"Loaded Data {df_stories.shape}")

#Print the first 5 rows
print(f"First 5 rows \n {df_stories.head(5)}")

#Print the average score and average num_comments across all stories
print(f"Average score:{df_stories['score'].mean():.2f}")
print(f"Average num_comments:{df_stories['num_comments'].mean():.2f}")


#Task 2 — Basic Analysis with NumPy (8 marks)
#Use NumPy to answer these questions and print the results:

#What is the mean, median, and standard deviation of score?
#What is the highest score and lowest score?
print("----------Numpy stats-----------")
scores = df_stories['score'].to_numpy()
print(f"Mean score :{np.mean(scores):.2f}")
print(f"Median score :{np.median(scores):.2f}")
print(f"Std deviation :{np.std(scores):.2f}")
print(f"Max score: {np.max(scores)}")
print(f"Min score: {np.min(scores)}")

#Which category has the most stories?
print(df_stories['category'].value_counts())
category=df_stories['category'].value_counts().idxmax()
category_count=df_stories['category'].value_counts().max()
print(f"Most stories in : {category} ({category_count} Stories)")
#Which story has the most comments? Print its title and comment count.
top_story=df_stories.loc[df_stories['num_comments'].idxmax()]
#print(df_stories_comments)
#print(df_stories['num_comments'].idxmax())
print(f"Most commented story: {top_story['title']} - {top_story['num_comments']}")

#Task 3 — Add New Columns
#engagement
#is_popular
df_stories['engagement']=df_stories['num_comments']/(df_stories['score']+1)
df_stories['is_popular']=df_stories['score']>df_stories['score'].mean()
print("Added 2 columns : Engagement,is_popular")
print(df_stories.head(2))

#Task4  — Save the Result (3 marks)
#Save the updated DataFrame (with the 2 new columns) to data/trends_analysed.csv
#Print a confirmation message
os.makedirs('data', exist_ok=True)
df_stories.to_csv('data/trends_analysed.csv', index=False)
print(f"saved {df_stories.shape[0]} stories to data/trends_analysed.csv file")