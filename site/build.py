# Aasteria Multimedia static site builder.
# Edit the DATA block below, then run:  python3 build.py
import os, re, html, datetime, json, urllib.request, urllib.parse
E = html.escape
SITE = "https://aasteria.com"

# ======================= DATA: EDIT HERE =======================
# Our work: one list for everything. Types: design, social, video, bts, web, print.
# Add an item: copy a line, change type, title, line and img (put the file in /img/).
# Video items need "id" (the YouTube ID, the part after v= in the link) and no img.
# Website items can have "url" (shows a Visit website link). Optional "w" and "h" are the image width and height in pixels.
WORK = [
 # ── Websites ──
 {"type": "web", "title": "Dr. Nandan Ortho", "line": "Website for an orthopaedic clinic in Surat.", "img": "img/web-drnandanortho.webp", "url": "https://drnandanortho.com/"},
 {"type": "web", "title": "Aasteria Multimedia", "line": "Our own agency website — design, build and SEO by us.", "img": "img/web-aasteria.webp", "url": "https://aasteria.com/"},
 # ── Edited Reels (YouTube Shorts: set "id" to the YouTube video ID) ──
 # ── Edited Reels (Instagram: set "url" to the Instagram reel link, "img" to a cover image) ──
 {"type": "reel", "title": "Placeholder Reel 1", "line": "Replace with reel description.", "id": "dQw4w9WgXcQ"},
 {"type": "reel", "title": "Placeholder Reel 2 (Instagram)", "line": "Replace with reel description.", "url": "https://www.instagram.com/aasteria_multimedia/", "img": "img/ph-video.webp"},
 # ── Graphic Design ──
 {"type": "design", "title": "Placeholder poster design", "line": "Replace with the client and what you made.", "img": "img/ph-design.webp"},
 {"type": "design", "title": "Placeholder logo design", "line": "Replace with the client and what you made.", "img": "img/ph-design.webp"},
 # ── Social Media ──
 {"type": "social", "title": "Placeholder social media post", "line": "Replace with the client and the campaign.", "img": "img/ph-social.webp"},
 # ── Edited Videos ──
 {"type": "video", "title": "Placeholder edited video", "line": "Replace with what the video was for.", "id": "dQw4w9WgXcQ"},
 # ── Behind the Scenes ──
 {"type": "bts", "title": "Placeholder behind the scenes", "line": "Replace with where and what you were shooting.", "img": "img/ph-bts.webp"},
 # ── Print ──
 {"type": "print", "title": "Placeholder brochure design", "line": "Replace with the client and the print job.", "img": "img/ph-print.webp"},
]
CATS = [("design", "Graphic design"), ("social", "Social media"), ("video", "Edited videos"), ("reel", "Edited Reels"), ("bts", "Behind the scenes"), ("web", "Websites"), ("print", "Print")]
# Add a client: name plus a logo in /img/ (WebP, 240x120). Six or more clients gives two scrolling rows.
CLIENTS = [{"name": "Placeholder client %d" % i, "img": "img/logo-client.webp"} for i in range(1, 9)]
# Paste your Google Business link (the share link from Google Maps). It powers the "Read all on Google" button.
GOOGLE_BUSINESS_URL = ""
# Replace each text with a real Google review before launch.
REVIEWS = [{"who": "Client name", "text": "Paste a real Google review here."} for _ in range(5)]
# Add a post: new entry at the TOP. "slug" becomes /blog/slug/. Body is HTML.
POSTS = [
 {"slug": "how-multimedia-is-used-in-business", "title": "How multimedia is used in business", "date": "2020-01-01",
  "desc": "Where video, audio, graphics and animation fit in a business, and what each one does for sales.",
  "body": "<p>Multimedia means mixing text, images, audio and video in one message. Businesses use it because people remember what they see and hear more than what they read.</p><h2>Where it is used</h2><p>Product videos show how something works in under a minute. Explainer animations make hard ideas simple. Social posts with strong visuals get shared. Training videos save staff hours.</p><h2>How to start</h2><p>Pick one goal, such as more enquiries. Make one short video or one clear graphic for it. Measure the result, then repeat what worked.</p>"},
 {"slug": "helpful-tips-about-lead-generation", "title": "Helpful tips about lead generation", "date": "2020-01-02",
  "desc": "Practical ways a small business can get more enquiries from its website and social pages.",
  "body": "<p>A lead is a person who has shown interest and shared a way to contact them. Getting more of them is mostly about making the next step obvious.</p><h2>Make contact easy</h2><p>Put a phone number, WhatsApp link and short form on every page. Fewer fields means more people finish the form.</p><h2>Give a reason to reply</h2><p>Offer something useful, like a free site check or a price estimate. Answer every enquiry the same day.</p><h2>Track the source</h2><p>Note where each lead came from. Spend more on the channel that brings real customers.</p>"},
 {"slug": "best-advice-for-writing-a-blog", "title": "Best advice for writing a blog", "date": "2020-01-03",
  "desc": "Simple rules for writing blog posts that people read and search engines can find.",
  "body": "<p>Good blog posts answer one question well. Start there.</p><h2>Pick one topic per post</h2><p>Write the question your customer would type into Google, and use it as the title.</p><h2>Write short</h2><p>Use short sentences and short paragraphs. Add a heading every few paragraphs so readers can scan.</p><h2>Finish with a next step</h2><p>Tell the reader what to do next: call, message or read a related post.</p>"},
]
# ===============================================================

NAME="Aasteria Multimedia"; TAG="A One-Click Complete Media Solutions"
EMAIL="info@aasteria.com"; PHONE="+91 70488 05418"; WA="917048805418"
SOC=[("Facebook","https://www.facebook.com/"),("Instagram","https://www.instagram.com/aasteria_multimedia/"),("Twitter","https://twitter.com/"),("LinkedIn","https://www.linkedin.com/"),("Pinterest","https://www.pinterest.com/"),("Behance","https://www.behance.net/aasterimultimedia")]
SERV=[("Digital Marketing","Ads and search work that bring enquiries to your phone and inbox."),("Web and App Development","Fast sites and apps that still load well on a slow mobile connection."),("Branding Design","A logo, colours and a short guide, so your brand looks the same everywhere."),("Social Media","We plan the posts, make them and answer the comments."),("Print Media","Brochures, banners and visiting cards, designed and ready for the press."),("Video Production","Product films, ads and event videos, shot and edited by us.")]
SERV_IC=["marketing","web","brand","social","print","video"]
FAQ=[("What does a digital marketing agency in Surat do?","We run your online marketing: the website, social pages, ads, content and video. The aim is simple. More people find you and contact you."),("Do you work with clients outside Surat?","Yes. We also work from Mumbai and Kolkata, and most projects run fully online."),("How long does a website take?","A simple business site takes two to three weeks once we have your text and photos."),("How much does it cost?","It depends on the work. Message us what you need and we will send a clear quote."),("Can one team handle everything?","Yes. Websites, branding, social media, print and video are all done by the same team.")]
GOALS=[("Get more calls and enquiries",[0,3,1],"Ads and search bring people in. Social posts keep you in front of them. A fast site turns visits into calls."),("Sell more online",[1,0,5],"A site or app that works well on a phone comes first. Ads send people to it. A short product video helps them decide."),("Look more professional",[2,4,5],"Start with the logo and brand guide. Then print the same look on cards and brochures. A brand video finishes the job.")]

# Google reviews: set GOOGLE_PLACES_KEY and GOOGLE_PLACE_ID as build environment variables (see README).
GOOGLE_KEY=os.environ.get("GOOGLE_PLACES_KEY",""); PLACE_ID=os.environ.get("GOOGLE_PLACE_ID","")
RATING,COUNT="5.0","32"
def google_reviews():
    if not (GOOGLE_KEY and PLACE_ID): return None
    try:
        req=urllib.request.Request("https://places.googleapis.com/v1/places/"+PLACE_ID,headers={"X-Goog-Api-Key":GOOGLE_KEY,"X-Goog-FieldMask":"rating,userRatingCount,reviews"})
        d=json.load(urllib.request.urlopen(req,timeout=15))
        out=[{"who":r.get("authorAttribution",{}).get("displayName","Google user"),"text":(r.get("text") or r.get("originalText") or {}).get("text",""),"rating":r.get("rating",5),"when":r.get("relativePublishTimeDescription","")} for r in d.get("reviews",[])]
        return d.get("rating"),d.get("userRatingCount"),[r for r in out if r["text"]]
    except Exception as e:
        print("Google reviews not fetched, using the list in build.py:",e); return None
G=google_reviews()
if G:
    if G[0]: RATING="%.1f"%G[0]
    if G[1]: COUNT=str(G[1])
    if G[2]: REVIEWS=G[2]
MAPS=GOOGLE_BUSINESS_URL or (("https://search.google.com/local/reviews?placeid="+PLACE_ID) if PLACE_ID else "https://www.google.com/maps/search/?api=1&query=Aasteria+Multimedia+Surat")
WRITE=("https://search.google.com/local/writereview?placeid="+PLACE_ID) if PLACE_ID else MAPS

