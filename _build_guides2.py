# -*- coding: utf-8 -*-
"""Generate 8 long-tail Bamzal guides + regenerate /guides hub (17 cards) + update sitemap."""
import os, json, re

SITE = os.path.dirname(os.path.abspath(__file__))

FAVICONS = ('<link rel="icon" type="image/png" sizes="32x32" href="/bamzal-favicon-a-32.png?v=a8">'
            '<link rel="icon" type="image/png" sizes="512x512" href="/bamzal-favicon-a-512.png?v=a8">'
            '<link rel="icon" type="image/png" sizes="48x48" href="/bamzal-favicon-a-48.png?v=a8">'
            '<link rel="icon" type="image/png" sizes="180x180" href="/bamzal-favicon-a-180.png?v=a8">'
            '<link rel="icon" type="image/x-icon" href="/bamzal-favicon-a.ico?v=a8">'
            '<link rel="apple-touch-icon" href="/bamzal-favicon-a-apple.png?v=a8">')
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;'
         '0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Fraunces:ital,opsz,wght@'
         '0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Cinzel:wght@600;700;800&display=swap" '
         'rel="stylesheet">')
ARTICLE_CSS = """    <style>
        .article-hero { padding: 140px 24px 48px; text-align: center; background: linear-gradient(180deg, var(--accent-light) 0%, var(--paper) 100%); }
        .article-hero-inner { max-width: 760px; margin: 0 auto; }
        .article-meta { display: flex; align-items: center; justify-content: center; gap: 20px; margin-top: 20px; font-size: .8125rem; color: var(--muted); }
        .article-meta span { display: flex; align-items: center; gap: 6px; }
        .article-body { max-width: 760px; margin: 0 auto; padding: 48px 24px 80px; }
        .article-body h2 { font-family: var(--font-display); font-size: 1.625rem; font-weight: 700; margin: 48px 0 16px; color: var(--ink); scroll-margin-top: 80px; }
        .article-body h3 { font-size: 1.125rem; font-weight: 600; margin: 32px 0 12px; color: var(--ink); }
        .article-body p { font-size: .9375rem; color: var(--slate); margin-bottom: 16px; line-height: 1.75; }
        .article-body strong { color: var(--ink); }
        .article-body a { color: var(--accent); text-decoration: none; font-weight: 500; }
        .article-body a:hover { text-decoration: underline; }
        .article-body ul, .article-body ol { margin: 8px 0 20px 24px; }
        .article-body li { font-size: .9375rem; color: var(--slate); margin-bottom: 8px; line-height: 1.7; }
        .toc { background: #fff; border: 1px solid var(--border); border-radius: var(--radius); padding: 28px 32px; margin-bottom: 40px; }
        .toc h3 { font-size: .9375rem; font-weight: 600; margin-bottom: 14px; color: var(--ink); }
        .toc ol { margin: 0; padding-left: 20px; }
        .toc li { font-size: .875rem; color: var(--slate); margin-bottom: 8px; line-height: 1.5; }
        .toc a { color: var(--accent); text-decoration: none; }
        .comparison-table-wrap { overflow-x: auto; margin: 24px 0 32px; }
        .comparison-table { width: 100%; border-collapse: collapse; font-size: .875rem; background: #fff; border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
        .comparison-table thead { background: var(--ink); }
        .comparison-table th { color: #fff; font-weight: 600; padding: 14px 16px; text-align: left; font-size: .8125rem; text-transform: uppercase; letter-spacing: .04em; }
        .comparison-table td { padding: 13px 16px; border-bottom: 1px solid var(--border); color: var(--slate); vertical-align: top; }
        .comparison-table tr:last-child td { border-bottom: none; }
        .comparison-table td:first-child { font-weight: 600; color: var(--ink); }
        .comparison-table tr:nth-child(even) { background: var(--surface); }
        .data-callout { background: var(--accent-light); border-left: 4px solid var(--accent); border-radius: 0 var(--radius-sm) var(--radius-sm) 0; padding: 20px 24px; margin: 24px 0 28px; }
        .data-callout p { color: var(--ink); margin-bottom: 0; font-size: .9375rem; }
        .data-callout strong { color: var(--accent-dark); }
        .verdict-box { background: #fff; border: 2px solid var(--accent); border-radius: var(--radius); padding: 28px 32px; margin: 24px 0 28px; }
        .verdict-box h4 { font-family: var(--font-display); font-size: 1.125rem; font-weight: 700; color: var(--accent); margin-bottom: 10px; }
        .verdict-box p { margin-bottom: 8px; }
        .verdict-box p:last-child { margin-bottom: 0; }
        @media (max-width: 768px) { .comparison-table { font-size: .8125rem; } .comparison-table th, .comparison-table td { padding: 10px 12px; } .article-meta { flex-direction: column; gap: 8px; } }
    </style>"""
