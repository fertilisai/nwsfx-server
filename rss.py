import feedparser as fp
import tldextract
from tqdm import tqdm
import json

topics = ['world','tech','business','science','ai']


def get_entry(keys, e, source):


    if 'published' in keys or 'published' in e.keys(): 
        published = e.published
    elif 'updated' in keys or 'updated' in e.keys(): 
        published = e.updated
    elif 'pubDate' in keys or 'pubDate' in e.keys(): 
        published = e.pubDate
    elif 'date' in keys or 'date' in e.keys(): 
        published = e.date
    else:
        published = ''

    if 'published_parsed' in keys or 'published_parsed' in e.keys():
        published_parsed = e.published_parsed
    elif 'updated_parsed' in keys or 'updated_parsed' in e.keys():
        published_parsed = e.updated_parsed
    else:
        published_parsed = ''

    if 'media_thumbnail' in keys or 'media_thumbnail' in e.keys():
        image = e.media_thumbnail[0]['url'] 
    elif 'media_content' in keys or 'media_content' in e.keys():
        image = e.media_content[0]['url']
    else:
        image = ''

    entry = {"title": e.title,
             "link": e.link,
             "date": published,
             "date_parsed": published_parsed,
             "source": source,
             "image": image,
             }
    return entry


def get_entries(feed):
    # Transform the feed into a list of dict (JSON)
    f = fp.parse(feed)

    for e in f.entries:
        try:
            source = tldextract.extract(e.link).registered_domain
            entry = get_entry(f.keys(), e, source)
            entries.append(entry)
        except Exception:
            print("Bad feed: " + feed)
            break

# List of feeds from text files
for t in topics:
    with open(f'rss/{t}.txt', 'r') as r:
        feeds = r.read().splitlines()
    
    entries = []
    for feed in tqdm(feeds):
        get_entries(feed)
    
    # Remove duplicates
    entries = { e['link'] : e for e in entries }.values()

    # Remove empty published dates
    entries = [e for e in entries if e['date_parsed'] != '']

    # sort entries by date
    entries = sorted(entries, key=lambda k: k['date_parsed'], reverse=True)

    j = json.dumps(entries, indent=4)
    with open(f'./json/{t}.json', 'w') as outfile:
        outfile.write(j)
        # print(f'{t} is done')


# Load all json and merge
feeds = []
for t in topics:
    with open(f'json/{t}.json', 'r') as r:
         feed = json.load(r)
    feeds = feeds + feed 

# sort entries by date
feeds = sorted(feeds, key=lambda k: k['date_parsed'], reverse=True)

# Ouput NwsFx
j = json.dumps(feeds, indent=4)
with open(f'./json/nwsfx.json', 'w') as outfile:
    outfile.write(j)
    # print(f'nwsfx is done')