ICONS={"marketing":"M4 10v4h3l8 4V6L7 10H4z M18 9c1.5 1 1.5 5 0 6","web":"M8 7l-5 5 5 5 M16 7l5 5-5 5 M14 5l-4 14","brand":"M12 2l8 8-8 12-8-12z M4 10h16","social":"M18 8a3 3 0 100-6 3 3 0 000 6z M6 15a3 3 0 100-6 3 3 0 000 6z M18 22a3 3 0 100-6 3 3 0 000 6z M8.6 13.5l6.8 4 M15.4 6.5l-6.8 4","print":"M7 9V3h10v6 M7 17H4v-7h16v7h-3 M7 14h10v7H7z","video":"M3 6h13v12H3z M16 10l5-3v10l-5-3","work":"M3 3h8v8H3z M13 3h8v8h-8z M3 13h8v8H3z M13 13h8v8h-8z","clients":"M9 11a4 4 0 100-8 4 4 0 000 8z M2 21c0-4 3-7 7-7s7 3 7 7 M17 4a4 4 0 010 7 M22 21c0-3-2-5-4-6","about":"M12 12a4 4 0 100-8 4 4 0 000 8z M4 21c0-4 4-7 8-7s8 3 8 7","faq":"M12 22a10 10 0 100-20 10 10 0 000 20z M9.5 9.5a2.5 2.5 0 114 2c-1 .7-1.5 1-1.5 2 M12 17v.5","blog":"M5 3h10l4 4v14H5z M14 3v5h5 M8 12h8 M8 16h8","mail":"M3 5h18v14H3z M3 6l9 7 9-7","target":"M12 22a10 10 0 100-20 10 10 0 000 20z M12 17a5 5 0 100-10 5 5 0 000 10z M12 13a1 1 0 100-2 1 1 0 000 2z","phone":"M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z","pin":"M12 22s7-6 7-12a7 7 0 10-14 0c0 6 7 12 7 12z M12 12a2.5 2.5 0 100-5 2.5 2.5 0 000 5z","search":"M11 19a8 8 0 100-16 8 8 0 000 16z M21 21l-4.3-4.3","heart":"M12 21s-8-5-8-11a4.5 4.5 0 018-3 4.5 4.5 0 018 3c0 6-8 11-8 11z","check":"M5 12l4 4 10-10","star2":"M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"}
def sprite():
    x=''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24" '+('fill="currentColor"' if k=="star2" else 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"')+f'><path d="{v}"/></symbol>' for k,v in ICONS.items())
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true">{x}</svg>'
def ic(n,c="icon"): return f'<svg class="{c}" width="24" height="24" aria-hidden="true"><use href="#i-{n}"/></svg>'
def H(n,t): return f'<h2 class="has-icon">{ic(n)}<span>{E(t)}</span></h2>'
def WAL(t): return f"https://wa.me/{WA}?text="+urllib.parse.quote(t)
def CTL(i): return f'<div class="scroll-buttons"><button class="button plain" data-scroll="{i}" data-dir="-1">Previous</button><button class="button plain" data-scroll="{i}" data-dir="1">Next</button></div>'
def uri(svg): return 'url("data:image/svg+xml,'+svg.replace("<","%3C").replace(">","%3E").replace("#","%23")+'")'
def dots(c,o): return uri(f"<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20'><circle cx='3' cy='3' r='2' fill='{c}' fill-opacity='{o}'/></svg>")
def lines(c,o): return uri(f"<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16'><path d='M0 16L16 0' stroke='{c}' stroke-opacity='{o}' stroke-width='1.5'/></svg>")