NAV = """<!-- NAV -->
<nav class="nav">
    <div class="nav-inner">
        <a href="/" class="nav-logo" aria-label="Bamzal home"><img class="brand-mark" src="/bamzal-header-mark-full.png" alt="" width="32" height="48" aria-hidden="true"><span class="brand-wordmark" aria-hidden="true"><span class="brand-b">B</span><svg class="brand-a" viewBox="0 0 64 64" focusable="false"><path d="M8 56 C18 22 30 10 42 16 C50 20 56 38 60 56" fill="none" stroke="currentColor" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"/><circle class="brand-dot" cx="31" cy="50" r="6.5"/></svg><span class="brand-rest">mzal</span></span></a>
        <button class="mobile-toggle" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menu">
            <span></span><span></span><span></span>
        </button>
        <ul class="nav-links">
            <li><a href="/product">Product</a></li>
            <li><a href="/demo">Demo</a></li>
            <li><a href="/pricing">Pricing</a></li>
            <li><a href="/guides">Guides</a></li>
            <li><a href="/company">Company</a></li>
            <li><a href="/contact">Contact</a></li>
            <li><a href="/contact" class="nav-cta">Get Started</a></li>
        </ul>
    </div>
</nav>"""
CTA = """<section class="cta-section">
    <h2>Ready for a growth team that does more than run ads?</h2>
    <p>Bamzal studies your whole Shopify store, fixes pages, pricing and retention, and runs Google, Meta, TikTok and Pinterest ads when they're the right lever &mdash; all from one dashboard inside your Shopify admin.</p>
    <div style="display:flex; gap:16px; justify-content:center; flex-wrap:wrap;">
        <a href="/demo" class="btn btn-white">View Live Demo &rarr;</a>
        <a href="/pricing" class="btn" style="background:rgba(255,255,255,.15); color:#fff; border:1.5px solid rgba(255,255,255,.3);">See Pricing</a>
        <a href="/product" class="btn" style="background:rgba(255,255,255,.15); color:#fff; border:1.5px solid rgba(255,255,255,.3);">How It Works</a>
    </div>
</section>"""
FOOTER = """<!-- FOOTER -->
<footer class="footer">
    <div class="footer-inner">
        <div class="footer-grid">
            <div>
                <div class="footer-brand"><img src="/bamzal-logo-light.svg" alt="Bamzal" width="155" height="44"></div>
                <p class="footer-desc">An autonomous AI growth team for Shopify — store fixes, pricing, retention and ads, with every move reversible and under your control.</p>
                <p style="font-size:.8125rem; margin-top:12px;">Bamzal Ltd.<br>Nahal Besor 10/7, Beit Shemesh, Israel<br>+972-58-486-9778</p>
            </div>
            <div class="footer-col">
                <h3>Product</h3>
                <a href="/product">How It Works</a>
                <a href="/demo">Live Demo</a>
                <a href="/pricing">Pricing</a>
                <a href="/#api-usage">API Usage</a>
            </div>
            <div class="footer-col">
                <h3>Guides</h3>
                <a href="/guides">All Guides</a>
                <a href="/roas-calculator">ROAS Calculator</a>
                <a href="/meta-ads-vs-google-ads-shopify">Meta vs Google Ads</a>
                <a href="/best-ai-marketing-tools-shopify">AI Marketing Tools</a>
            </div>
            <div class="footer-col">
                <h3>Company</h3>
                <a href="/company">About Us</a>
                <a href="/contact">Contact</a>
                <a href="/company#security">Security</a>
            </div>
            <div class="footer-col">
                <h3>Legal</h3>
                <a href="/privacy">Privacy Policy</a>
                <a href="/terms">Terms of Service</a>
                <a href="/data-deletion">Data Deletion</a>
                <a href="/dpa">DPA</a>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; 2026 Bamzal Ltd. All rights reserved.</span>
            <div class="footer-legal">
                <a href="/privacy">Privacy Policy</a>
                <a href="/terms">Terms of Service</a>
            </div>
        </div>
    </div>
</footer>"""


