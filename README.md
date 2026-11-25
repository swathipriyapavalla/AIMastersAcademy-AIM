# AI Masters Academy website

A static website (no server needed): a home page plus one SEO-ready page for every course.

```
index.html                     Home page
courses/<course>.html          One page per course (generated)
assets/site.css, common.js     Shared styles and scripts
data/courses.json              ALL course content lives here
data/icons.json, site.json     Technology icons, phone, email and domain
build.py                       Rebuilds the course pages from data/
robots.txt, sitemap.xml, llms.txt   For search engines and AI search tools
```

## Go live
1. Replace `https://YOUR-DOMAIN` with your real address in every file:
   `sed -i 's#https://YOUR-DOMAIN#https://www.yourdomain.com#g' index.html courses/*.html data/site.json robots.txt sitemap.xml llms.txt`
2. Upload the whole folder to GitHub Pages, Netlify, Vercel or any web host.
3. Add the site to Google Search Console and Bing Webmaster Tools and submit `sitemap.xml`.
4. Check the structured data at https://validator.schema.org and https://search.google.com/test/rich-results

## Add or change course content
1. Edit `data/courses.json` (needs Python 3.8 or newer, no extra packages).
2. Run `python build.py`. The files in `courses/` are rewritten.
3. Upload the changed files.

Fields you can edit for each course: `summary`, `overview` (optional longer text), `who_for`, `tools`, `roles`,
`modules` (title, weeks, topics, project), `registered`, `modes`.

Extra sections and FAQs (shown on the page, and the FAQs are added to the structured data):
```json
"extra_sections": [{"id": "fees", "title": "Fees and batches", "html": "<p>Your text or HTML here.</p>"}],
"faqs": [{"q": "Is there a demo class?", "a": "Yes, message us on WhatsApp to book one."}]
```
Tools need an icon in `data/icons.json` (a tool without an icon simply shows no icon).

## Add a new course
Add an entry to `data/courses.json` (copy an existing one, give it a new `slug`) and run `python build.py`.
Then add the course to the arrays near the top of the script in `index.html` (COURSES, SD, REG, TILE) and to the
static card list and JSON-LD in the page head, so it shows on the home page and in the menu.

## Notes
- Update `lastmod` in `sitemap.xml` when content changes.
- Add a 1200x630 share image and a logo, then add `og:image` and `logo` to the page heads.
- The "registered students" numbers are placeholders. Replace them with real figures.