CSS="""
:root{--bg:#FAFAFA;--alt:#F3EDF7;--fg:#1E1226;--mu:#5A4A66;--pu:#6A1B9A;--pk:#D6106A;--lp:#FF1F7A;--ln:#DDD0E6;--s1:8px;--s2:16px;--s3:24px;--s4:32px;--s6:48px;--s8:64px;--s12:96px;--r:8px;--sh:0 8px 24px rgba(106,27,154,.22)}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:80px}
body{margin:0;font:18px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:var(--bg);color:var(--fg)}
img{max-width:100%;height:auto;display:block}a{color:var(--pu);transition:color .3s}a:hover{color:var(--pk)}::selection{background:rgba(214,16,106,.28)}
a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible,summary:focus-visible{outline:3px solid var(--pk);outline-offset:2px}
.wrap{max-width:1040px;margin:0 auto;padding:0 var(--s3)}
main>section{position:relative;padding:var(--s8) 0}main>section:nth-of-type(even){background:var(--alt)}main>section>.wrap{position:relative;z-index:1}
h1,h2,h3{color:var(--pu);line-height:1.2;margin:0 0 var(--s2)}h1{font-size:clamp(2.25rem,6vw,4rem);max-width:14ch}h2{font-size:1.75rem}h3{font-size:1.125rem}
p{margin:0 0 var(--s2);max-width:60ch}.muted{color:var(--mu);font-size:.875rem}p.muted{font-size:1rem}
.skip{position:absolute;left:-999px}.skip:focus{left:var(--s2);top:var(--s2);background:var(--bg);padding:var(--s1);z-index:99}
.progress{position:fixed;top:0;left:0;height:4px;width:100%;background:var(--lp);transform:scaleX(0);transform-origin:0 50%;z-index:99}
.icon{flex:none;width:24px;height:24px}
.site-header{position:sticky;top:0;z-index:5;background:rgba(250,250,250,.92);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-bottom:1px solid var(--ln);transition:box-shadow .3s}.site-header.scrolled{box-shadow:var(--sh)}
.site-header .wrap{display:flex;align-items:center;gap:var(--s3);height:64px}
.logo{display:flex;align-items:center;flex:none}.logo img{height:40px;width:auto}
.site-nav{display:flex;gap:var(--s3);overflow-x:auto;margin-left:auto}.site-nav a{color:var(--pu);font-weight:600;text-decoration:none;padding:var(--s1) 0;white-space:nowrap;border-bottom:3px solid transparent;transition:border-color .2s,color .3s}.site-nav a:hover{color:var(--pk)}.site-nav a.active{border-bottom-color:var(--lp)}
.button{position:relative;overflow:hidden;display:inline-block;padding:12px var(--s3);background:var(--pk);color:#fff;text-decoration:none;font:inherit;font-weight:600;border:2px solid var(--pk);border-radius:var(--r);cursor:pointer;transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s,background-color .3s,color .3s}
.button:hover{background:var(--pu);border-color:var(--pu);color:#fff;transform:translateY(-3px);box-shadow:var(--sh)}.button:active{transform:none;box-shadow:none}
.button.plain{background:rgba(106,27,154,.08);color:var(--pu);border-color:var(--pu)}.button.plain:hover{background:var(--pu);color:#fff}
.button-row{display:flex;gap:var(--s2);flex-wrap:wrap;margin-top:var(--s3)}
.ripple{position:absolute;width:20px;height:20px;border-radius:50%;background:rgba(255,255,255,.45);transform:translate(-50%,-50%) scale(0);animation:ripple .6s ease-out forwards;pointer-events:none}
main a:not(.button){text-decoration:underline;text-decoration-color:transparent;text-underline-offset:4px;transition:color .3s,text-decoration-color .3s}main a:not(.button):hover{text-decoration-color:currentColor}
.has-icon{display:flex;align-items:center;gap:var(--s2)}.has-icon .icon{width:48px;height:48px;padding:12px;background:var(--pu);color:#fff;border-radius:var(--r);transition:transform .3s,background-color .3s}.has-icon:hover .icon{transform:rotate(-8deg) scale(1.08);background:var(--pk)}
main>section:nth-of-type(3n+2) .has-icon .icon{background:var(--pk)}main>section:nth-of-type(3n) .has-icon .icon{background:var(--lp)}
main>section:not(.hero):not(.cta-band)::before{content:"";position:absolute;pointer-events:none;z-index:0}
main>section:nth-of-type(odd):not(.hero):not(.cta-band)::before{right:var(--s3);top:var(--s3);width:160px;height:160px;background:DOTS_P}
main>section:nth-of-type(even):not(.cta-band)::before{left:0;bottom:0;width:200px;height:96px;background:LINES_P}
.hero{position:relative;overflow:hidden;background:#1E1226;color:#F3EDF7;padding:var(--s12) 0 128px}.hero::before{content:"";position:absolute;left:0;bottom:0;width:360px;height:240px;background:DOTS_K;pointer-events:none}
.hero h1{color:#fff}.hero .button.plain{background:transparent;color:#fff;border-color:#fff}.hero .button.plain:hover{background:#fff;color:#1E1226}
.hero .wrap{display:grid;gap:var(--s6);grid-template-columns:repeat(auto-fit,minmax(280px,1fr));align-items:center}
@keyframes rise{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}.hero .wrap>*{animation:rise .7s both}.hero .wrap>*:nth-child(2){animation-delay:.2s}
.deco-hero{position:absolute;right:-120px;top:-80px;width:640px;height:640px;pointer-events:none;z-index:0}.deco-hero circle{transform-box:fill-box;transform-origin:center;animation:pulse 6s ease-in-out infinite}.deco-hero circle:nth-child(2){animation-delay:1s}.deco-hero circle:nth-child(3){animation-delay:2s}
.deco-hero g:first-of-type circle:nth-child(1){fill:rgba(255,31,122,.16)}.deco-hero g:first-of-type circle:nth-child(2){fill:rgba(106,27,154,.28)}.deco-hero g:first-of-type circle:nth-child(3){fill:rgba(106,27,154,.14)}.flow{animation:flow 8s linear infinite}
@keyframes pulse{50%{transform:scale(1.06)}}@keyframes flow{to{stroke-dashoffset:-160}}@keyframes grow{from{transform:scaleY(0)}}@keyframes draw{to{stroke-dashoffset:0}}@keyframes bob{50%{transform:translateY(-8px)}}@keyframes slide{to{transform:translateX(-50%)}}@keyframes ripple{to{transform:translate(-50%,-50%) scale(14);opacity:0}}@keyframes ring{from{box-shadow:0 0 0 0 rgba(214,16,106,.55)}to{box-shadow:0 0 0 16px rgba(214,16,106,0)}}@keyframes open{from{opacity:0;transform:translateY(-8px)}}@keyframes fill{to{transform:scaleX(1)}}
.hero-graphic{width:100%;height:auto;filter:drop-shadow(0 8px 16px rgba(30,18,38,.16))}.gp{fill:#fff;stroke:#DDD0E6}
.bars rect{fill:#6A1B9A;transform-box:fill-box;transform-origin:50% 100%;animation:grow .9s both}.bars rect:nth-child(2){animation-delay:.1s}.bars rect:nth-child(3){animation-delay:.2s}.bars rect:nth-child(4){animation-delay:.3s}.bars rect:nth-child(5){animation-delay:.4s}.bars .hot{fill:#D6106A}
.trend{fill:none;stroke:#FF1F7A;stroke-width:4;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:400;stroke-dashoffset:400;animation:draw 1.4s .7s forwards}.dot{fill:#FF1F7A}
.chip-g{animation:bob 3s ease-in-out infinite}.chip-g.c2{animation-delay:1s}.chip-g.c3{animation-delay:2s}.chip-g.c4{animation-delay:.5s}.chip{fill:rgba(243,237,247,.95);stroke:#DDD0E6}.chip-i{color:#6A1B9A}
.stats{margin-top:-64px;position:relative;z-index:2}.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));background:rgba(250,250,250,.88);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border:1px solid rgba(106,27,154,.22);border-radius:var(--r);box-shadow:var(--sh)}
.stats-grid>div{padding:var(--s3);border-right:1px solid rgba(106,27,154,.18);transition:background-color .3s}.stats-grid>div:hover{background:rgba(214,16,106,.07)}.stats-grid p{margin:0}.stat-icon{width:32px;height:32px;color:var(--pu);margin-bottom:var(--s1)}.stats-grid>div:nth-child(even) .stat-icon{color:var(--pk)}
.stat-number{font-size:3.5rem;font-weight:700;line-height:1;color:var(--lp);margin-bottom:var(--s1)!important}
.marquee{margin-top:var(--s8);background:rgba(106,27,154,.96);color:#fff;overflow:hidden;white-space:nowrap;padding:var(--s2) 0;font-weight:700;font-size:1.125rem}.marquee-track{display:flex;width:max-content;animation:slide 32s linear infinite}.marquee:hover .marquee-track{animation-play-state:paused}
.marquee-track span{display:flex;gap:var(--s6);padding-right:var(--s6)}.marquee b{display:flex;align-items:center;gap:var(--s1)}.marquee b::after{content:"";width:8px;height:8px;border-radius:50%;background:#FF1F7A;margin-left:var(--s4)}
.service-grid{list-style:none;padding:0;margin:var(--s4) 0 0;display:grid;gap:var(--s3);grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.service-card{background:rgba(255,255,255,.72);border:1px solid rgba(106,27,154,.18);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);border-radius:var(--r);padding:var(--s4);transition:transform .2s ease-out,box-shadow .3s,border-color .2s,background-color .3s}
.service-card:hover{transform:translateY(-6px);box-shadow:var(--sh);border-color:var(--pk);background:rgba(214,16,106,.06)}.service-card p{margin-bottom:var(--s2)}.more{font-weight:700}
.big-icon{width:72px;height:72px;padding:16px;background:var(--pu);color:#fff;border-radius:var(--r);margin-bottom:var(--s2);transition:background-color .2s}.service-card:nth-child(3n+2) .big-icon{background:var(--pk)}.service-card:nth-child(3n) .big-icon{background:var(--lp)}.service-card:hover .big-icon{background:var(--pu)}.service-card:nth-child(3n+1):hover .big-icon{background:var(--pk)}
.checks{list-style:none;padding:0;margin:var(--s3) 0}.checks li{display:flex;gap:var(--s1);margin-bottom:var(--s1)}.checks .icon{color:var(--pk);margin-top:2px}
.about .wrap{display:grid;gap:var(--s6);grid-template-columns:repeat(auto-fit,minmax(260px,1fr));align-items:center}
.founder{position:relative;margin:0;max-width:340px;padding:0 var(--s3) 0 0}.founder::before{content:"";position:absolute;right:0;top:var(--s4);width:90%;aspect-ratio:1;border-radius:50%;background:rgba(106,27,154,.2)}.founder::after{content:"";position:absolute;left:-8px;top:var(--s3);width:24px;height:24px;border-radius:50%;background:var(--lp)}
.founder img{position:relative;z-index:1;width:100%;height:auto;border-radius:50%;box-shadow:0 0 0 6px var(--bg),0 0 0 10px var(--pk)}.founder figcaption{position:relative;z-index:1;margin-top:var(--s3)}
main>section.start{background:rgba(214,16,106,.07)}main>section.process{background:rgba(255,31,122,.06)}main>section.reviews{background:rgba(106,27,154,.08)}
.goal-buttons{display:flex;flex-wrap:wrap;gap:var(--s2);margin:var(--s3) 0}.goal{font:inherit;font-weight:600;padding:12px var(--s3);background:rgba(106,27,154,.08);color:var(--pu);border:2px solid var(--pu);border-radius:var(--r);cursor:pointer;transition:transform .35s cubic-bezier(.2,.8,.2,1),background-color .3s,color .3s}.goal:hover,.goal[aria-pressed=true]{background:var(--pu);color:#fff}.goal:hover{transform:translateY(-3px)}
.goal-result{background:rgba(255,255,255,.8);border:1px solid rgba(106,27,154,.2);border-radius:var(--r);padding:var(--s4);box-shadow:var(--sh);margin-bottom:var(--s2)}.goal-result.on{animation:rise .4s both}.js .goal-result{display:none}.js .goal-result.on{display:block}
.goal-services{display:flex;flex-wrap:wrap;gap:var(--s2);list-style:none;padding:0;margin:0 0 var(--s3)}.goal-services li{display:flex;align-items:center;gap:var(--s1);font-weight:600;color:var(--pu)}
.process-list{display:grid;gap:var(--s3);grid-template-columns:repeat(auto-fit,minmax(220px,1fr));list-style:none;padding:0;margin:var(--s4) 0 0}.process-list li{position:relative;border-top:4px solid var(--pu);padding-top:var(--s2);transition:border-color .3s,transform .3s}.process-list li:nth-child(even){border-top-color:var(--pk)}.process-list li:nth-child(3n){border-top-color:var(--lp)}.process-list li:hover{border-top-color:var(--pk);transform:translateY(-4px)}
.process-list li::before{content:"";position:absolute;top:-10px;left:0;width:16px;height:16px;border-radius:50%;background:var(--pk)}.step-top{display:flex;justify-content:space-between;align-items:flex-start}.step-top .icon{width:32px;height:32px;color:var(--pu)}.step-num{font-size:3rem;font-weight:700;color:var(--lp);line-height:1;margin:0 0 var(--s1)}
.section-head{display:flex;justify-content:space-between;align-items:end;gap:var(--s2);flex-wrap:wrap}.scroll-buttons{display:flex;gap:var(--s1)}.scroll-buttons .button{padding:var(--s1) var(--s2)}
.h-scroll{display:flex;gap:var(--s3);overflow-x:auto;scroll-snap-type:x mandatory;list-style:none;margin:var(--s1) 0 0;padding:var(--s2) var(--s1) var(--s4);cursor:grab;scrollbar-color:#6A1B9A #DDD0E6}.h-scroll.drag{cursor:grabbing;user-select:none}.h-scroll>li{flex:0 0 min(82%,380px);scroll-snap-align:start}
.project-card,.video-card{background:rgba(255,255,255,.8);border-radius:var(--r);box-shadow:var(--sh);padding-bottom:var(--s2);overflow:hidden;transition:transform .2s ease-out,box-shadow .3s}.project-card:hover,.video-card:hover{transform:translateY(-6px);box-shadow:0 16px 32px rgba(214,16,106,.24)}
.project-card img{width:100%;aspect-ratio:16/10;object-fit:cover;background:var(--alt);border-radius:var(--r) var(--r) 0 0;transition:transform .5s}.project-card:hover img{transform:scale(1.06)}
.project-card h3,.project-card p,.video-card h3{margin-left:var(--s2);margin-right:var(--s2)}.project-card h3,.video-card h3{margin-top:var(--s2)}
.video-play{display:block;position:relative;width:100%;aspect-ratio:16/9;padding:0;border:0;background:var(--ln);border-radius:var(--r) var(--r) 0 0;cursor:pointer;overflow:hidden}.video-play img{width:100%;height:100%;object-fit:cover}.video-play iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.video-play span{position:absolute;left:var(--s2);bottom:var(--s2);background:var(--pk);color:#fff;padding:var(--s1) var(--s2);font-weight:600;border-radius:var(--r);animation:ring 2.4s infinite}.video-play:hover span{background:var(--pu)}
.logo-row{overflow:hidden;margin-top:var(--s3)}.logo-track{display:flex;width:max-content;animation:slide 40s linear infinite}.logo-row.reverse .logo-track{animation-direction:reverse}.logo-row:hover .logo-track{animation-play-state:paused}
.logo-set{display:flex;gap:var(--s3);list-style:none;margin:0;padding:0 var(--s3) 0 0}.logo-set li{flex:none;width:180px;background:rgba(255,255,255,.85);border:1px solid rgba(106,27,154,.18);border-radius:var(--r);padding:var(--s2);transition:transform .3s,box-shadow .3s,border-color .3s}.logo-set li:hover{transform:translateY(-4px);box-shadow:var(--sh);border-color:var(--pk)}.logo-set img{width:100%;aspect-ratio:2/1;object-fit:contain}
.review-wrap{display:grid;gap:var(--s6);grid-template-columns:1fr;align-items:center}@media(min-width:820px){.review-wrap{grid-template-columns:1fr 1.6fr}}
.rating-big{font-size:6rem;line-height:1;font-weight:700;color:var(--lp);margin:var(--s2) 0}.stars{display:flex;gap:4px;color:#FF1F7A}.stars .icon{width:20px;height:20px}
.review-stage{position:relative;background:rgba(255,255,255,.85);border:1px solid rgba(106,27,154,.2);border-radius:var(--r);padding:var(--s6) var(--s4) var(--s4);box-shadow:var(--sh)}
.review-stage::before{content:"\u201c";position:absolute;top:0;left:var(--s3);font-size:8rem;line-height:1;color:var(--lp);opacity:.4}
.review-slide{margin:0}.review-slide+.review-slide{margin-top:var(--s4)}.review-text{position:relative;font-size:1.375rem;line-height:1.45;color:var(--fg);max-width:none;margin:var(--s2) 0 var(--s3)}
.review-slide figcaption{display:flex;align-items:center;gap:var(--s2)}.avatar{flex:none;display:grid;place-items:center;width:48px;height:48px;border-radius:50%;background:var(--pu);color:#fff;font-weight:700}
.js .review-slide{display:none}.js .review-slide.on{display:block;animation:rise .5s both}.js .review-slide+.review-slide{margin-top:0}
.review-nav{display:none;gap:var(--s1);flex-wrap:wrap;margin-top:var(--s3)}.js .review-nav{display:flex}
.review-dot{width:48px;height:48px;border-radius:50%;border:2px solid transparent;background:rgba(106,27,154,.12);color:var(--pu);font:inherit;font-weight:700;cursor:pointer;transition:background-color .3s,color .3s,transform .3s}.review-dot:hover{transform:translateY(-3px);background:rgba(214,16,106,.15)}.review-dot[aria-selected=true]{background:var(--pk);color:#fff}
.review-progress{display:none;height:4px;background:var(--ln);margin-top:var(--s3);border-radius:2px;overflow:hidden}.js .review-progress{display:block}.review-progress i{display:block;height:100%;background:var(--pk);transform:scaleX(0);transform-origin:0 50%}.review-progress.run i{animation:fill 7s linear forwards}
details{background:rgba(255,255,255,.7);border:1px solid rgba(106,27,154,.16);border-radius:var(--r);padding:var(--s2) var(--s3);margin-bottom:var(--s1)}details[open]{background:rgba(214,16,106,.06);border-color:rgba(214,16,106,.35)}
summary{font-weight:600;cursor:pointer;color:var(--pu);list-style:none;transition:color .3s}summary::-webkit-details-marker{display:none}summary:hover{color:var(--pk)}summary::after{content:"+";float:right;font-size:1.5rem;line-height:1;transition:transform .25s}details[open] summary::after{transform:rotate(45deg)}details p{margin:var(--s1) 0 0}details[open] p{animation:open .3s}
.post-list{list-style:none;padding:0;margin:var(--s3) 0 0}.post-list li{border-top:1px solid var(--ln);padding:var(--s2) 0;transition:padding-left .3s,border-color .3s}.post-list li:hover{padding-left:var(--s1);border-color:var(--pk)}.post-list h2,.post-list h3{margin:0 0 var(--s1);font-size:1.125rem}.post-list p{margin:0}
.cta-band{position:relative;overflow:hidden;background:#6A1B9A!important;color:#fff;padding:var(--s8) 0}.cta-band h2{color:#fff;font-size:2rem}.cta-band .button.plain{background:transparent;color:#fff;border-color:#fff}.cta-band .button.plain:hover{background:#fff;color:#6A1B9A}
.cta-band::after{content:"";position:absolute;right:-80px;top:-100px;width:340px;height:340px;border-radius:50%;background:rgba(255,31,122,.38);pointer-events:none}.cta-band .wrap::after{content:"";position:absolute;left:-120px;bottom:-140px;width:260px;height:260px;border-radius:50%;background:rgba(255,255,255,.1);pointer-events:none;z-index:-1}
.contact .wrap{display:grid;gap:var(--s6);grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}form{display:grid;gap:var(--s2);max-width:480px}label{display:grid;gap:4px;font-weight:600}
input,textarea{font:inherit;padding:12px;border:2px solid rgba(106,27,154,.45);border-radius:var(--r);background:rgba(255,255,255,.9);color:var(--fg);transition:border-color .2s,box-shadow .2s}input:focus,textarea:focus{border-color:var(--pu);box-shadow:var(--sh)}
.contact-list p{display:flex;gap:var(--s2);align-items:flex-start}.contact-list .icon{color:var(--pu);margin-top:4px}
.site-footer{position:relative;overflow:hidden;background:#1E1226;color:#F3EDF7;border-top:8px solid var(--lp);padding:var(--s8) 0 var(--s12)}.site-footer::before{content:"";position:absolute;right:0;bottom:0;width:320px;height:200px;background:DOTS_K;pointer-events:none}.site-footer::after{content:"";position:absolute;left:-100px;top:-100px;width:280px;height:280px;border-radius:50%;background:rgba(106,27,154,.45);pointer-events:none}
.site-footer .wrap{position:relative;z-index:1}.site-footer a{color:#fff;text-decoration:none}.site-footer a:hover{color:#FF1F7A;text-decoration:underline}.site-footer h2{font-size:1.125rem;color:#fff}.site-footer ul{display:block;padding:0;margin:0;list-style:none}.site-footer li{margin-bottom:var(--s1)}
.footer-cols{display:grid;gap:var(--s6);grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}.footer-logo{display:inline-block;background:#FAFAFA;padding:var(--s2);border-radius:var(--r);margin-bottom:var(--s2)}.footer-logo img{width:184px;height:auto}.site-footer .footer-logo:hover{text-decoration:none}
.footer-bottom{border-top:1px solid rgba(221,208,230,.25);margin-top:var(--s6);padding-top:var(--s3)}.site-footer .muted{color:#DDD0E6;margin:0}
.whatsapp{position:fixed;right:var(--s2);bottom:var(--s2);background:var(--pk);color:#fff;padding:12px var(--s2);border-radius:var(--r);font-weight:700;text-decoration:none;z-index:6;box-shadow:var(--sh);animation:ring 2.4s infinite}.whatsapp:hover{background:var(--pu);color:#fff}
.to-top{position:fixed;left:var(--s2);bottom:var(--s2);background:#6A1B9A;color:#fff;padding:12px var(--s2);border-radius:var(--r);font-weight:700;text-decoration:none;box-shadow:var(--sh);opacity:0;pointer-events:none;transform:translateY(16px);transition:opacity .3s,transform .3s,background-color .2s;z-index:6}.to-top.show{opacity:1;pointer-events:auto;transform:none}.to-top:hover{background:var(--pk);color:#fff}
.crumbs{font-size:.875rem;color:var(--mu);padding-top:var(--s3)}.post{padding:var(--s4) 0 var(--s8)}.post h2{margin-top:var(--s4)}
.js .reveal{opacity:0;transform:translateY(24px);transition:opacity .6s,transform .6s}.js .reveal.in{opacity:1;transform:none}
.cursor-ring{position:fixed;left:0;top:0;width:36px;height:36px;pointer-events:none;z-index:100;opacity:0;transition:opacity .3s}.cursor-ring.on{opacity:1}
.cursor-shape{position:absolute;inset:0;border:2px solid #D6106A;border-radius:50%;transition:transform .3s,background-color .3s}.cursor-ring.hover .cursor-shape{transform:scale(1.7);background:rgba(214,16,106,.14)}
.cursor-label{position:absolute;inset:0;display:grid;place-items:center;font-size:.75rem;font-weight:700;color:#D6106A;opacity:0;transition:opacity .2s}.cursor-ring.has-label .cursor-label{opacity:1}
.cursor-dot{position:fixed;left:0;top:0;width:8px;height:8px;margin:-4px 0 0 -4px;background:#FF1F7A;border-radius:50%;pointer-events:none;z-index:101;opacity:0;transition:opacity .3s}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation:none!important;transition:none!important}.js .reveal{opacity:1;transform:none}.trend{stroke-dashoffset:0}.logo-track{width:auto;flex-wrap:wrap}.logo-set{flex-wrap:wrap}.logo-set[aria-hidden]{display:none}.review-progress{display:none!important}}

.filters{display:flex;flex-wrap:wrap;gap:var(--s1);margin:var(--s3) 0 var(--s1)}.filter{font:inherit;font-weight:600;padding:var(--s1) var(--s2);background:rgba(106,27,154,.08);color:var(--pu);border:2px solid var(--pu);border-radius:var(--r);cursor:pointer;transition:background-color .3s,color .3s,transform .3s}.filter:hover,.filter[aria-pressed=true]{background:var(--pu);color:#fff}.filter:hover{transform:translateY(-2px)}
.work-count{margin-bottom:var(--s3)}
.work-grid{columns:3 260px;column-gap:var(--s3);list-style:none;padding:0;margin:0}
.work-item{break-inside:avoid;margin:0 0 var(--s3);background:rgba(255,255,255,.85);border:1px solid rgba(106,27,154,.16);border-radius:var(--r);box-shadow:var(--sh);overflow:hidden;transition:transform .2s ease-out,box-shadow .3s}.work-item:hover{transform:translateY(-6px);box-shadow:0 16px 32px rgba(214,16,106,.24)}.work-item[hidden]{display:none}
.work-open{display:block;position:relative;overflow:hidden;color:inherit}.work-open img{width:100%;height:auto;transition:transform .5s}.work-item:hover .work-open img{transform:scale(1.05)}.work-item[data-cat=video] .work-open img{aspect-ratio:16/9;object-fit:cover}
.work-over{position:absolute;inset:0;display:grid;place-items:center;background:rgba(106,27,154,.72);color:#fff;font-weight:700;opacity:0;transition:opacity .3s}.work-open:hover .work-over,.work-open:focus-visible .work-over{opacity:1}
.work-play{position:absolute;left:var(--s2);bottom:var(--s2);background:var(--pk);color:#fff;padding:var(--s1) var(--s2);font-weight:600;border-radius:var(--r);animation:ring 2.4s infinite}
.work-cap{padding:var(--s2)}.work-cap h3{margin:0 0 4px}.work-cap p{margin:0;font-size:.875rem;color:var(--mu)}.work-tag{display:inline-block;font-size:.75rem;font-weight:700;color:var(--pk);margin-bottom:4px}
.browser-bar{display:flex;align-items:center;gap:6px;padding:var(--s1) var(--s2);background:var(--alt);border-bottom:1px solid var(--ln)}.browser-bar i{width:10px;height:10px;border-radius:50%;background:var(--pk)}.browser-bar i:nth-child(2){background:var(--lp)}.browser-bar i:nth-child(3){background:var(--pu)}.browser-bar span{margin-left:var(--s1);font-size:.75rem;color:var(--mu);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#lightbox{border:0;padding:0;background:transparent;color:var(--fg);width:min(92vw,1000px);max-width:none}#lightbox::backdrop{background:rgba(30,18,38,.82)}
.lb-box{background:var(--bg);border-radius:var(--r);padding:var(--s2);box-shadow:var(--sh)}.lb-body img{width:100%;max-height:70vh;object-fit:contain;background:var(--alt);border-radius:var(--r)}.lb-body iframe{width:100%;aspect-ratio:16/9;border:0;border-radius:var(--r)}
.lb-bar{display:flex;gap:var(--s1);justify-content:space-between;align-items:center;margin-top:var(--s2);flex-wrap:wrap}.lb-bar .button{padding:var(--s1) var(--s2)}.lb-cap{margin:var(--s2) 0 0;max-width:none}

.nav-toggle{display:none;margin-left:auto;width:44px;height:44px;flex-direction:column;justify-content:center;align-items:center;gap:5px;padding:0;background:transparent;border:2px solid var(--pu);border-radius:var(--r);cursor:pointer}
.nav-toggle span{width:20px;height:2px;background:var(--pu);transition:transform .25s,opacity .2s}
.nav-toggle[aria-expanded=true] span:nth-child(1){transform:translateY(7px) rotate(45deg)}.nav-toggle[aria-expanded=true] span:nth-child(2){opacity:0}.nav-toggle[aria-expanded=true] span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
.site-footer::before,.site-footer::after{z-index:0}.site-footer .wrap{z-index:2}.footer-logo{position:relative;z-index:3}
@media(max-width:760px){
.js .nav-toggle{display:flex}
.js .site-nav{position:absolute;top:100%;left:0;right:0;margin:0;flex-direction:column;gap:0;overflow:visible;background:var(--bg);border-bottom:1px solid var(--ln);box-shadow:var(--sh);padding:var(--s1) var(--s3) var(--s2);opacity:0;transform:translateY(-8px);visibility:hidden;transition:opacity .25s,transform .25s,visibility .25s}
.js .site-nav.open{opacity:1;transform:none;visibility:visible}
.js .site-nav a{padding:var(--s2) 0;border-bottom:1px solid var(--ln)}.js .site-nav a:last-child{border-bottom-color:transparent}
.site-footer::after{width:160px;height:160px;left:-80px;top:-80px}
.founder{margin:0 auto;padding:0 var(--s3)}.founder figcaption{text-align:center}
}
"""
CSS=CSS.replace("DOTS_P",dots("#6A1B9A",".4")).replace("LINES_P",lines("#6A1B9A",".3")).replace("DOTS_K",dots("#FF1F7A",".45"))
CSS=re.sub(r"\s*([{};:,>])\s*",r"\1",CSS.replace("\n","")).replace(";}","}")

