#!/usr/bin/env python3
"""Builds one SEO-ready page per course from data/courses.json.

Usage:   python build.py
Output:  courses/<slug>.html   (edit data/courses.json, then run this again)
"""
import json, os, sys, html
ROOT = os.path.dirname(os.path.abspath(__file__))
E = html.escape
def load(p): return json.load(open(os.path.join(ROOT, p), encoding='utf8'))
COURSES, ICONS, SITE = load('data/courses.json'), load('data/icons.json'), load('data/site.json')

# Optional preview mode (self-contained pages with absolute links): python build.py --preview urls.json outdir
PREVIEW = '--preview' in sys.argv
if PREVIEW:
    URLS = json.load(open(sys.argv[sys.argv.index('--preview') + 1]))
    OUT = sys.argv[sys.argv.index('--preview') + 2]
else:
    URLS, OUT = None, os.path.join(ROOT, 'courses')
os.makedirs(OUT, exist_ok=True)
DOMAIN = SITE['domain']

def ic(name, size=24):
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" aria-hidden="true">{ICONS[name]}</svg>' if name in ICONS else ''
def home(a=''): return (URLS['home'] if PREVIEW else '../index.html') + a
def page_href(c): return URLS[c['slug']] if PREVIEW else c['slug'] + '.html'
def canonical(c): return (URLS[c['slug']] if PREVIEW else f"{DOMAIN}/courses/{c['slug']}.html")
CSS = open(os.path.join(ROOT, 'assets/site.css'), encoding='utf8').read()
JS = open(os.path.join(ROOT, 'assets/common.js'), encoding='utf8').read()

def faqs(c):
    n, tools = c['name'], ', '.join(c['tools'])
    base = [
     (f"How long is the {n} course?", f"The {n} course runs for about {c['duration']} ({c['weeks']} weeks) with {len(c['modules'])} modules and {len(c['modules'])} hands-on projects."),
     (f"Who can join the {n} course?", f"The course level is: {c['level']}. It suits " + '; '.join(w[0].lower() + w[1:] for w in c['who_for']) + '.'),
     (f"Which tools and technologies are taught in the {n} course?", f"You work with {tools}."),
     (f"What jobs can I aim for after the {n} course?", f"The course prepares you for roles such as {', '.join(c['roles'])}. Career support includes resume and LinkedIn help, portfolio reviews, mock interviews and job application guidance."),
     (f"How do I enroll in the {n} course?", f"Send an enquiry using the form on this page, message the academy on WhatsApp at {SITE['phone_display']}, or email {SITE['email']}. A counsellor will share batch dates and fees. Classroom, live online and weekend batches are available."),
    ]
    return base + [(q['q'], q['a']) for q in c.get('faqs', [])]

def jsonld(c):
    url, org = canonical(c), {"@type": "EducationalOrganization", "name": SITE['name']}
    course = {"@type": "Course", "name": c['name'], "description": c['summary'] + f" {c['duration']} course. Level: {c['level']}.", "url": url,
      "provider": org, "educationalLevel": 'Intermediate' if 'Python needed' in c['level'] else 'Beginner',
      "timeRequired": f"P{c['duration'].split()[0]}M", "inLanguage": "en", "teaches": c['tools'],
      "syllabusSections": [{"@type": "Syllabus", "name": m['title'], "description": '; '.join(m['topics']), "timeRequired": m['weeks']} for m in c['modules']],
      "hasCourseInstance": {"@type": "CourseInstance", "courseMode": ["onsite", "online"]}}
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Home", "item": (URLS['home'] if PREVIEW else DOMAIN + '/')},
      {"@type": "ListItem", "position": 2, "name": "Courses", "item": (URLS['home'] if PREVIEW else DOMAIN + '/') + '#courses'},
      {"@type": "ListItem", "position": 3, "name": c['name'], "item": url}]}
    faq = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs(c)]}
    return json.dumps({"@context": "https://schema.org", "@graph": [course, crumbs, faq]}, ensure_ascii=False)

