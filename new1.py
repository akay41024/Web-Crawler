import crawl4ai

# Method 1: Using __version__ attribute (if available)
print(crawl4ai.__version__)  # Direct version string access

# Method 2: Using importlib.metadata (more reliable)
from importlib.metadata import version
print(version('crawl4ai'))