NAV=[("Services","services"),("Work","work"),("Clients","clients"),("Blog","blog"),("Contact","contact")]
def ld(o): return '<script type="application/ld+json">'+json.dumps(o,separators=(",",":"))+'</script>'
def fmt(d): return datetime.date.fromisoformat(d).strftime("%d %B %Y")
def head(title,desc,path,og="website",extra=""):
    u=SITE+path
    return f'''<!doctype html><html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{u}">
<meta name="color-scheme" content="light"><meta name="theme-color" content="#6A1B9A">
<meta property="og:type" content="{og}"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{u}"><meta property="og:image" content="{SITE}/img/og.webp">
<meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/img/favicon.png" type="image/png">
<style>{CSS}</style><script>document.documentElement.className='js'</script>{extra}</head><body><div class="progress" id="progress"></div><a class="skip" href="#main">Skip to content</a>'''
def hdr(home):
    p="" if home else "/"
    return f'<header class="site-header"><div class="wrap"><a class="logo" href="/"><img src="/img/logo.webp" width="123" height="40" alt="{NAME}"></a><button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu"><span></span><span></span><span></span></button><nav class="site-nav" id="site-nav" aria-label="Main">'+"".join(f'<a href="{p}#{i}">{n}</a>' for n,i in NAV)+'</nav></div></header>'