CUR = ' aria-current="page"'
def header(cur):
    items = ''.join(f'<a href="{page_href(x)}"{CUR if x is cur else ""}><span class="ddi">{ic(x["tile"],22)}</span><span>{E(x["name"])}<small>{E(x["duration"])} · {E(x["level"])}</small></span></a>' for x in COURSES)
    allc = f'<a href="{home("#courses")}"><span class="ddi"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4H10V10H4ZM14 4H20V10H14ZM4 14H10V20H4ZM14 14H20V20H14Z" fill="none" stroke="#3A2FE0" stroke-width="2" stroke-linejoin="round"/></svg></span><span>All courses<small>Browse every program</small></span></a>'
    wa = f'https://wa.me/{SITE["wa"]}?text=' + 'Hi%20AI%20Masters%20Academy%2C%20I%20want%20to%20know%20more%20about%20your%20courses.'
    return f'''<a class="skip" href="#main">Skip to main content</a>
<div class="wrap">
<header>
  <a class="logo" href="{home()}" aria-label="AI Masters Academy, home"><i aria-hidden="true">AIM</i><span class="lt" aria-hidden="true"><span class="l1">AI Masters</span><span class="l2">Academy</span></span></a>
  <div class="hr"><button class="tauto" id="tauto" type="button" hidden title="Follow local time again">Auto</button><button class="tbtn" id="themeBtn" type="button" aria-label="Switch theme"><svg class="t-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg><svg class="t-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button><button class="tbtn" id="fsBtn" type="button" aria-label="Enter full screen" title="Enter full screen"><svg class="fs-in" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9V4H9M20 9V4H15M4 15V20H9M20 15V20H15"/></svg><svg class="fs-out" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 4V9H4M15 4V9H20M9 20V15H4M15 20V15H20"/></svg></button><button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="mainnav" aria-label="Menu"><span></span><span></span><span></span></button></div>
  <nav id="mainnav" aria-label="Main"><a href="{home()}">Home</a><a href="{home('#about')}">About Us</a><div class="dd" id="dd"><a href="{home('#courses')}" class="ddt" id="ddT" aria-expanded="false" aria-controls="ddM">Courses<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9L12 15L18 9"/></svg></a><div class="ddm" id="ddM" aria-label="Courses menu">{allc}{items}</div></div><a href="{home('#careers')}">Careers</a><a class="nav-wa" href="{wa}" target="_blank" rel="noopener"><svg width="20" height="20" fill="currentColor" aria-hidden="true"><use href="#wa"/></svg>Contact Us</a></nav>
</header>'''

def widgets():
    opts = ''.join(f'<a href="https://wa.me/{SITE["wa"]}?text=' + ('Hi%20AI%20Masters%20Academy%2C%20I%20would%20like%20to%20know%20more%20about%20the%20' + E(x["name"]).replace(' ', '%20') + '%20course.') + f'" target="_blank" rel="noopener">{E(x["name"])}</a>' for x in COURSES)
    return f'''<div class="a11y"><div class="a11y-box" id="a11yBox" role="dialog" aria-label="Accessibility options" hidden><div class="a11y-h"><b>Accessibility</b><button type="button" class="a11y-x" id="a11yX" aria-label="Close accessibility options">&times;</button></div><div class="a11y-row"><span id="zLbl">Text size: 100%</span><span class="grp"><button type="button" class="ab" id="zDn" aria-label="Decrease text size">A\u2212</button><button type="button" class="ab" id="zUp" aria-label="Increase text size">A+</button></span></div><button type="button" class="ab sw" data-k="c" aria-pressed="false">High contrast</button><button type="button" class="ab sw" data-k="f" aria-pressed="false">Readable font</button><button type="button" class="ab sw" data-k="l" aria-pressed="false">Highlight links</button><button type="button" class="ab sw" data-k="m" aria-pressed="false">Pause animations</button><button type="button" class="ab rs" id="a11yR">Reset all</button></div><button class="a11y-btn" id="a11yBtn" type="button" aria-expanded="false" aria-controls="a11yBox" aria-label="Accessibility options" title="Accessibility options"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="7.5" r="1.4"/><path d="M7 10.5L12 11.5L17 10.5M12 11.5V15M9.5 20L12 15L14.5 20"/></svg></button></div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<button class="totop" id="toTop" type="button" aria-label="Back to top"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>
<div class="wa"><div class="wa-box" id="waBox" hidden><div class="wa-head"><b>AI Masters Assistant</b><span>Chat with us on WhatsApp</span></div><div class="wa-body"><p>Hi! Which course would you like to know about?</p><div class="wa-body" style="padding:0">{opts}</div></div></div><button class="wa-btn" id="waToggle" type="button" aria-expanded="false" aria-controls="waBox"><svg width="22" height="22" fill="currentColor" aria-hidden="true"><use href="#wa"/></svg>Contact Us</button></div>'''