def render_article(slug, title, meta_desc, og_desc, kicker, read_min, toc_items, body, keywords, crumb, faqs=None):
    url = "https://bamzal.com/" + slug
    toc_items = list(toc_items)
    faqld = ""
    faq_section = ""
    if faqs:
        faq_json = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
            indent=2, ensure_ascii=False)
        faqld = '    <script type="application/ld+json">\n%s\n    </script>' % faq_json
        faq_items_html = "\n".join(
            "        <h3>" + q + "</h3>\n        <p>" + a + "</p>" for q, a in faqs)
        faq_section = '\n    <h2 id="faq">Frequently asked questions</h2>\n' + faq_items_html + "\n"
        toc_items = toc_items + [("faq", "Frequently asked questions")]
    toc_html = "\n".join('            <li><a href="#%s">%s</a></li>' % (a, t) for a, t in toc_items)
    art = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": title,
        "image": "https://bamzal.com/bamzal-og.png?v=og1", "description": meta_desc,
        "author": {"@type": "Organization", "name": "Bamzal", "url": "https://bamzal.com"},
        "publisher": {"@type": "Organization", "name": "Bamzal", "url": "https://bamzal.com",
            "logo": {"@type": "ImageObject", "url": "https://bamzal.com/bamzal-favicon-a-apple.png?v=a8"}},
        "datePublished": "2026-06-21", "dateModified": "2026-06-21",
        "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "keywords": keywords}, indent=2, ensure_ascii=False)
    crumbj = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bamzal.com/"},
        {"@type": "ListItem", "position": 2, "name": "Guides", "item": "https://bamzal.com/guides"},
        {"@type": "ListItem", "position": 3, "name": crumb, "item": url}]}, indent=2, ensure_ascii=False)
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="Bynu8UFHhaQK6Q9k8k2SBpfzIeaZIAQzRfaMiZ402gc" />
    <meta name="google-site-verification" content="fZkN1ASC85TdFlqB5fG5f3R10V6CZP9dG9iUCF8uXhM" />
    {fav}<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Bamzal</title>
    <meta name="description" content="{meta_desc}">
    <link rel="canonical" href="{url}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{og_desc}">
    <meta property="og:image" content="https://bamzal.com/bamzal-og.png?v=og1">
    <meta property="og:image:secure_url" content="https://bamzal.com/bamzal-og.png?v=og1">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:type" content="image/png">
    <meta property="og:image:alt" content="Bamzal — autonomous AI growth team for Shopify.">
    <meta property="og:site_name" content="Bamzal">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{og_desc}">
    <meta name="twitter:image" content="https://bamzal.com/bamzal-og.png?v=og1">
    {fonts}
    <link rel="stylesheet" href="/shared.css?v=brand-lockup-20260518">
{css}
    <script type="application/ld+json">
{art}
    </script>
    <script type="application/ld+json">
{crumbj}
    </script>
{faqld}
</head>
<body>

{nav}

<section class="article-hero">
    <div class="article-hero-inner">
        <div class="hero-badge">Guide</div>
        <h1>{title}</h1>
        <p>{kicker}</p>
        <div class="article-meta">
            <span>By Bamzal</span><span>|</span><span>Updated June 2026</span><span>|</span><span>{read} min read</span>
        </div>
    </div>
</section>

<div class="article-body">
    <div class="toc">
        <h3>Table of Contents</h3>
        <ol>
{toc}
        </ol>
    </div>
{body}
{faq_section}
</div>

{cta}

{footer}

</body>
</html>
""".format(fav=FAVICONS, title=title, meta_desc=meta_desc, url=url, og_desc=og_desc, fonts=FONTS,
           css=ARTICLE_CSS, art=art, crumbj=crumbj, faqld=faqld, nav=NAV, kicker=kicker, read=read_min,
           toc=toc_html, body=body, faq_section=faq_section, cta=CTA, footer=FOOTER)
    open(os.path.join(SITE, slug + ".html"), "w", encoding="utf-8", newline="\n").write(html)
    print("wrote", slug + ".html")
