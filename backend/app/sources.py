"""Source credibility index.

Every outlet we crawl is listed here with a tier, a confidence weight and a rationale.
The weights are editorial (methodology v0) and are published on the /sources page.
"""

TIERS = {
    "primary": {"label": "Primary source", "description": "Official bodies publishing their own documents, data or announcements."},
    "factcheck": {"label": "Fact-checker", "description": "Organisations dedicated to verifying claims, with published methodology."},
    "established": {"label": "Established outlet", "description": "Long-running newsrooms with editorial standards and a track record of corrections."},
    "specialist": {"label": "Specialist outlet", "description": "Domain-focused publications with deep subject expertise."},
    "regional": {"label": "Regional outlet", "description": "Regional-language newsrooms; essential for local coverage."},
    "aggregator": {"label": "Aggregator / community", "description": "Discovery only. Stories found here are low-confidence until corroborated."},
}


def S(id, name, feed, homepage, lang, tier, weight, rationale, extract=True):
    return {"id": id, "name": name, "feed": feed, "homepage": homepage, "lang": lang, "tier": tier,
            "weight": weight, "rationale": rationale, "extract": extract}


SOURCES = [
    # Primary
    S("nasa", "NASA News Releases", "https://www.nasa.gov/news-release/feed/", "https://www.nasa.gov", "en", "primary", 0.95,
      "Official agency announcements; authoritative for its own missions, not for independent assessment."),
    # Fact-checkers
    S("altnews", "Alt News", "https://www.altnews.in/feed/", "https://www.altnews.in", "en", "factcheck", 0.85,
      "Dedicated Indian fact-checking organisation; publishes evidence for each verdict."),
    S("factly", "Factly", "https://factly.in/feed/", "https://factly.in", "en", "factcheck", 0.85,
      "Dedicated Indian fact-checking and public-data organisation."),
    # Established Indian outlets
    S("thehindu_national", "The Hindu - National", "https://www.thehindu.com/news/national/feeder/default.rss", "https://www.thehindu.com", "en", "established", 0.9,
      "National daily with a long editorial history and a readers' editor for corrections."),
    S("thehindu_international", "The Hindu - International", "https://www.thehindu.com/news/international/feeder/default.rss", "https://www.thehindu.com", "en", "established", 0.9,
      "International desk of The Hindu."),
    S("thehindu_business", "The Hindu - Business", "https://www.thehindu.com/business/feeder/default.rss", "https://www.thehindu.com", "en", "established", 0.88,
      "Business desk of The Hindu."),
    S("thehindu_scitech", "The Hindu - Sci-Tech", "https://www.thehindu.com/sci-tech/feeder/default.rss", "https://www.thehindu.com", "en", "established", 0.88,
      "Science and technology desk of The Hindu."),
    S("thehindu_kerala", "The Hindu - Kerala", "https://www.thehindu.com/news/national/kerala/feeder/default.rss", "https://www.thehindu.com", "en", "established", 0.88,
      "Kerala bureau of The Hindu; English coverage of state news."),
    S("indianexpress", "The Indian Express", "https://indianexpress.com/feed/", "https://indianexpress.com", "en", "established", 0.88,
      "National daily known for investigative and explanatory journalism."),
    S("scroll", "Scroll.in", "https://feeds.feedburner.com/ScrollinArticles.rss", "https://scroll.in", "en", "established", 0.8,
      "Digital-native newsroom with long-form reporting; mixes news and opinion (labelled)."),
    S("livemint", "Mint", "https://www.livemint.com/rss/news", "https://www.livemint.com", "en", "established", 0.82,
      "Business and economy daily."),
    S("livemint_tech", "Mint - Technology", "https://www.livemint.com/rss/technology", "https://www.livemint.com", "en", "established", 0.78,
      "Technology desk of Mint; includes consumer and sale coverage."),
    S("economictimes", "The Economic Times", "https://economictimes.indiatimes.com/rssfeedstopstories.cms", "https://economictimes.indiatimes.com", "en", "established", 0.78,
      "Large business newsroom; fast, high-volume coverage."),
    S("toi", "The Times of India", "https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "https://timesofindia.indiatimes.com", "en", "established", 0.72,
      "Highest-reach English daily; broad but high-volume coverage, so weighted lower for depth."),
    S("ndtv", "NDTV", "https://feeds.feedburner.com/ndtvnews-top-stories", "https://www.ndtv.com", "en", "established", 0.74,
      "National broadcaster's news site; fast breaking coverage."),
    # International
    S("bbc_world", "BBC News - World", "https://feeds.bbci.co.uk/news/world/rss.xml", "https://www.bbc.com/news", "en", "established", 0.9,
      "Public broadcaster with published editorial guidelines and a corrections page."),
    S("bbc_tech", "BBC News - Technology", "https://feeds.bbci.co.uk/news/technology/rss.xml", "https://www.bbc.com/news", "en", "established", 0.88,
      "Technology desk of the BBC."),
    S("bbc_science", "BBC News - Science", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml", "https://www.bbc.com/news", "en", "established", 0.88,
      "Science and environment desk of the BBC."),
    S("aljazeera", "Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml", "https://www.aljazeera.com", "en", "established", 0.8,
      "International broadcaster with strong West Asia and Global South coverage."),
    # Specialist tech
    S("lwn", "LWN.net", "https://lwn.net/headlines/rss", "https://lwn.net", "en", "specialist", 0.92,
      "The reference publication for Linux kernel and free-software development."),
    S("arstechnica", "Ars Technica", "https://feeds.arstechnica.com/arstechnica/index", "https://arstechnica.com", "en", "specialist", 0.85,
      "Technically rigorous science and technology journalism."),
    S("theverge", "The Verge", "https://www.theverge.com/rss/index.xml", "https://www.theverge.com", "en", "specialist", 0.75,
      "Consumer technology and internet culture."),
    S("techcrunch", "TechCrunch", "https://techcrunch.com/feed/", "https://techcrunch.com", "en", "specialist", 0.75,
      "Startup and venture funding news."),
    S("hackernews", "Hacker News (front page)", "https://hnrss.org/frontpage", "https://news.ycombinator.com", "en", "aggregator", 0.5,
      "Community-curated links; useful for discovery, not a source of record.", extract=False),
    # Malayalam
    S("mathrubhumi", "Mathrubhumi", "https://www.mathrubhumi.com/rss", "https://www.mathrubhumi.com", "ml", "regional", 0.8,
      "One of Kerala's oldest Malayalam dailies."),
    S("asianet", "Asianet News", "https://www.asianetnews.com/rss", "https://www.asianetnews.com", "ml", "regional", 0.7,
      "Major Malayalam broadcaster's news site; fast, high-volume coverage."),
    S("twentyfour", "Twenty Four News", "https://www.twentyfournews.com/feed", "https://www.twentyfournews.com", "ml", "regional", 0.65,
      "Malayalam news channel."),
    S("oneindia_ml", "Oneindia Malayalam", "https://malayalam.oneindia.com/rss/malayalam-news-fb.xml", "https://malayalam.oneindia.com", "ml", "regional", 0.6,
      "Digital Malayalam news portal; high volume, lighter verification."),
    S("gnews_ml", "Google News (Malayalam)", "https://news.google.com/rss?hl=ml&gl=IN&ceid=IN:ml", "https://news.google.com", "ml", "aggregator", 0.55,
      "Aggregated Malayalam headlines; discovery only.", extract=False),
]

SOURCE_MAP = {s["id"]: s for s in SOURCES}

# Context sources used for rabbit holes (not crawled as news).
CONTEXT_SOURCES = [
    {"id": "wikipedia", "name": "Wikipedia", "homepage": "https://en.wikipedia.org", "tier": "specialist", "weight": 0.7,
     "rationale": "Background and history only. Never used as the sole source for current events; claims link to the article used."},
]


def public_sources():
    return {"tiers": TIERS, "sources": [{k: v for k, v in s.items() if k != "extract"} for s in SOURCES], "context_sources": CONTEXT_SOURCES,
            "methodology": [
                "Weights are editorial judgements (methodology v0) based on tier, track record of corrections, and depth of coverage.",
                "Weights affect ranking and the confidence shown next to citations. They never hide a source you have not excluded.",
                "Aggregators are used for discovery only; their stories are low-confidence until corroborated by another outlet.",
                "Primary sources are authoritative for what an institution said, not for whether it is true.",
                "You can exclude any source in your settings.",
            ]}
