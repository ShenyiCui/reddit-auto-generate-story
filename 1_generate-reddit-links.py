import requests
from bs4 import BeautifulSoup
import sys

def scrape_top_posts(subreddit_url, top_n=10, output_file='top_posts.txt'):
    """
    Scrapes the top N post URLs from a given subreddit and writes them to a text file.

    :param subreddit_url: URL of the subreddit (e.g., 'https://www.reddit.com/r/AmItheAsshole/top/')
    :param top_n: Number of top posts to scrape
    :param output_file: Name of the output text file
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(subreddit_url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the subreddit page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    a_tags = soup.find_all('a', attrs={'data-event-action': 'title'})

    if not a_tags:
        print("No post links found. The subreddit page structure might have changed.")
        return

    post_urls = []
    for i, a in enumerate(a_tags):
        if i == 0: continue  # Skip the first post (pinned post)
        href = a.get('href')
        if href and href.startswith('/r/'):
            full_url = f"https://www.reddit.com{href}"
            post_urls.append(full_url)
        if len(post_urls) >= top_n:
            break

    if not post_urls:
        print("No valid post URLs found.")
        return

    # Write the URLs to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for url in post_urls:
                file.write(url + '\n')
        print(f"Successfully written top {len(post_urls)} post URLs to '{output_file}'.")
    except IOError as e:
        print(f"Error writing to file: {e}")

subreddit = sys.argv[1]
if not subreddit:
    print("Please provide the subreddit URL as an argument.")
else:
    scrape_top_posts(subreddit_url=subreddit, top_n=10, output_file='input/top_posts.txt')