def build(i, c):
    others = [x for x in COURSES if x is not c]
    n, mods = c['name'], c['modules']
    tech = ''.join(f'<span class="tk" style="--k:{k}" title="{E(t)}" role="img" aria-label="{E(t)}">{ic(t)}</span>' for k, t in enumerate(c['tools']))
    desc = (c['summary'] + f" {c['duration']} course, {c['level'].lower()}. Curriculum, tools, careers and enrollment at {SITE['name']}.")[:300]
    title = f"{c['short']} Course ({c['duration']}) | {SITE['name']}"
    mod_html = ''.join(f'<details class="mod"{" open" if k == 0 else ""}><summary><span class="mn">{k+1:02d}</span><span class="mt">{E(m["title"])}<small>{E(m["weeks"])}</small></span></summary><div class="mc"><ul>{"".join("<li>"+E(t)+"</li>" for t in m["topics"])}</ul><p class="mp"><b>Project:</b> {E(m["project"])}</p></div></details>' for k, m in enumerate(mods))
    extra = ''.join(f'<section class="cs" id="{E(s["id"])}"><h2>{E(s["title"])}</h2>{s["html"]}</section>' for s in c.get('extra_sections', []))
    faq_html = ''.join(f'<details{" open" if k == 0 else ""}><summary>{E(q)}</summary><p>{E(a)}</p></details>' for k, (q, a) in enumerate(faqs(c)))
    rel = ''.join(f'<a class="rc" href="{page_href(x)}"><span class="cico py">{ic(x["tile"],28)}</span><span><b>{E(x["name"])}</b><small>{E(x["duration"])} · {E(x["level"])}</small></span></a>' for x in others)
    foot = ''.join(f'<a href="{page_href(x)}">{E(x["short"])}</a>' for x in COURSES)
    sub = [('overview', 'Overview'), ('curriculum', 'Curriculum'), ('tools', 'Tools'), ('careers', 'Careers')] + [(s['id'], s['title']) for s in c.get('extra_sections', [])] + [('faq', 'FAQ'), ('contact', 'Enroll')]
    subnav = ''.join(f'<a href="#{a}">{E(b)}</a>' for a, b in sub)
    wa_link = f'https://wa.me/{SITE["wa"]}?text=' + 'Hi%20AI%20Masters%20Academy%2C%20I%20would%20like%20to%20know%20more%20about%20the%20' + E(n).replace(' ', '%20') + '%20course.'
    modes = ', '.join(c['modes'])
    css = f'<style>{CSS}</style>' if PREVIEW else '<link rel="stylesheet" href="../assets/site.css">'
    js = f'<script>{JS}</script>' if PREVIEW else '<script src="../assets/common.js" defer></script>'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc[:158])}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="theme-color" content="#3A2FE0">
<link rel="canonical" href="{canonical(c)}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{SITE['name']}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc[:200])}"><meta property="og:url" content="{canonical(c)}"><meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc[:200])}">
<script type="application/ld+json">{jsonld(c)}</script>
<script>(function(){{var p=null,h=new Date().getHours();try{{p=localStorage.getItem('aima_theme')}}catch(e){{}}document.documentElement.setAttribute('data-theme',(p==='dark'||p==='light')?p:((h>=18||h<6)?'dark':'light'))}})()</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=Figtree:wght@400;500;600&display=swap" rel="stylesheet">
{css}
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="wa" viewBox="0 0 24 24"><path d="{SITE['wa_path']}"/></symbol></svg>
{header(c)}
<main id="main">
<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{home()}">Home</a></li><li><a href="{home('#courses')}">Courses</a></li><li aria-current="page">{E(n)}</li></ol></nav>
<div class="chero"><div>
  <span class="eyebrow">{E(c['duration'])} · {E(c['level'])}</span>
  <h1><span class="cico py">{ic(c['tile'],38)}</span>{E(n)}</h1>
  <p class="lead">{E(c['summary'])}</p>
  <div class="cta"><a class="btn" href="#contact">Enroll now</a><a class="btn alt" href="#curriculum">View curriculum</a></div>
  <div class="tks" aria-label="Technologies you will use">{tech}</div>
</div>
<aside class="glance" aria-label="Course at a glance"><h2>Course at a glance</h2><dl><div><dt>Duration</dt><dd>{E(c['duration'])}</dd></div><div><dt>Weeks</dt><dd>{c['weeks']}</dd></div><div><dt>Modules</dt><dd>{len(mods)}</dd></div><div><dt>Projects</dt><dd>{len(mods)}</dd></div><div><dt>Level</dt><dd>{E(c['level'])}</dd></div><div><dt>Registered</dt><dd>{c['registered']} students</dd></div></dl><p style="margin:16px 0 0;color:var(--muted);font-size:14px">Study modes: {E(modes)}.</p></aside></div>
<nav class="subnav" aria-label="On this page">{subnav}</nav>

