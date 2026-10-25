# -*- coding: utf-8 -*-
"""Build the Midad magazine. Set SITE_URL before submitting the site to Google Ads."""
import json
import re
import shutil
from pathlib import Path

from desk_ai import ARTICLES as AI
from desk_art import ARTICLES as ART
from desk_beauty import ARTICLES as BEAUTY
from desk_general import ARTICLES as GENERAL
from desk_health import ARTICLES as HEALTH
from desk_stories import STORIES
from desk_tools import ARTICLES as TOOLS
from desk_zodiac import ARTICLES as ZODIAC

ROOT = Path(__file__).resolve().parent

# Public https origin, no trailing slash. Required for canonical links and sitemap.
SITE_URL = ""
# Optional. Example: "AW-123456789" or "G-XXXX". Leave empty until you choose a tag.
GOOGLE_TAG_ID = ""

NAME_AR = "مداد"
BRAND = "Midad"
TOOLS_ORIGIN = "https://creativotools.com"

SECTIONS = {
    "general": {
        "nav": "عام",
        "title": "معلومات عامة",
        "kicker": "معرفة عامة",
        "desc": "شروحات عملية عن التحقق من الأخبار، وحقوق الصور، وتنظيم الملفات، والقراءة الدقيقة.",
        "intro": "القسم ده للمعلومة اللي بتنفع قبل أي أداة: إزاي تقرأ خبر، وإزاي تستخدم صورة من غير ما تاخد حق غيرها، وإزاي تحفظ ملفاتك. الصفحات دي مكتوبة عشان تتقرأ، وممكن تستخدمها صفحة وصول لإعلان بيتكلم عن نفس الموضوع.",
        "articles": GENERAL,
    },
    "beauty": {
        "nav": "جمال",
        "title": "الجمال",
        "kicker": "جمال",
        "desc": "عناية يومية بالبشرة والجسم والشعر، من غير وعود منتجات ومن غير وصفات طبية.",
        "intro": "عناية البشرة والجسم والشعر هنا روتين يومي: غسيل، وترطيب، وشمس، وقراءة الإعلان قبل الشراء. الكلام عام ومش كشف جلدية. لو في مرض جلدي أو حساسية، الطبيب يشوف الحالة.",
        "articles": BEAUTY,
    },
    "health": {
        "nav": "صحة",
        "title": "الصحة",
        "kicker": "صحة",
        "desc": "نوم وحركة وميّة، ومتى تزور الطبيب، وأنواع الأكل الشائعة بحدودها.",
        "intro": "كلام عادي عن النوم والمشي والميّة، وجواه أنواع الأكل. المقال مش كشف، ومتوقفش الدوا من نفسك. لو عندك مرض أو بتشرب دوا، اسأل الدكتور قبل ما تغيّر أكلك.",
        "articles": HEALTH,
    },
    "zodiac": {
        "nav": "أبراج",
        "title": "أبراج",
        "kicker": "أبراج",
        "desc": "قراءة ترفيهية للأبراج الاتناشر، مع توضيح إن العمود مش علم ومش طالع شخصي.",
        "intro": "كل برج له صفحة واضحة: شخصيته، وطريقته في العلاقات، والشغل اللي يناسبه في كلام الأبراج. الوصف شائع وتسلية، والناس مختلفة حتى لو اتولدوا في نفس الأسبوع.",
        "articles": ZODIAC,
    },
    "tools": {
        "nav": "أدوات",
        "title": "أدوات",
        "kicker": "أدوات",
        "desc": "شرح ضغط الصور وملفات PDF والسيرة الذاتية والعلامة المائية وطمس الوجوه، بحدود كل طريقة.",
        "intro": "هنا بنشرح المهارة نفسها: امتى الملف يصغر، وليه النص في الـ PDF يفضل يتحدد، وإيه اللي العلامة المائية بتعمله وإيه اللي مش بتعمله. لو في أداة مقابلة على Creativo Tools، اللينك مكتوب في آخر المقال وواضح إنه موقع تاني.",
        "articles": TOOLS,
    },
    "ai": {
        "nav": "ذكاء اصطناعي",
        "title": "ذكاء اصطناعي",
        "kicker": "ذكاء اصطناعي",
        "desc": "شرح واضح للنماذج اللغوية، والأخطاء الطليقة، والخصوصية، وحقوق الصور المولّدة، والمذاكرة.",
        "intro": "القسم ده مش كتالوج أدوات ولا وعود. بنشرح النموذج بيعمل إيه، ليه الجملة السلسة مش دليل إنها صح، وإيه اللي يحصل لما ترفع ملف لخدمة سحابية. لو بتعلن عن صفحة من هنا، الإعلان لازم يوصف الشرح ده مش منتج مش موجود.",
        "articles": AI,
    },
    "art": {
        "nav": "أخبار الفن",
        "title": "أخبار الفن",
        "kicker": "أخبار الفن",
        "desc": "تغطية لمعارض أكتوبر 2026 من مصادر المتاحف، مع صور مرخّصة وشرح لأصل كل صورة.",
        "intro": "أخبار المعارض هنا متكتوبة من إعلانات المتاحف ووكالات الأنباء وأدلة البرامج المنشورة في أكتوبر 2026. كل صورة ليها صاحب وترخيص. لو الصورة لمبنى أو لوحة قديمة، بنقول كده بصراحة وماندّعيش إنها لقطة من قاعة المعرض.",
        "articles": ART,
    },
}