def foot():
    ex=''.join(f'<li><a href="/#{i}">{n}</a></li>' for n,i in NAV)
    so=''.join(f'<li><a href="{u}" rel="noopener">{n}</a></li>' for n,u in SOC)
    return f'<footer class="site-footer"><div class="wrap"><div class="footer-cols"><div><a class="footer-logo" href="/"><img src="/img/logo.webp" width="184" height="60" alt="{NAME}"></a><p>{TAG}</p></div><div><h2>Explore</h2><ul>{ex}</ul></div><div><h2>Contact</h2><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:+917048805418">{PHONE}</a></li><li>Gopipura, Surat, Gujarat</li><li>Also Mumbai and Kolkata</li></ul></div><div><h2>Follow us</h2><ul>{so}</ul></div></div><div class="footer-bottom"><p class="muted">&copy; {datetime.date.today().year} {NAME}</p></div></div></footer><a class="to-top" href="#main">Top</a><a class="whatsapp" href="https://wa.me/{WA}">WhatsApp us</a>'

GRAPHIC='<svg class="hero-graphic" viewBox="0 0 400 320" role="img" aria-label="Bar chart going up, with marketing, social, search and heart icons"><rect class="gp" x="4" y="4" width="392" height="312" rx="4"/><line x1="32" y1="280" x2="368" y2="280" stroke="#DDD0E6" stroke-width="2"/><g class="bars"><rect x="48" y="220" width="40" height="60"/><rect x="108" y="190" width="40" height="90"/><rect x="168" y="160" width="40" height="120"/><rect x="228" y="130" width="40" height="150"/><rect class="hot" x="288" y="90" width="40" height="190"/></g><polyline class="trend" points="68,200 128,170 188,140 248,110 308,70"/><circle class="dot" cx="308" cy="70" r="8"/><g class="chip-g"><rect class="chip" x="24" y="24" width="48" height="48" rx="4"/><use class="chip-i" href="#i-marketing" x="36" y="36" width="24" height="24"/></g><g class="chip-g c2"><rect class="chip" x="340" y="24" width="48" height="48" rx="4"/><use class="chip-i" href="#i-social" x="352" y="36" width="24" height="24"/></g><g class="chip-g c3"><rect class="chip" x="340" y="120" width="48" height="48" rx="4"/><use class="chip-i" href="#i-search" x="352" y="132" width="24" height="24"/></g><g class="chip-g c4"><rect class="chip" x="24" y="120" width="48" height="48" rx="4"/><use class="chip-i" href="#i-heart" x="36" y="132" width="24" height="24"/></g></svg>'
DECO='<svg class="deco-hero" viewBox="0 0 600 600" aria-hidden="true"><g fill="none" stroke="#FF1F7A" stroke-opacity=".3" stroke-width="2"><circle cx="300" cy="300" r="120"/><circle cx="300" cy="300" r="200"/><circle cx="300" cy="300" r="280"/></g><path class="flow" d="M0 520C120 440 200 560 320 480S520 400 600 300" fill="none" stroke="#DDD0E6" stroke-width="3" stroke-dasharray="4 12" stroke-linecap="round"/><g fill="#FF1F7A"><circle cx="420" cy="120" r="6"/><circle cx="140" cy="200" r="4"/><circle cx="520" cy="420" r="5"/></g><g stroke="#fff" stroke-opacity=".5" stroke-width="2" stroke-linecap="round"><path d="M80 80h16M88 72v16"/><path d="M500 220h16M508 212v16"/><path d="M360 540h16M368 532v16"/></g></svg>'