<section class="cs" id="overview"><h2>About the {E(c['short'])} course</h2>
<p class="sub">{E(c.get('overview', c['summary']))}</p>
<div class="two"><div class="box"><h3>Who is this course for?</h3><ul class="check">{"".join("<li>"+E(w)+"</li>" for w in c['who_for'])}</ul></div>
<div class="box"><h3>What you will build</h3><ul class="check">{"".join("<li>"+E(m["project"])+"</li>" for m in mods)}</ul></div></div></section>

<section class="cs" id="curriculum"><h2>{E(c['short'])} course curriculum</h2>
<div class="tools-bar"><p class="sub" style="margin:0">{c['weeks']} weeks, {len(mods)} modules and {len(mods)} projects.</p><button class="btn alt" id="expandAll" type="button">Expand all modules</button></div>
<div class="mods">{mod_html}</div></section>

<section class="cs" id="tools"><h2>Tools and technologies</h2><p class="sub">What you will work with during the course.</p>
<div class="tgrid">{"".join('<div class="tc">'+ic(t,30)+E(t)+'</div>' for t in c['tools'])}</div></section>

<section class="cs" id="careers"><h2>Career opportunities</h2><p class="sub">Roles this course prepares you for. We help with your resume, portfolio, mock interviews and job applications.</p>
<div class="roles">{"".join("<span>"+E(r[0].upper()+r[1:])+"</span>" for r in c['roles'])}</div></section>
{extra}
<section class="cs" id="faq"><h2>{E(c['short'])} course FAQ</h2><p class="sub">Common questions about this course.</p><div class="faq">{faq_html}</div></section>

<section class="cs" id="more"><h2>Explore other courses</h2><div class="rel">{rel}</div></section>

<section id="contact"><div class="enroll">
  <div><div class="eyebrow" style="background:color-mix(in srgb,var(--brand-ink) 16%,transparent);color:inherit">Enroll</div><h2>Start the {E(c['short'])} course</h2><p class="sub">Send an enquiry or message us on WhatsApp. Our counsellor will share batch dates and fees.</p>
  <div class="cards2"><a class="cc" href="{wa_link}" target="_blank" rel="noopener"><span class="ci"><svg class="f" viewBox="0 0 24 24" aria-hidden="true"><use href="#wa"/></svg></span><span><b>WhatsApp</b><small>{SITE['phone_display']}</small></span></a><a class="cc" href="tel:+{SITE['wa']}"><span class="ci"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4H9L11 9L8.5 10.5A11 11 0 0 0 13.5 15.5L15 13L20 15V19A2 2 0 0 1 18 21A16 16 0 0 1 3 6A2 2 0 0 1 5 4Z"/></svg></span><span><b>Call us</b><small>{SITE['phone_display']}</small></span></a><a class="cc" href="mailto:{SITE['email']}"><span class="ci"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7L12 13L21 7"/></svg></span><span><b>Email</b><small>{SITE['email']}</small></span></a></div></div>
  <div><h3 class="fh">Send us an enquiry</h3><form id="form" novalidate data-course="{E(n)}" data-email="{SITE['email']}">
  <label>Full name<input id="name" autocomplete="name" required></label><label>Email<input id="email" type="email" autocomplete="email" required></label><label>Phone<input id="phone" type="tel" autocomplete="tel" required></label>
  <label>Course<input value="{E(n)}" readonly></label><label>Preferred mode<select id="mode">{"".join("<option>"+E(m)+"</option>" for m in c['modes'])}</select></label>
  <p class="err" id="err" role="alert"></p><button class="btn" type="submit">Send enquiry by email</button></form><div class="ok" id="ok" hidden></div></div>
</div></section>
</main>
<footer><span>\u00a9 2026 {SITE['name']}. Course durations and syllabus are indicative and may change by batch.</span><a class="ftop" href="#main">Back to top \u2191</a><nav class="fnav" aria-label="Courses"><a href="{home()}">Home</a>{foot}</nav></footer>
</div>
{widgets()}
{js}
</body>
</html>'''

for i, c in enumerate(COURSES):
    p = os.path.join(OUT, c['slug'] + '.html')
    open(p, 'w', encoding='utf8').write(build(i, c))
    print('built', p)
