from datetime import datetime

import requests
import json
import os
import time

BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}
catogory_max=25

# Categories and keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def stories_list():
    #Step 1 — Get the list of top story IDs:
    url = f"{BASE_URL}/topstories.json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()[:500]
    except Exception as e:
        print(f"Failed to fetch top stories: {e}")
        return []

def check_catagory(title):
    if not title:
        return None

    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None

#Step 2 — Get each story's details:
#https://hacker-news.firebaseio.com/v0/item/{id}.json
def check_all_cat_finished(category_dict):
    if all(value == 25 for value in category_dict.values()):
        return True
    else:
        return False

def fetch_data():
    list_of_stories=stories_list()
    print(f"stories are collectd :{len(list_of_stories)}")
    stories=[]
    category_count={cat:0 for cat in CATEGORIES}
    for story_id in list_of_stories:
        print(f"entered:storyid is {story_id}")
        url = f"{BASE_URL}/item/{story_id}.json"
        try:
            response=requests.get(url,headers=HEADERS,timeout=10)
            response.raise_for_status()
            story=response.json()

        except Exception as e:
            print("Failed to retrieve the story {story_id}:{e}")
            story=None
        title = story.get("title", "")
        #print("title is ",title)
        category=check_catagory(title)
        #print(f"category :{category}")
        #print(f"category count :{category_count.get(category, 0)}")
        if not category or not title or category_count.get(category, 0) >= catogory_max:
            print("Skipping category",category)
            continue
        story_data = {
                "post_id": story.get("id"),
                "title": title,
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", ""),
                "collected_at": datetime.now().isoformat()
            }
        print(f"collected:{category}")
        stories.append(story_data)
        category_count[category]=category_count[category]+1
        if category_count[category]== 25:
            time.sleep(2)
        if check_all_cat_finished(category_count):
            print("break")
            break
        
    return stories

def save_json(collected):
    os.makedirs("data",exist_ok=True)
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
    # Save JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected, f, indent=4)

    print(f"Collected {len(collected)} stories. Saved to {filename}")
    
if __name__=="__main__":
    stories_data=fetch_data()
    save_json(stories_data)