SIZE={"design":(640,800),"social":(640,640),"video":(480,270),"reel":(405,720),"bts":(640,480),"web":(640,400),"print":(640,800)}
def work_item(it):
    t=it["type"]; label=dict(CATS).get(t,t); w_,h_=it.get("w") or SIZE[t][0],it.get("h") or SIZE[t][1]
    ti=E(it["title"]); ln=E(it.get("line",""))
    meta=f'data-title="{ti}" data-line="{ln}"'
    if t=="video":
        v=it["id"]; im=f'<img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" width="480" height="270" loading="lazy" alt="">'
        trig=f'<a class="work-open" href="https://www.youtube.com/watch?v={v}" data-kind="video" data-id="{v}" data-cursor="Play" {meta} aria-label="Play video: {ti}">{im}<span class="work-play">Play</span></a>'
    elif t=="reel":
        if it.get("id"):
            # YouTube Short / Reel — embeds in the lightbox
            v=it["id"]; im=f'<img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" width="405" height="720" loading="lazy" alt="{ti}" style="aspect-ratio:9/16;object-fit:cover;width:100%">'
            trig=f'<a class="work-open" href="https://www.youtube.com/shorts/{v}" data-kind="video" data-id="{v}" data-cursor="Play" {meta} aria-label="Play reel: {ti}">{im}<span class="work-play">Play</span></a>'
        else:
            # Instagram / external link — opens in new tab
            ph=it.get("img","img/ph-video.webp")
            im=f'<img src="/{ph}" width="405" height="720" loading="lazy" alt="{ti}" style="aspect-ratio:9/16;object-fit:cover;width:100%">'
            trig=f'<a class="work-open" href="{E(it.get("url","#"))}" target="_blank" rel="noopener" data-kind="url" data-cursor="Watch" aria-label="Watch reel: {ti}">{im}<span class="work-play">Watch</span></a>'
    else:
        im=f'<img src="/{it["img"]}" width="{w_}" height="{h_}" loading="lazy" alt="{ti}">'
        if t=="web" and it.get("url"):
            trig=f'<a class="work-open" href="{E(it["url"])}" target="_blank" rel="noopener" data-kind="url" data-cursor="Visit" aria-label="Visit website: {ti}">{im}<span class="work-over">Visit</span></a>'
            trig=f'<div class="browser"><div class="browser-bar"><i></i><i></i><i></i><span>{E(it["url"])}</span></div>{trig}</div>'
        else:
            trig=f'<a class="work-open" href="/{it["img"]}" data-kind="img" data-src="/{it["img"]}" data-cursor="View" {meta} aria-label="View larger: {ti}">{im}<span class="work-over">View</span></a>'
            if t=="web": trig=f'<div class="browser"><div class="browser-bar"><i></i><i></i><i></i><span>{E(it.get("url") or "client website")}</span></div>{trig}</div>'
    visit=f'<p><a class="button plain" href="{E(it["url"])}" target="_blank" rel="noopener" style="margin-top:8px;display:inline-block">View full website &#8594;</a></p>' if t=="web" and it.get("url") else ""
    return f'<li class="work-item" data-cat="{t}">{trig}<div class="work-cap"><span class="work-tag">{E(label)}</span><h3>{ti}</h3><p>{ln}</p>{visit}</div></li>'
def initials(n): return "".join(w[0] for w in n.split()[:2]).upper() or "G"
def logo_set(items,hid=False): return '<ul class="logo-set"'+(' aria-hidden="true"' if hid else '')+'>'+''.join(f'<li><img src="/{im}" width="240" height="120" alt="{"" if hid else E(nm)+" logo"}"></li>' for nm,im in items)+'</ul>'
def logo_row(items,cls=""): return f'<div class="logo-row {cls}"><div class="logo-track">{logo_set(items)}{logo_set(items,True)}</div></div>'

def home():
    biz={"@type":["LocalBusiness","Organization"],"@id":SITE+"/#org","name":NAME,"url":SITE+"/","slogan":TAG,"email":EMAIL,"telephone":PHONE,"image":SITE+"/img/og.webp","logo":SITE+"/img/logo.webp","founder":{"@type":"Person","name":"Priyanka Pal","image":SITE+"/img/founder.webp"},
     "address":{"@type":"PostalAddress","streetAddress":"Gopipura","addressLocality":"Surat","addressRegion":"Gujarat","addressCountry":"IN"},
     "areaServed":["Surat","Mumbai","Kolkata"],"sameAs":[u for _,u in SOC],"aggregateRating":{"@type":"AggregateRating","ratingValue":RATING,"reviewCount":COUNT}}
    s=head("Digital Marketing Agency in Surat | Aasteria Multimedia","Aasteria Multimedia is a digital marketing agency in Gopipura, Surat. Websites, branding, social media, print and video from one team.","/",extra=ld({"@context":"https://schema.org","@graph":[biz]}))
    stars=ic("star2")*5
    s+=sprite()+hdr(True)+'<main id="main">'
    s+=f'<section class="hero">{DECO}<div class="wrap"><div><h1>Digital marketing agency in Surat</h1><p>Aasteria Multimedia works from Gopipura, Surat, with clients in Mumbai and Kolkata too. Websites, branding, social media, print and video all come from one team, so you only explain your business once.</p><div class="button-row"><a class="button" href="#contact">Talk to us</a><a class="button plain" href="#work">See our work</a></div></div><div>{GRAPHIC}</div></div></section>'
    s+='<div class="stats"><div class="wrap"><div class="stats-grid">'+''.join(f'<div>{ic(k,"stat-icon")}<p class="stat-number" data-count="{n}">{n}</p><p class="muted">{l}</p></div>' for k,n,l in [("star2",RATING,"Google rating"),("heart",COUNT,"Google reviews"),("pin","3","Cities: Surat, Mumbai and Kolkata"),("work","6","Services under one roof")])+'</div></div></div>'
    s+='<div class="marquee" aria-hidden="true"><div class="marquee-track">'+('<span>'+''.join(f'<b>{ic(SERV_IC[i])}{E(a)}</b>' for i,(a,_) in enumerate(SERV))+'</span>')*2+'</div></div>'
    cards=''.join(f'<li class="service-card">{ic(SERV_IC[i],"big-icon")}<h3>{E(a)}</h3><p>{E(b)}</p><a class="more" href="{WAL("Hi, I want to ask about "+a+".")}">Ask on WhatsApp</a></li>' for i,(a,b) in enumerate(SERV))
    s+=f'<section class="services" id="services"><div class="wrap">{H("marketing","What we do")}<ul class="service-grid">{cards}</ul></div></section>'
    checks=''.join(f'<li>{ic("check")}<span>{E(t)}</span></li>' for t in ["One team for web, branding, social media, print and video","Clients in Surat, Mumbai and Kolkata","Founded by Ms. Priyanka Pal, digital marketer and content developer","Answers on WhatsApp and phone: +91 70488 05418"])
    s+=f'<section class="about" id="about"><div class="wrap"><div>{H("about","About Aasteria")}<p><b>Mission:</b> help local businesses get found online and get calls, without hiring six different vendors.</p><p><b>Vision:</b> to be the first agency a business in Gujarat thinks of for media work.</p><ul class="checks">{checks}</ul></div><figure class="founder"><img src="/img/founder.webp" width="320" height="320" loading="lazy" alt="Ms. Priyanka Pal, founder of Aasteria Multimedia"><figcaption><b>Ms. Priyanka Pal</b><br><span class="muted">Founder, digital marketer and content developer</span></figcaption></figure></div></section>'
    gb=''.join(f'<button class="goal" data-i="{i}" aria-pressed="false">{E(g)}</button>' for i,(g,_,_) in enumerate(GOALS))
    gr=''.join(f'<div class="goal-result" id="gr-{i}"><p>{E(t)}</p><ul class="goal-services">'+''.join(f'<li>{ic(SERV_IC[k])}{E(SERV[k][0])}</li>' for k in ks)+f'</ul><a class="button" href="{WAL("Hi, I want to "+g.lower()+".")}">Message us about this</a></div>' for i,(g,ks,t) in enumerate(GOALS))
    s+=f'<section class="start" id="start"><div class="wrap">{H("target","Not sure where to start?")}<p class="muted">Pick what you want most. We will show where we would begin.</p><div class="goal-buttons">{gb}</div>{gr}</div></section>'
    steps=[("Talk","You tell us about the business and what you want to change."),("Plan","We agree what we will make, when, and the price."),("Make","We design, build, shoot or print, and show you drafts."),("Launch","We publish the work and check the results with you.")]
    s+='<section class="process" id="process"><div class="wrap">'+H("target","How a project runs")+'<ol class="process-list">'+''.join(f'<li><div class="step-top"><p class="step-num" data-count="{i+1}">{i+1}</p>{ic(["phone","target","brand","marketing"][i])}</div><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i,(t,d) in enumerate(steps))+'</ol></div></section>'
    present=[(k,n) for k,n in CATS if any(x["type"]==k for x in WORK)]
    filt='<button class="filter" data-f="all" aria-pressed="true">All work</button>'+''.join(f'<button class="filter" data-f="{k}" aria-pressed="false">{E(n)}</button>' for k,n in present)
    s+=f'<section class="work" id="work"><div class="wrap">{H("work","Recent Work")}<p class="muted">Graphic design, edited reels, videos, behind the scenes and websites — a snapshot of our latest projects.</p><div class="filters" role="group" aria-label="Filter our work">{filt}</div><p class="muted work-count" aria-live="polite"></p><ul class="work-grid">'+"".join(work_item(x) for x in WORK)+'</ul></div></section><dialog id="lightbox" aria-label="Work preview"><div class="lb-box"><div class="lb-body"></div><p class="lb-cap"></p><div class="lb-bar"><div class="button-row" style="margin:0"><button class="button plain" data-lb="-1">Previous</button><button class="button plain" data-lb="1">Next</button></div><button class="button" data-lb="close">Close</button></div></div></dialog>'
    lg=[(c["name"],c["img"]) for c in CLIENTS]; half=len(lg)//2; rowb=lg[half:]+lg[:half]
    s+=f'<section class="clients" id="clients"><div class="wrap">{H("clients","Clients we have worked with")}<p class="muted">Hover to pause the scroll.</p></div>{logo_row(lg)}{logo_row(rowb,"reverse") if len(lg)>=6 else ""}</section>'
    slides=''.join(f'<figure class="review-slide{" on" if i==0 else ""}" id="rv-{i}"><div class="stars">{ic("star2")*int(round(float(r.get("rating",5))))}</div><p class="review-text">{E(r["text"])}</p><figcaption><span class="avatar">{E(initials(r["who"]))}</span><span><b>{E(r["who"])}</b><br><span class="muted">{(E(r["when"])+", ") if r.get("when") else ""}Google review</span></span></figcaption></figure>' for i,r in enumerate(REVIEWS))
    dots_=''.join(f'<button class="review-dot" data-i="{i}" aria-selected="{"true" if i==0 else "false"}" aria-label="Show review from {E(r["who"])}">{E(initials(r["who"]))}</button>' for i,r in enumerate(REVIEWS))
    s+=f'<section class="reviews" id="reviews"><div class="wrap review-wrap"><div class="review-summary">{H("star2","What clients say")}<p class="rating-big" data-count="{RATING}">{RATING}</p><div class="stars">{stars}</div><p class="muted">Rated {RATING} from {COUNT} Google reviews</p><div class="button-row"><a class="button plain" href="{MAPS}" rel="noopener">Read all on Google</a><a class="button" href="{WRITE}" rel="noopener">Write a review</a></div></div><div class="review-stage"><div class="review-slides">{slides}</div><div class="review-nav" aria-label="Choose a review">{dots_}</div><div class="review-progress run"><i></i></div></div></div></section>'
    s+=f'<section class="faq" id="faq"><div class="wrap">{H("faq","Common questions")}'+"".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q,a in FAQ)+'</div></section>'
    s+=f'<section class="blog-preview" id="blog"><div class="wrap">{H("blog","From the blog")}<ul class="post-list">'+"".join(f'<li><h3><a href="/blog/{p["slug"]}/">{E(p["title"])}</a></h3><p class="muted">{E(p["desc"])}</p></li>' for p in POSTS[:3])+'</ul><p><a href="/blog/">All posts</a></p></div></section>'
    s+=f'<section class="cta-band"><div class="wrap"><h2>Have a project in mind?</h2><p>Send us a message on WhatsApp or call {PHONE}.</p><div class="button-row"><a class="button" href="{WAL("Hi, I would like to talk about a project.")}">WhatsApp us</a><a class="button plain" href="tel:+917048805418">Call us</a></div></div></section>'
    s+=f'''<section class="contact" id="contact"><div class="wrap"><div>{H("mail","Talk to us")}<form action="https://api.web3forms.com/submit" method="post"><input type="hidden" name="access_key" value="YOUR_WEB3FORMS_KEY"><input type="hidden" name="subject" value="New enquiry from aasteria.com"><label>Name<input name="name" required autocomplete="name"></label><label>Email<input type="email" name="email" required autocomplete="email"></label><label>Message<textarea name="message" rows="5" required></textarea></label><button class="button" type="submit">Send message</button></form></div><div class="contact-list"><p>{ic("mail")}<span><b>Email</b><br><a href="mailto:{EMAIL}">{EMAIL}</a></span></p><p>{ic("phone")}<span><b>Phone and WhatsApp</b><br><a href="tel:+917048805418">{PHONE}</a></span></p><p>{ic("pin")}<span><b>Address</b><br>Gopipura, Surat, Gujarat, India<br><span class="muted">We also work in Mumbai and Kolkata.</span></span></p></div></div></section></main>'''
    return s+foot()+JS+"</body></html>"

