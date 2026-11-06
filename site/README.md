# Aasteria Multimedia static site

All content lives in the DATA block at the top of `build.py`. Edit it, then run `python3 build.py`. This rewrites index.html, the blog pages and sitemap.xml, and checks that every image exists (it prints MISSING IMAGE if not).

Before launch
- Replace the placeholder reviews, projects, videos and clients with real ones.
- Put your Web3Forms key in build.py where it says YOUR_WEB3FORMS_KEY (free key from web3forms.com, sent to your email).
- Paste your Google Business link into GOOGLE_BUSINESS_URL in build.py.
- Images live in img/: logo.webp (transparent, about 480 px wide), founder.webp, og.webp (1200x630), favicon.png.
- Check _redirects against the old WordPress sitemap.

Add a client: add one line to CLIENTS, put the logo in img/ (WebP, 240x120), run build. Six or more clients make two scrolling rows.
Add work (graphic design, social posts, edited videos, behind the scenes, websites, print): copy a line in WORK. Pick the type, write the title and line, and put the image in img/ (WebP, around 640 px wide). For a video give the YouTube ID instead of an image. For a website add its url to show a Visit website link. Run build.
Add a blog post: add an entry at the top of POSTS (slug, title, date, desc, body HTML), run build. It appears at /blog/your-slug/ and in the sitemap.
Reviews: paste real Google reviews into REVIEWS (name and text), or use the live Google option below.

Deploy free
- Cloudflare Pages: push the folder to GitHub, Pages > Create project > connect repo, build command `python3 build.py` (or empty if you commit the built files), output directory `/`.
- Netlify: drag the folder onto app.netlify.com/drop, or connect the repo.
Point aasteria.com DNS to the host and keep _redirects in the root.

Google reviews (live from Google, optional)
1. In Google Cloud Console enable "Places API (New)" and create an API key restricted to it.
2. Find your Place ID with Google's Place ID Finder.
3. In Cloudflare Pages or Netlify add environment variables GOOGLE_PLACES_KEY and GOOGLE_PLACE_ID. Never put the key in a file.
4. Set the build command to `python3 build.py`. Each build fetches the latest rating, count and up to 5 reviews.
5. For daily refresh, trigger a deploy hook once a day.
If the key is missing or Google does not answer, the REVIEWS list is used. Check Google's Places API terms on showing review content.
