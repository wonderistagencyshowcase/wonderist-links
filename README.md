# Wonderist Links

Wonderist's link-in-bio page (replaces linktr.ee/wonderistagency).

- `index.html`: the whole page. Buttons, featured spot, podcasts and "Featured In" links are all in here.
- `blog.json`: the latest 3 blog posts. Updated automatically every morning by the "Update blog posts" GitHub Action from the Webflow RSS feed. Until that feed is turned on, the page shows the blog links written into `index.html`.
- `scripts/update_blog.py`: the script the Action runs. The feed address is at the top.
- Click tracking goes to Google Analytics (G-PN46S1R65F) as a `link_click` event with the button name and section.

To change a link, edit `index.html`, then commit and push in GitHub Desktop. GitHub Pages republishes in about a minute.
