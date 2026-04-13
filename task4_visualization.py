import os
import pandas as pd
import matplotlib.pyplot as plt

#Load data/trends_analysed.csv into a DataFrame
df=pd.read_csv('data/trends_analysed.csv')
# Create outputs folder
os.makedirs('outputs', exist_ok=True)

#Chart 1: Top 10 Stories by Score
top10_stories=df.sort_values(by='score',ascending=False).head(10)
#print(top10_stories['score'])
top10_stories['short_title'] = top10_stories['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
plt.figure()
plt.barh(top10_stories['short_title'], top10_stories['score'])
plt.xlabel('Score')
plt.ylabel('Story Title')
plt.title('Top 10 Stories by Score')
plt.gca().invert_yaxis()  # highest score on top
plt.savefig('outputs/chart1_top_stories.png')
plt.show()

#Chart 2: Stories per Category
category_counts = df['category'].value_counts()

plt.figure()

plt.bar(category_counts.index, category_counts.values)
plt.xlabel('Category')
plt.ylabel('Number of Stories')
plt.title('Stories per Category')

plt.savefig('outputs/chart2_categories.png')
plt.show()


#Task4 — Chart 3: Score vs Comments
plt.figure()

# Separate popular vs non-popular
popular = df[df['is_popular'] == True]
not_popular = df[df['is_popular'] == False]

plt.scatter(popular['score'], popular['num_comments'], label='Popular')
plt.scatter(not_popular['score'], not_popular['num_comments'], label='Not Popular')

plt.xlabel('Score')
plt.ylabel('Number of Comments')
plt.title('Score vs Comments')
plt.legend()

plt.savefig('outputs/chart3_scatter.png')
plt.show()

#Combine all 3 charts into one figure:

#Use plt.subplots(1, 3) or plt.subplots(2, 2) to lay them out together
#Add an overall title: "TrendPulse Dashboard"
#Save as outputs/dashboard.png

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# --- Chart 1: Top 10 Stories ---
top10 = df.sort_values(by='score', ascending=False).head(10)
top10['short_title'] = top10['title'].apply(
    lambda x: x[:50] + '...' if len(x) > 50 else x
)

axes[0].barh(top10['short_title'], top10['score'])
axes[0].set_title('Top 10 Stories')
axes[0].set_xlabel('Score')
axes[0].invert_yaxis()

# --- Chart 2: Stories per Category ---
category_counts = df['category'].value_counts()

axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title('Stories per Category')
axes[1].set_xlabel('Category')
axes[1].set_ylabel('Count')

# --- Chart 3: Scatter Plot ---
popular = df[df['is_popular'] == True]
not_popular = df[df['is_popular'] == False]

axes[2].scatter(popular['score'], popular['num_comments'], label='Popular')
axes[2].scatter(not_popular['score'], not_popular['num_comments'], label='Not Popular')

axes[2].set_title('Score vs Comments')
axes[2].set_xlabel('Score')
axes[2].set_ylabel('Comments')
axes[2].legend()

# --- Overall Title ---
plt.suptitle('TrendPulse Dashboard')

# Save BEFORE show
plt.savefig('outputs/dashboard.png')

plt.show()