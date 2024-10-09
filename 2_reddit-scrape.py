import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import time

def create_file_name(title):
    fileName = title[:100]
    # remove special characters except for spaces
    fileName = re.sub(r"[^a-zA-Z0-9 ]", "", fileName)
    fileName = fileName.title()
    fileName = fileName.replace(" ", "")
    timestamp = int(time.time() * 1000)
    fileName = f"{fileName}_{timestamp}.txt"
    return fileName

def scrape_reddit_post(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f'Failed to load page {url}, Status Code: {response.status_code}')
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract title
    title_tag = soup.find('h1', id=lambda x: x and x.startswith('post-title-'))
    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        title = 'No title found'
    
    # Extract post content
    post_container = soup.find('div', class_='text-neutral-content', slot='text-body')
    if post_container:
        paragraphs = post_container.find_all('p')
        post_content = '\n\n'.join([para.get_text(strip=True) for para in paragraphs])
    else:
        post_content = 'No post content found'
    
    return title, post_content

curr_dir = Path(__file__).parent
# read from reddit_links.txt and get the URLs line by line
reddit_links_file = open(curr_dir / "input" / "top_posts.txt", "r")
for reddit_post_url in reddit_links_file:
  reddit_post_url = reddit_post_url.strip()
  title, content = scrape_reddit_post(reddit_post_url)
  fileName = create_file_name(title)
  f = open(curr_dir / "stories" / fileName, "w")
  f.write(title + "\n\n" + content)
  f.close()
  print(f"Scraped {title} from {reddit_post_url}")
  time.sleep(1)