def esc(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def prefix_for(rel):
    return "../" * rel.count("/")


def public_path(rel):
    if rel == "index.html":
        return ""
    if rel.endswith("/index.html"):
        return rel[: -len("index.html")]
    if rel.endswith(".html"):
        return rel[:-5] + "/"
    return rel


def home_href(prefix):
    return prefix if prefix else "./"


def rewrite_article_links(html):
    def repl(match):
        url = match.group(1)
        if url.startswith(("http://", "https://", "//", "mailto:", "#")):
            return match.group(0)
        frag = ""
        if "#" in url:
            url, frag = url.split("#", 1)
            frag = "#" + frag
        if not url.endswith(".html"):
            return match.group(0)
        url = url[:-5]
        if url.endswith("/index"):
            url = url[: -len("index")]
        elif url == "index":
            url = "./"
        if not url.endswith("/"):
            url += "/"
        if url.startswith("../"):
            url = "../" + url
        elif not url.startswith(("/", "./")):
            url = "../" + url
        return f'href="{url}{frag}"'

    return re.sub(r'href="([^"]+)"', repl, html)


NOTES = {
    "beauty": "ده روتين يومي، مش كشف. لو بشرتك فيها طفح أو حساسية أو حَب تحت الجلد، روح لطبيب جلدية.",
    "health": "الكلام ده معلومة عامة، مش كشف. لو بتشرب دوا أو عندك مرض، اسأل الدكتور قبل ما تغيّر الأكل أو الدوا.",
    "zodiac": "الأبراج تسلية. مش علم، ومش بتتنبأ بيومك، ومش نصيحة صحية أو مالية.",
}


def note_block(section_key):
    text = NOTES.get(section_key)
    if not text:
        return ""
    return f'<p class="note">{esc(text)}</p>'


def logo():
    return (
        '<svg class="mark" viewBox="0 0 32 32" aria-hidden="true">'
        '<rect width="32" height="32" rx="9" fill="#1B2330"/>'
        '<path d="M16 4.2c.45 0 .86.24 1.08.63l5.15 12.05c.55 1.28-.38 2.66-1.74 2.84L16 27.6l-4.49-7.88c-1.36-.18-2.29-1.56-1.74-2.84L14.92 4.83A1.22 1.22 0 0 1 16 4.2z" fill="#F6F1E7"/>'
        '<path d="M16 12.6v7.4" stroke="#C4492C" stroke-width="1.6" stroke-linecap="round"/>'
        '<circle cx="16" cy="10.7" r="1.45" fill="#C4492C"/>'
        "</svg>"
    )


def gtag(prefix):
    if not GOOGLE_TAG_ID:
        return ""
    gid = esc(GOOGLE_TAG_ID)
    return f"""<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{gid}');</script>
"""


def nav(prefix, active):
    items = [
        ("home", home_href(prefix), "الرئيسية"),
        ("general", f"{prefix}general/", "عام"),
        ("beauty", f"{prefix}beauty/", "جمال"),
        ("health", f"{prefix}health/", "صحة"),
        ("zodiac", f"{prefix}zodiac/", "أبراج"),
        ("tools", f"{prefix}tools/", "أدوات"),
        ("ai", f"{prefix}ai/", "ذكاء اصطناعي"),
        ("art", f"{prefix}art/", "أخبار الفن"),
        ("stories", f"{prefix}stories/", "قصص"),
    ]
    links = []
    for key, href, label in items:
        current = ' aria-current="page"' if key == active else ""
        links.append(f'<a href="{href}"{current}>{label}</a>')
    return "".join(links)


def footer(prefix):
    return f'''<footer class="site-footer"><div class="wrap foot">
  <div>
    <p><strong>مداد</strong></p>
    <p>مجلة عربية عن الجمال والصحة والأبراج والمعرفة والأدوات والفن، وفيها قصص أصلية.</p>
  </div>
  <div>
    <ul>
      <li><a href="{prefix}general/">معلومات عامة</a></li>
      <li><a href="{prefix}beauty/">الجمال</a></li>
      <li><a href="{prefix}health/">الصحة</a></li>
      <li><a href="{prefix}zodiac/">أبراج</a></li>
      <li><a href="{prefix}tools/">أدوات</a></li>
      <li><a href="{prefix}ai/">ذكاء اصطناعي</a></li>
      <li><a href="{prefix}art/">أخبار الفن</a></li>
      <li><a href="{prefix}stories/">قصص</a></li>
    </ul>
  </div>
  <div>
    <ul>
      <li><a href="{prefix}about/">عن مداد</a></li>
      <li><a href="{prefix}editorial/">سياسة التحرير</a></li>
      <li><a href="{prefix}privacy/">الخصوصية</a></li>
      <li><a href="{prefix}terms/">شروط الاستخدام</a></li>
    </ul>
  </div>
</div>
<p class="wrap fine">© 2026 مداد. القصص أصلية. صور الأخبار مرخّصة ومصادرها مكتوبة تحت كل صورة. أدوات Creativo Tools على <a href="{TOOLS_ORIGIN}/ar/">creativotools.com</a>.</p>
</footer>'''


def shell(rel, title, description, main, active, robots="index,follow", jsonld="", extra_js=""):
    prefix = prefix_for(rel)
    canonical = ""
    og = ""
    if SITE_URL:
        url = f"{SITE_URL}/{public_path(rel)}"
        canonical = f'<link rel="canonical" href="{esc(url)}">'
        og = (
            f'<meta property="og:title" content="{esc(title)}">'
            f'<meta property="og:description" content="{esc(description)}">'
            f'<meta property="og:type" content="article">'
            f'<meta property="og:locale" content="ar_AR">'
            f'<meta property="og:url" content="{esc(url)}">'
        )
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#1b2330">
{canonical}
{og}
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560;9..144,700&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
{gtag(prefix)}
{jsonld}
</head>
<body>
<a class="skip" href="#content">تجاوز إلى المحتوى</a>
<div class="topline"><div class="wrap"><span>مجلة مداد · أكتوبر 2026</span><a href="{prefix}editorial/">إزاي بنتحقق من الخبر</a></div></div>
<header class="site-header"><div class="wrap bar">
  <a class="logo" href="{home_href(prefix)}">{logo()}<span><strong>مداد</strong><small>{BRAND}</small></span></a>
  <button class="menu-btn" type="button" data-menu aria-expanded="false" aria-controls="site-nav">القائمة</button>
  <nav class="nav" id="site-nav" data-nav>{nav(prefix, active)}</nav>
</div></header>
<main id="content">{main}</main>
{footer(prefix)}
<script src="{prefix}assets/js/site.js"></script>
{extra_js}
</body>
</html>
"""


def write(rel, html):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return public_path(rel)


def ld(payload):
    if not SITE_URL:
        return ""
    return '<script type="application/ld+json">' + json.dumps(payload, ensure_ascii=False) + "</script>"


def article_ld(rel, article, kind):
    if not SITE_URL:
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": kind,
        "headline": article["title"],
        "description": article["description"],
        "inLanguage": "ar",
        "datePublished": article["date_iso"],
        "dateModified": article["date_iso"],
        "author": {"@type": "Organization", "name": "مداد"},
        "publisher": {"@type": "Organization", "name": "مداد"},
        "mainEntityOfPage": f"{SITE_URL}/{public_path(rel)}",
    }
    if article.get("image"):
        data["image"] = f"{SITE_URL}/{article['image']}"
    return ld(data)


def sources_block(article):
    rows = article.get("sources") or []
    if not rows:
        return ""
    items = "".join(
        f'<li><a href="{esc(url)}" rel="noopener noreferrer">{esc(name)}</a></li>'
        for name, url in rows
    )
    return f'<section class="sources"><h2>المصادر</h2><ul>{items}</ul><p>تواريخ المعارض ممكن تتغير. راجع صفحة الجهة قبل الزيارة.</p></section>'


def tool_block(article):
    if not article.get("tool_href"):
        return ""
    return (
        f'<p class="note">الأداة على موقع تاني: Creativo Tools. الملف، حسب شرح الموقع ده، بيتعالج جوه المتصفح.'
        f' <a href="{esc(article["tool_href"])}" rel="noopener noreferrer">صفحة الأداة</a>.</p>'
        f'<p><a class="cta" href="{esc(article["tool_href"])}">افتح {esc(article["tool_label"])}</a></p>'
    )


def related_block(section_key, article, articles):
    others = [item for item in articles if item["slug"] != article["slug"]][:2]
    if not others:
        return ""
    links = "".join(
        f'<a href="../{item["slug"]}/"><span class="kicker {section_key}">{esc(item["kicker"])}</span><br>{esc(item["title"])}</a>'
        for item in others
    )
    return f'<div class="related"><h2>من نفس القسم</h2>{links}</div>'


def render_article(section_key, article, articles):
    meta = SECTIONS[section_key]
    rel = f'{section_key}/{article["slug"]}/index.html'
    prefix = prefix_for(rel)
    figure = ""
    if article.get("image"):
        fig_class = "figure photo" if article.get("frame") == "cover" else "figure"
        figure = (
            f'<figure class="{fig_class}"><img src="{prefix}{article["image"]}" alt="{esc(article.get("alt") or "")}">'
            f'<figcaption>{article["caption"]}</figcaption></figure>'
        )
    crumbs = (
        f'<p class="meta"><a href="{home_href(prefix)}">الرئيسية</a> / '
        f'<a href="{prefix}{section_key}/">{esc(meta["title"])}</a></p>'
    )
    main = f'''<article class="post"><div class="wrap-narrow">
{crumbs}
<p class="kicker {section_key}">{esc(article["kicker"])}</p>
<h1>{esc(article["title"])}</h1>
<p class="meta">تحرير مداد · {esc(article["date_label"])} · حوالي {esc(article["minutes"])} دقائق قراءة</p>
{note_block(section_key)}
{figure}
<div class="prose">{rewrite_article_links(article["body"])}</div>
{tool_block(article)}
{sources_block(article)}
{related_block(section_key, article, articles)}
</div></article>'''
    kind = "NewsArticle" if section_key == "art" else "Article"
    return write(
        rel,
        shell(rel, article["title"] + " | مداد", article["description"], main, section_key, jsonld=article_ld(rel, article, kind)),
    )


def render_section(section_key):
    meta = SECTIONS[section_key]
    articles = meta["articles"]
    cards = []
    for article in articles:
        image = ""
        card_class = "card photo" if article.get("frame") == "cover" else "card"
        if article.get("image"):
            image = f'<img src="../{article["image"]}" alt="{esc(article.get("alt") or "")}">'
        cards.append(
            f'<a class="{card_class}" href="{article["slug"]}/">{image}<span class="pad">'
            f'<span class="kicker {section_key}">{esc(article["kicker"])}</span>'
            f'<h2>{esc(article["title"])}</h2><p>{esc(article["description"])}</p></span></a>'
        )
    main = f'''<section class="page-hero"><div class="wrap">
<p class="kicker {section_key}">{esc(meta["kicker"])}</p>
<h1>{esc(meta["title"])}</h1>
<p class="lede">{esc(meta["intro"])}</p>
{note_block(section_key)}
</div></section>
<section><div class="wrap grid">{"".join(cards)}</div></section>'''
    rel = f"{section_key}/index.html"
    return write(rel, shell(rel, meta["title"] + " | مداد", meta["desc"], main, section_key))


def cover(story, prefix):
    image = story.get("image")
    if not image:
        return (
            f'<div class="cover" style="background:{story["cover"]}">'
            f'<span>{esc(story["genre"])} · {len(story["chapters"])} فصول</span>'
            f'<b>{esc(story["title"])}</b><span>قصة أصلية مكتملة</span></div>'
        )
    return (
        f'<div class="cover has-photo">'
        f'<img src="{prefix}{image}" alt="{esc(story.get("alt") or story["title"])}">'
        f'<div class="cover-shade"><span>{esc(story["genre"])} · {len(story["chapters"])} فصول</span>'
        f'<b>{esc(story["title"])}</b><span>{esc(story.get("hook") or "قصة أصلية مكتملة")}</span></div></div>'
    )


def render_stories_index():
    cards = []
    for story in STORIES:
        cards.append(
            f'<a class="cover-card" data-genres="{esc(story["genre"])}" href="{story["slug"]}/">'
            f'{cover(story, "../")}<p>{esc(story["blurb"])}</p></a>'
        )
    filters = "".join(
        f'<button type="button" data-filter="{esc(genre)}" aria-pressed="{"true" if genre == "all" else "false"}">{esc(label)}</button>'
        for genre, label in [
            ("all", "الكل"),
            ("غموض", "غموض"),
            ("رومانسي", "رومانسي"),
            ("خيال", "خيال"),
            ("دراما", "دراما"),
            ("إثارة", "إثارة"),
        ]
    )
    main = f'''<section class="page-hero"><div class="wrap">
<p class="kicker stories">قصص</p>
<h1>قصص مداد</h1>
<p class="lede">قصص أصلية مصرية، بتتشد فصل ورا فصل. الغلاف رسم للقصة مش صورة حقيقية. مفيش أعداد قراء مزيّفة. آخر فصل وصلته بيتحفظ على جهازك بس.</p>
<div class="filters">{filters}</div>
<div class="story-row">{"".join(cards)}</div>
</div></section>'''
    rel = "stories/index.html"
    extra = f'<script src="{prefix_for(rel)}assets/js/reader.js"></script>'
    return write(rel, shell(rel, "قصص | مداد", "قصص أصلية مصرية من مداد: غموض وإثارة ورومانسي وخيال ودراما، وتتقرى فصلًا فصلًا.", main, "stories", extra_js=extra))


def render_story(story):
    chapters = []
    for index, chapter in enumerate(story["chapters"], start=1):
        chapters.append(
            f'<li><a href="{index}/"><span>فصل {index}</span><span>{esc(chapter["title"])}</span></a></li>'
        )
    main = f'''<section class="story-top wrap">
{cover(story, prefix_for(f'stories/{story["slug"]}/index.html'))}
<div>
<p class="kicker stories">{esc(story["genre"])}</p>
<h1>{esc(story["title"])}</h1>
<p class="meta">كتابة تحرير مداد · قصة أصلية · {len(story["chapters"])} فصول · مكتملة</p>
<p>{story["synopsis"]}</p>
<p class="meta">الغلاف رسم مصاحب للقصة، مش صورة لمكان أو شخص حقيقيين.</p>
<p data-continue="{esc(story["slug"])}"></p>
<ol class="chapter-list">{"".join(chapters)}</ol>
</div>
</section>'''
    rel = f'stories/{story["slug"]}/index.html'
    extra = f'<script src="{prefix_for(rel)}assets/js/reader.js"></script>'
    page = shell(
        rel,
        story["title"] + " | قصص مداد",
        story["blurb"],
        main,
        "stories",
        extra_js=extra,
    )
    written = [write(rel, page)]
    total = len(story["chapters"])
    for index, chapter in enumerate(story["chapters"], start=1):
        prev_link = f'<a href="../{index - 1}/">الفصل السابق</a>' if index > 1 else "<span></span>"
        next_link = (
            f'<a href="../{index + 1}/">الفصل التالي</a>' if index < total else '<a href="../">نهاية القصة</a>'
        )
        percent = int(index / total * 100)
        body = "".join(f"<p>{esc(p)}</p>" for p in chapter["paragraphs"])
        chapter_prefix = prefix_for(f'stories/{story["slug"]}/{index}/index.html')
        still = ""
        if story.get("image"):
            still = (
                f'<figure class="story-still"><img src="{chapter_prefix}{story["image"]}" alt="{esc(story.get("alt") or "")}">'
                f'<figcaption>رسم غلاف للقصة، مش صورة حقيقية.</figcaption></figure>'
            )
        cliff = ""
        if index < total:
            nxt = story["chapters"][index]
            cliff = (
                f'<aside class="cliff"><p>الفصل الجاي</p>'
                f'<a href="../{index + 1}/"><strong>{esc(nxt["title"])}</strong></a></aside>'
            )
        reader = f'''<article class="post"><div class="wrap-narrow" data-reader data-story="{esc(story["slug"])}" data-chapter="{index}" data-title="{esc(story["title"])}">
<div class="reader-bar">
  <a href="../">{esc(story["title"])}</a>
  <div class="controls">
    <button type="button" data-size="-1" aria-label="تصغير الخط">أ-</button>
    <button type="button" data-size="1" aria-label="تكبير الخط">أ+</button>
    <button type="button" data-night>ليلي</button>
  </div>
</div>
<p class="meta">فصل {index} من {total} · {esc(chapter["title"])}</p>
<div class="track" aria-hidden="true"><span style="width:{percent}%"></span></div>
{still}
<div class="reader">{body}{cliff}</div>
<div class="pager">{prev_link}{next_link}</div>
</div></article>'''
        crel = f'stories/{story["slug"]}/{index}/index.html'
        extra = f'<script src="{prefix_for(crel)}assets/js/reader.js"></script>'
        written.append(
            write(
                crel,
                shell(
                    crel,
                    f'{chapter["title"]} | {story["title"]} | مداد',
                    story["blurb"],
                    reader,
                    "stories",
                    extra_js=extra,
                ),
            )
        )
    return written


def static_pages():
    about = '''<article class="post"><div class="wrap-narrow prose">
<h1>عن مداد</h1>
<p>مداد مجلة عربية بتتقرأ من المتصفح. الاسم العربي مداد، واللاتيني Midad. فيها معلومات عامة، وجمال، وصحة فيها أنواع الأكل، وأبراج للتسلية، وأدوات، وذكاء اصطناعي، وأخبار الفن، وقصص أصلية مكتوبة للمصري والعربي.</p>
<p>الموقع مش بيطلب اسم، ولا بريد، ولا كلمة سر، ولا رقم بطاقة. القراءة كلها على الصفحات دي. لو في لينك لأداة على creativotools.com، المقال بيقول إن الموقع تاني، وبيشرح المهارة قبل اللينك.</p>
<p>أخبار الفن بتعتمد على صفحات المتاحف وبياناتها الصحفية وتغطيات منشورة، والتاريخ مكتوب جنب المصدر. الصورة بتبقى إما عمل فني في الملكية العامة، أو صورة مكان برخصة مفتوحة، والتعليق بيقول الفرق.</p>
<p>كل قسم صفحة كاملة لوحدها: عنوانها واضح، ومحتواها عن نفس الموضوع، ومن غير تحويل تلقائي لموقع تاني.</p>
</div></article>'''
    editorial = '''<article class="post"><div class="wrap-narrow prose">
<h1>سياسة التحرير</h1>
<h2>الخبر</h2>
<p>ماننشرش رقم أو اقتباس من غير مصدر نقدر نفتحه. في أخبار المعارض بنفرّق بين اللي قالته الجهة المنظمة، واللي بنستنتجه. لو صورة اللوحة من متحف تاني، بنقول إنها مثال على أسلوب الفنان ومش دليل إنها معلقة في المعرض.</p>
<h2>الصور</h2>
<p>مش بنسحب صورًا صحفية محفوظة الحقوق. الصور المستخدمة من ويكيميديا كومنز، وترخيصها ملكية عامة أو نسب-مشاركة. الاسم والترخيص ظاهرين في التعليق.</p>
<h2>التصحيح</h2>
<p>لو تاريخ معرض اتغير أو اسم اتصحح، التعديل بيظهر في نفس الصفحة مع المصدر. مفيش نموذج مراسلة على الموقع.</p>
<h2>الصحة والجمال والأبراج</h2>
<p>مقالات البشرة والجسم والشعر روتين يومي، ومش روشتة. مقالات الصحة والأكل معلومات عامة، ومش سبب تبطّل الدوا. الأبراج شرح شائع للشخصية والعلاقات والشغل، ومش حكم على حد.</p>
<h2>القصص</h2>
<p>القصص من تأليف مداد. أي تشابه مع أشخاص حقيقيين غير مقصود. مفيش عدّاد قراء ولا تقييمات مصنوعة. غلاف القصة رسم مصاحب للحكاية، ومش صورة لمكان أو لشخص حقيقيين، ومش دليل على حدث.</p>
<h2>الذكاء الاصطناعي في التحرير</h2>
<p>المعلومة المنشورة لازم تتراجع على مصدرها قبل ما تتنشر. النموذج مش مصدر. جملة طليقة من غير صفحة متحف أو مرجع مش بتتتعامل كخبر.</p>
</div></article>'''
    tag_text = (
        "وسم القياس متفعل على الصفحات. جوجل ممكن يحط أو يقرأ ملفات تعريف ارتباط مرتبطة بالوسم ده، ومنها قياس الزيارات وقياس الحملات لو المعرّف بتاع إعلانات جوجل. تقدر تراجع سياسة جوجل على policies.google.com."
        if GOOGLE_TAG_ID
        else "مفيش وسم جوجل أو بكسل إعلان مركّب على الصفحات حاليًا. لو أضفنا معرّف قياس لاحقًا، السياسة دي بتتحدث في نفس الصفحة عشان تقول إنه شغّال وإيه استخدامه."
    )
    privacy = f'''<article class="post"><div class="wrap-narrow prose legal">
<h1>سياسة الخصوصية</h1>
<p>آخر تحديث: 25 أكتوبر 2026. مداد مجلة بتتقري من المتصفح. مش بنعمل حسابات للزوار.</p>
<h2>اللي بيتحفظ على جهازك</h2>
<p>الموقع يستخدم تخزين المتصفح المحلي عشان حاجتين: حجم الخط ووضع القراءة الليلي في القصص، وآخر فصل وصلته في كل قصة. البيانات دي مش بتتبعت لسيرفر، لأن الصفحات مش بتبعت نموذج.</p>
<h2>مفيش حساب ولا بريد</h2>
<p>مداد مش بيجمع أسماء ولا عناوين بريد. مفيش صفحة مراسلة، ومفيش صندوق رسائل على الموقع. مش بنبيع بيانات، لأنه مفيش بيانات زوار عندنا.</p>
<h2>الإعلانات والقياس</h2>
<p>{tag_text} لو فتحت الموقع من إعلان على جوجل، الرابط ممكن يحتوي معامل زي gclid. المعامل ده طريقة جوجل عشان يعرف إن النقرة جت من إعلانه. مداد مش بيخزّن المعامل ده في حساب، لأن مفيش حساب.</p>
<h2>لينكات خارجية</h2>
<p>لينكات Creativo Tools والمتاحف والمصادر بتودّي لمواقع ليها سياساتها. قراءة مداد مش بترفع ملفاتك للمواقع دي. لو فتحت أداة ورفعت ملف، اقرأ شرح الأداة نفسها.</p>
<h2>الأطفال</h2>
<p>المجلة مكتوبة لجمهور عام. مش بنطلب بيانات من أطفال عن قصد.</p>
</div></article>'''
    terms = '''<article class="post"><div class="wrap-narrow prose legal">
<h1>شروط الاستخدام</h1>
<p>باستخدامك مداد فأنت بتقرأ مجلة. المحتوى رأي وشرح عام، مش استشارة قانونية أو طبية أو مالية. صفحات الجمال والصحة والدايت مش بتتشخص ولا بتوصف دوا. صفحات الأبراج تسلية، ومش تنبؤ.</p>
<h2>القصص</h2>
<p>القصص ملك مداد. تقدر تشارك رابط الفصل. إعادة نشر النص كامل مش مسموحة.</p>
<h2>الأخبار</h2>
<p>تواريخ المعارض وأسماء القاعات مأخوذة من المصادر المكتوبة تحت المقال وقت النشر. الجهة المنظمة هي اللي بتأكد موعد الزيارة. صورة اللوحة القديمة ملكيتها العامة كعمل فني، ونسبها للفنان، ومش معناها إن مداد يملك اللوحة.</p>
<h2>الأدوات</h2>
<p>شرح المهارة على مداد. تنفيذ الأداة، لو موجود، على creativotools.com وبشروط الموقع ده. حدود الملفات المذكورة في المقال هي حدود الأداة كما وُصفت وقت الكتابة، وممكن تتغير على موقع الأداة.</p>
<h2>الاستخدام المقبول</h2>
<p>متستخدمش الموقع عشان تنتحل صفة التحرير، أو تجمع بيانات الزوار، أو تعرض محتوى القصص على إنه تجربة شخص حقيقي.</p>
</div></article>'''
    pages = {
        "about/index.html": ("عن مداد", "مداد مجلة عربية بأقسام المعرفة والأدوات والذكاء الاصطناعي وأخبار الفن والقصص، ومن غير نماذج ولا حسابات.", about, "home"),
        "editorial/index.html": ("سياسة التحرير", "إزاي مداد بتكتب الخبر، وبتختار الصور، وبتصحح الأخطاء.", editorial, "home"),
        "privacy/index.html": ("سياسة الخصوصية", "البيانات اللي مداد بيحفظها على جهازك، ووضع قياس الإعلانات.", privacy, "home"),
        "terms/index.html": ("شروط الاستخدام", "شروط قراءة مجلة مداد واستخدام نصوصها وروابطها.", terms, "home"),
    }
    written = []
    for rel, (title, desc, body, active) in pages.items():
        written.append(write(rel, shell(rel, title + " | مداد", desc, body, active)))
    return written


def render_home(paths):
    by_slug = {article["slug"]: article for article in ART}
    lead = by_slug["louvre-abu-dhabi-spices"]
    sides = [
        by_slug["cairo-alive-archive"],
        by_slug["cassatt-orsay"],
        by_slug["zurbaran-louvre"],
    ]
    side_html = []
    for article in sides:
        side_html.append(
            f'<a class="sideitem" href="art/{article["slug"]}/">'
            f'<img src="{article["image"]}" alt="{esc(article.get("alt") or "")}">'
            f'<div><p class="kicker art">أخبار الفن</p><h3>{esc(article["title"])}</h3>'
            f'<p>{esc(article["date_label"])}</p></div></a>'
        )
    desks = "".join(
        f'<a class="desk {key}" href="{key}/"><span>{esc(meta["kicker"])}</span>'
        f'<strong>{esc(meta["title"])}</strong><em>{len(meta["articles"])} مقالات</em></a>'
        for key, meta in SECTIONS.items()
    )
    desks += (
        f'<a class="desk stories" href="stories/"><span>قصص</span>'
        f'<strong>قصص</strong><em>{len(STORIES)} قصص مكتملة</em></a>'
    )

    def trio(key, count=3):
        bits = []
        for article in SECTIONS[key]["articles"][:count]:
            image = ""
            card_class = "card photo" if article.get("frame") == "cover" else "card"
            if article.get("image"):
                image = f'<img src="{article["image"]}" alt="{esc(article.get("alt") or "")}">'
            bits.append(
                f'<a class="{card_class}" href="{key}/{article["slug"]}/">{image}<span class="pad">'
                f'<span class="kicker {key}">{esc(article["kicker"])}</span>'
                f'<h2>{esc(article["title"])}</h2><p>{esc(article["description"])}</p></span></a>'
            )
        title = SECTIONS[key]["title"]
        return (
            f'<section class="tint tint-{key}"><div class="wrap"><div class="section-head"><h2>{esc(title)}</h2>'
            f'<a href="{key}/">كل القسم</a></div><div class="grid">{"".join(bits)}</div></div></section>'
        )

    story_cards = "".join(
        f'<a class="cover-card" href="stories/{story["slug"]}/">{cover(story, "")}<p>{esc(story["blurb"])}</p></a>'
        for story in STORIES
    )
    lead_story = next(story for story in STORIES if story["slug"] == "last-microbus")
    main = f'''<section class="hero"><div class="wrap hero-split">
<div>
<p class="kicker">مجلة مداد</p>
<h1>اقرَأ بوضوح، واستخدم الأداة وأنت فاهم حدودها.</h1>
<p class="lede">جمال وصحة وأنواع أكل، وأبراج للتسلية، ومعرفة عامة، وأدوات، وذكاء اصطناعي، وأخبار فن من مصادرها، وقصص أصلية تتقرى فصل ورا فصل.</p>
<p class="hero-links"><a class="hero-btn" href="stories/last-microbus/">ابدأ بقصة</a><a class="hero-btn ghost" href="beauty/">الجمال</a><a class="hero-btn ghost" href="health/">الصحة</a><a class="hero-btn ghost" href="zodiac/">الأبراج</a></p>
</div>
<a class="hero-story" href="stories/last-microbus/">
<img src="{lead_story["image"]}" alt="{esc(lead_story.get("alt") or "")}">
<span><small>{esc(lead_story["genre"])}</small><strong>{esc(lead_story["title"])}</strong><em>{esc(lead_story["hook"])}</em></span>
</a>
</div></section>
<section class="story-band"><div class="wrap"><div class="section-head"><h2>قصص تتشاف قبل ما تتقرى</h2><a href="stories/">المكتبة</a></div>
<div class="story-row">{story_cards}</div></div></section>
<section><div class="wrap home-grid">
<a class="feature" href="art/{lead["slug"]}/">
<img src="{lead["image"]}" alt="{esc(lead.get("alt") or "")}">
<div><p class="kicker art">{esc(lead["kicker"])} · {esc(lead["date_label"])}</p><h2>{esc(lead["title"])}</h2><p>{esc(lead["description"])}</p></div>
</a>
<div class="sidestack">{"".join(side_html)}</div>
</div></section>
<section><div class="wrap desks">{desks}</div></section>
{trio("beauty")}
{trio("health", 6)}
{trio("zodiac", 6)}
{trio("general")}
{trio("tools")}
{trio("ai")}'''
    org = ""
    if SITE_URL:
        org = ld({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "مداد",
            "alternateName": BRAND,
            "url": SITE_URL + "/",
            "description": "مجلة عربية للمعرفة والأدوات والذكاء الاصطناعي وأخبار الفن والقصص.",
        })
    return write(
        "index.html",
        shell(
            "index.html",
            "مداد | مجلة المعرفة والأدوات والفن والقصص",
            "مجلة مداد: معلومات عامة، شرح أدوات، ذكاء اصطناعي، أخبار فن حقيقية، وقصص أصلية.",
            main,
            "home",
            jsonld=org,
        ),
    )


def write_robots(urls):
    lines = ["User-agent: *", "Allow: /", ""]
    if SITE_URL:
        sitemap = ROOT / "sitemap.xml"
        body = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]
        for rel in urls:
            body.append(f"  <url><loc>{esc(SITE_URL + '/' + rel)}</loc><lastmod>2026-10-25</lastmod></url>")
        body.append("</urlset>\n")
        sitemap.write_text("\n".join(body), encoding="utf-8")
        lines.append(f"Sitemap: {SITE_URL}/sitemap.xml")
    else:
        leftover = ROOT / "sitemap.xml"
        if leftover.exists():
            leftover.unlink()
        lines.append("# Set SITE_URL in build_blog.py and rebuild to publish an absolute sitemap.")
    (ROOT / "robots.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def cleanup_legacy_pages():
    for name in ("about.html", "editorial.html", "privacy.html", "terms.html", "ads.html", "contact.html"):
        path = ROOT / name
        if path.is_file():
            path.unlink()
    for key in list(SECTIONS) + ["stories"]:
        folder = ROOT / key
        if not folder.exists():
            continue
        for path in folder.rglob("*.html"):
            if path.name != "index.html":
                path.unlink()


def main():
    cleanup_legacy_pages()
    old_posts = ROOT / "posts"
    if old_posts.exists():
        shutil.rmtree(old_posts)
    old_ads = ROOT / "ads.html"
    if old_ads.exists():
        old_ads.unlink()
    old_contact = ROOT / "contact.html"
    if old_contact.exists():
        old_contact.unlink()

    urls = []
    for key in SECTIONS:
        urls.append(render_section(key))
        articles = SECTIONS[key]["articles"]
        for article in articles:
            urls.append(render_article(key, article, articles))
    urls.append(render_stories_index())
    for story in STORIES:
        urls.extend(render_story(story))
    urls.extend(static_pages())
    urls.append(render_home(urls))
    write_robots(urls)
    print(f"Wrote {len(urls)} pages")


if __name__ == "__main__":
    main()
