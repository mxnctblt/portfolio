import re

def extract_hashtags(text):
    """
    Extracts hashtags from a given text.
    """
    hashtag_pattern = re.compile(r'\#\w+')  # Regex pattern to match hashtags
    hashtags = re.findall(hashtag_pattern, text)  # Find all matches of hashtags in the text
    return hashtags

def is_country_spotify_link(link):
    """
    Checks if the given link is a country-specific Spotify link.
    """
    return "/intl-" in link

def is_spotify_link(link):
    """
    Checks if the given link is a Spotify link.
    """
    return "open.spotify.com" in link

def is_youtube_link(link):
    """
    Checks if the given link is a YouTube link.
    """
    return "youtube.com" in link or "youtu.be" in link

def remove_country(spotify_link):
    """
    Removes the country code from a country-specific Spotify link.
    """
    country_code_start = spotify_link.find("intl-")
    if country_code_start != -1:
        country_code_end = spotify_link.find("/", country_code_start)
        if country_code_end != -1:
            spotify_link = spotify_link[:country_code_start] + spotify_link[country_code_end+1:]
    return spotify_link

def embed_spotify_url(spotify_url):
    """
    Converts a Spotify share link to the embed link format.
    """
    # Replace the Spotify share link with the embed link format
    return re.sub(r'https:\/\/open\.spotify\.com\/(track|album|artist|playlist)\/(\w+)',
                  r'https://open.spotify.com/embed/\1/\2', spotify_url)

def embed_youtube_url(youtube_url):
    """
    Converts a YouTube link to the embed link format.
    """
    # Replace the YouTube link with the embed link format
    regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"
    return re.sub(regex, r"https://www.youtube.com/embed/\1", youtube_url)