NAVJS="""<script>(function(){var nt=document.querySelector('.nav-toggle'),nv=document.querySelector('.site-nav');function c(){nv.classList.remove('open');nt.setAttribute('aria-expanded','false')}nt.addEventListener('click',function(){nt.setAttribute('aria-expanded',nv.classList.toggle('open'))});nv.addEventListener('click',function(e){if(e.target.closest('a'))c()});document.addEventListener('click',function(e){if(!e.target.closest('.site-header'))c()});addEventListener('keydown',function(e){if(e.key==='Escape')c()});addEventListener('resize',function(){if(innerWidth>760)c()})})();</script>"""
def crumbs(items): return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+u} for i,(n,u) in enumerate(items)]}
def blog_index():
    s=head("Blog | Aasteria Multimedia","Notes on digital marketing, lead generation and content from Aasteria Multimedia in Surat.","/blog/")
    s+=hdr(False)+'<main id="main" class="wrap post"><p class="crumbs"><a href="/">Home</a> / Blog</p><h1>Blog</h1><ul class="post-list">'
    s+="".join(f'<li><h2><a href="/blog/{p["slug"]}/">{E(p["title"])}</a></h2><p class="muted">{fmt(p["date"])}</p><p>{E(p["desc"])}</p></li>' for p in POSTS)
    return s+"</ul></main>"+foot()+NAVJS+"</body></html>"
def post_page(p):  # reusable post template
    path=f'/blog/{p["slug"]}/'
    art={"@context":"https://schema.org","@type":"Article","headline":p["title"],"description":p["desc"],"datePublished":p["date"],"mainEntityOfPage":SITE+path,"image":SITE+"/img/og.webp","author":{"@type":"Person","name":"Priyanka Pal"},"publisher":{"@type":"Organization","name":NAME}}
    bc=dict(crumbs([("Home","/"),("Blog","/blog/"),(p["title"],path)]),**{"@context":"https://schema.org"})
    s=head(p["title"]+" | "+NAME,p["desc"],path,"article",ld(art)+ld(bc))
    s+=hdr(False)+f'<main id="main" class="wrap post"><p class="crumbs"><a href="/">Home</a> / <a href="/blog/">Blog</a> / {E(p["title"])}</p><article><h1>{E(p["title"])}</h1><p class="muted">{fmt(p["date"])}, by Priyanka Pal</p>{p["body"]}</article><p><a class="button" href="/#contact">Talk to us</a></p><p><a href="/">Back to home</a></p></main>'
    return s+foot()+NAVJS+"</body></html>"

