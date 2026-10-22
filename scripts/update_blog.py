"""Pull the newest posts from the Wonderist blog RSS feed into blog.json.

Runs daily from .github/workflows/update-blog.yml. If the feed is missing
(RSS not turned on in Webflow yet) or broken, blog.json is left alone and the
page keeps showing its built-in blog links.
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED_URL = "https://www.wonderistagency.com/blog/rss.xml"
MAX_POSTS = 3
MEDIA = "{http://search.yahoo.com/mrss/}"


def image_for(item):
    for tag in (MEDIA + "thumbnail", MEDIA + "content", "enclosure"):
        el = item.find(tag)
        if el is not None and el.get("url"):
            return el.get("url")
    # Fall back to the first image inside the post description
    m = re.search(r'<img[^>]+src="([^"]+)"', item.findtext("description") or "")
    return m.group(1) if m else ""


def main():
    try:
        req = urllib.request.Request(FEED_URL, headers={"User-Agent": "wonderist-links"})
        with urllib.request.urlopen(req, timeout=30) as r:
            root = ET.fromstring(r.read())
    except Exception as err:
        print(f"Feed not available yet, leaving blog.json as is: {err}")
        return 0

    posts = []
    for item in root.iter("item"):
        date = item.findtext("pubDate") or ""
        try:
            date = parsedate_to_datetime(date).isoformat()
        except (TypeError, ValueError):
            date = ""
        posts.append({
            "title": (item.findtext("title") or "").strip(),
            "link": (item.findtext("link") or "").strip(),
            "date": date,
            "image": image_for(item),
        })

    posts = [p for p in posts if p["title"] and p["link"]]
    posts.sort(key=lambda p: p["date"], reverse=True)
    if not posts:
        print("Feed had no posts, leaving blog.json as is")
        return 0

    with open("blog.json", "w") as f:
        json.dump({"posts": posts[:MAX_POSTS]}, f, indent=2)
        f.write("\n")
    print(f"Saved {len(posts[:MAX_POSTS])} posts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