JS="""<script>(function(){var rm=matchMedia('(prefers-reduced-motion:reduce)').matches,io2='IntersectionObserver' in window;
document.addEventListener('click',function(e){var c=e.target.closest('[data-scroll]');if(c){document.getElementById(c.dataset.scroll).scrollBy({left:c.dataset.dir*340,behavior:rm?'auto':'smooth'});return}
var b=e.target.closest('.video-play');if(!b||b.disabled)return;var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.id+'?autoplay=1';f.title=b.dataset.t;f.allow='autoplay;encrypted-media;picture-in-picture';f.allowFullscreen=true;b.replaceChildren(f);b.disabled=true});
var bar=document.getElementById('progress'),hd=document.querySelector('.site-header'),tt=document.querySelector('.to-top');
addEventListener('scroll',function(){var h=document.documentElement;bar.style.transform='scaleX('+(h.scrollTop/(h.scrollHeight-h.clientHeight||1))+')';hd.classList.toggle('scrolled',scrollY>8);tt.classList.toggle('show',scrollY>600)},{passive:true});
document.addEventListener('pointerdown',function(e){var b=e.target.closest('.button');if(!b||rm)return;var r=b.getBoundingClientRect(),p=document.createElement('span');p.className='ripple';p.style.left=(e.clientX-r.left)+'px';p.style.top=(e.clientY-r.top)+'px';b.appendChild(p);setTimeout(function(){p.remove()},650)});
var gb=document.querySelectorAll('.goal');gb.forEach(function(g){g.addEventListener('click',function(){var on=g.getAttribute('aria-pressed')==='true';gb.forEach(function(x){x.setAttribute('aria-pressed','false')});document.querySelectorAll('.goal-result').forEach(function(r){r.classList.remove('on')});if(!on){g.setAttribute('aria-pressed','true');document.getElementById('gr-'+g.dataset.i).classList.add('on')}})});
var rs=document.querySelectorAll('.review-slide'),rd=document.querySelectorAll('.review-dot'),ri=0,rt,rg=document.querySelector('.review-stage');
function rshow(i){ri=(i+rs.length)%rs.length;rs.forEach(function(x,k){x.classList.toggle('on',k===ri)});rd.forEach(function(d,k){d.setAttribute('aria-selected',k===ri)});var pb=document.querySelector('.review-progress');if(pb){pb.classList.remove('run');void pb.offsetWidth;pb.classList.add('run')}}
function rreset(){clearInterval(rt);if(!rm&&rs.length>1)rt=setInterval(function(){rshow(ri+1)},7000)}
rd.forEach(function(d,k){d.addEventListener('click',function(){rshow(k);rreset()})});
if(rg){rg.addEventListener('mouseenter',function(){clearInterval(rt)});rg.addEventListener('mouseleave',function(){rshow(ri);rreset()});rg.addEventListener('focusin',function(){clearInterval(rt)})}
rreset();
var wi=[].slice.call(document.querySelectorAll('.work-item')),fb=document.querySelectorAll('.filter'),wc=document.querySelector('.work-count'),lb=document.getElementById('lightbox'),cur=0;
function vis(){return wi.filter(function(x){return !x.hidden})}
function cnt(){if(wc)wc.textContent='Showing '+vis().length+' of '+wi.length+' items'}cnt();
fb.forEach(function(b){b.addEventListener('click',function(){fb.forEach(function(x){x.setAttribute('aria-pressed',x===b)});wi.forEach(function(it){var show=b.dataset.f==='all'||it.dataset.cat===b.dataset.f;it.hidden=!show;if(show&&!rm){it.style.animation='none';void it.offsetWidth;it.style.animation='rise .4s both'}});cnt()})});
function openLb(i){var v=vis();if(!v.length||!lb||!lb.showModal)return;cur=(i+v.length)%v.length;var a=v[cur].querySelector('.work-open'),b=lb.querySelector('.lb-body');b.textContent='';if(a.dataset.kind==='video'){var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+a.dataset.id+'?autoplay=1';f.title=a.dataset.title;f.allow='autoplay;encrypted-media;picture-in-picture';f.allowFullscreen=true;b.appendChild(f)}else{var im=document.createElement('img');im.src=a.dataset.src;im.alt=a.dataset.title;b.appendChild(im)}lb.querySelector('.lb-cap').textContent=a.dataset.title+(a.dataset.line?': '+a.dataset.line:'');if(!lb.open)lb.showModal()}
document.addEventListener('click',function(e){var o=e.target.closest('.work-open');if(o&&lb&&lb.showModal){if(o.dataset.kind==='url')return;e.preventDefault();openLb(vis().indexOf(o.closest('.work-item')));return}var l=e.target.closest('[data-lb]');if(l){l.dataset.lb==='close'?lb.close():openLb(cur+Number(l.dataset.lb));return}if(e.target===lb)lb.close()});
if(lb)lb.addEventListener('close',function(){lb.querySelector('.lb-body').textContent=''});
var nt=document.querySelector('.nav-toggle'),nv=document.querySelector('.site-nav');
function nclose(){nv.classList.remove('open');nt.setAttribute('aria-expanded','false')}
nt.addEventListener('click',function(){var o=nv.classList.toggle('open');nt.setAttribute('aria-expanded',o)});
nv.addEventListener('click',function(e){if(e.target.closest('a'))nclose()});
document.addEventListener('click',function(e){if(!e.target.closest('.site-header'))nclose()});
addEventListener('keydown',function(e){if(e.key==='Escape')nclose()});
addEventListener('resize',function(){if(innerWidth>760)nclose()});
var links=[].slice.call(document.querySelectorAll('.site-nav a'));
if(io2){var so=new IntersectionObserver(function(l){l.forEach(function(x){if(x.isIntersecting)links.forEach(function(a){a.classList.toggle('active',a.hash==='#'+x.target.id)})})},{rootMargin:'-45% 0px -50% 0px'});document.querySelectorAll('main section[id]').forEach(function(q){so.observe(q)})}
document.querySelectorAll('.h-scroll').forEach(function(r){var d=0,sx=0,sl=0,mv=0;r.addEventListener('dragstart',function(e){e.preventDefault()});r.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse')return;d=1;mv=0;sx=e.clientX;sl=r.scrollLeft});addEventListener('pointermove',function(e){if(!d)return;var dx=e.clientX-sx;if(Math.abs(dx)>5){mv=1;r.style.scrollSnapType='none';r.classList.add('drag')}if(mv)r.scrollLeft=sl-dx});addEventListener('pointerup',function(){if(!d)return;d=0;r.classList.remove('drag');r.style.scrollSnapType=''});r.addEventListener('click',function(e){if(mv){e.stopPropagation();e.preventDefault();mv=0}},true)});
if(!rm&&matchMedia('(pointer:fine)').matches){var ring=document.createElement('div'),dot=document.createElement('div');ring.className='cursor-ring';ring.innerHTML='<span class="cursor-shape"></span><span class="cursor-label"></span>';dot.className='cursor-dot';document.body.append(ring,dot);
var lab=ring.querySelector('.cursor-label'),mx=-100,my=-100,rx=-100,ry=-100,nx=0,ny=0,gr=document.querySelector('.hero-graphic');
addEventListener('pointermove',function(e){if(e.pointerType!=='mouse')return;mx=e.clientX;my=e.clientY;nx=mx/innerWidth-.5;ny=my/innerHeight-.5;ring.classList.add('on');dot.style.opacity=1});
document.documentElement.addEventListener('mouseleave',function(){ring.classList.remove('on');dot.style.opacity=0});
document.addEventListener('pointerover',function(e){if(!e.target.closest)return;ring.classList.toggle('hover',!!e.target.closest('a,button,summary,input,textarea,label,.service-card,.project-card,[data-cursor]'));var c=e.target.closest('[data-cursor]');lab.textContent=c?c.dataset.cursor:'';ring.classList.toggle('has-label',!!c)});
(function loop(){rx+=(mx-rx)*.16;ry+=(my-ry)*.16;ring.style.transform='translate3d('+(rx-18)+'px,'+(ry-18)+'px,0)';dot.style.transform='translate3d('+mx+'px,'+my+'px,0)';if(gr&&scrollY<innerHeight)gr.style.transform='translate('+(-nx*24)+'px,'+(-ny*24)+'px)';requestAnimationFrame(loop)})();
document.querySelectorAll('.button,.goal').forEach(function(b){b.addEventListener('pointermove',function(e){var r=b.getBoundingClientRect();b.style.transform='translate('+((e.clientX-r.left-r.width/2)*.2)+'px,'+((e.clientY-r.top-r.height/2)*.3-3)+'px)'});b.addEventListener('pointerleave',function(){b.style.transform=''})});
document.querySelectorAll('.work-item,.service-card').forEach(function(c){c.addEventListener('pointermove',function(e){var b=c.getBoundingClientRect(),x=(e.clientX-b.left)/b.width-.5,y=(e.clientY-b.top)/b.height-.5;c.style.transform='perspective(800px) rotateY('+x*8+'deg) rotateX('+-y*8+'deg) translateY(-6px)'});c.addEventListener('pointerleave',function(){c.style.transform=''})})}
if(rm||!io2)return;
var io=new IntersectionObserver(function(l){l.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{threshold:.1});
document.querySelectorAll('main section:not(.hero) .wrap>*:not(.review-wrap)').forEach(function(el){el.classList.add('reveal');el.style.transitionDelay=Array.prototype.indexOf.call(el.parentNode.children,el)*80+'ms';io.observe(el)});
document.querySelectorAll('[data-count]').forEach(function(n){var t=parseFloat(n.dataset.count),dp=(n.dataset.count.split('.')[1]||'').length;n.textContent=(0).toFixed(dp);var co=new IntersectionObserver(function(l){if(!l[0].isIntersecting)return;co.disconnect();var st=null;(function f(ts){st=st||ts;var p=Math.min((ts-st)/1500,1);n.textContent=(t*(1-Math.pow(1-p,3))).toFixed(dp);if(p<1)requestAnimationFrame(f)})(0)},{threshold:.5});co.observe(n)});
})();</script>"""

def w(path,txt):
    # Image paths are made relative so the site also works when index.html is opened straight from the folder.
    if path.endswith(".html"):
        P="../"*path.count("/")
        txt=txt.replace('src="/img/','src="'+P+'img/').replace('href="/img/','href="'+P+'img/').replace('data-src="/img/','data-src="'+P+'img/')
    os.makedirs(os.path.dirname(path) or ".",exist_ok=True); open(path,"w",encoding="utf-8").write(txt)
w("index.html",home()); w("blog/index.html",blog_index())
for p in POSTS: w(f'blog/{p["slug"]}/index.html',post_page(p))
today=datetime.date.today().isoformat()
urls=["/","/blog/"]+[f'/blog/{p["slug"]}/' for p in POSTS]
w("sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)+"</urlset>")
w("robots.txt",f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("built",len(urls),"pages")
# Check that every local image used on a page exists in the folder.
bad=set()
for root,_,fs in os.walk("."):
    for f in fs:
        if f.endswith(".html"):
            t=open(os.path.join(root,f),encoding="utf-8").read()
            for m in re.findall(r'(?:src|href)="((?:\.\./)*img/[^"]+)"',t):
                if not os.path.exists(os.path.normpath(os.path.join(root,m))): bad.add(os.path.normpath(os.path.join(root,m)))
for b in sorted(bad): print("MISSING IMAGE:",b)
print("image check done" if not bad else "Fix the missing images above (check spelling, capital letters and file type).")
