"""Two-level interest taxonomy: fields -> subfields, with keyword hints for offline classification."""

FIELDS = [
    {
        "id": "politics",
        "name": "Politics & Governance",
        "subfields": [
            ("indian_politics", "Indian politics", "bjp congress lok_sabha rajya_sabha union_minister modi rahul_gandhi chief_minister mla cabinet opposition aap tmc dmk cpi(m) ldf udf amit_shah governor"),
            ("global_politics", "Global politics", "president prime_minister trump putin xi_jinping white_house kremlin regime coalition sanctions macron netanyahu"),
            ("public_policy", "Public policy", "policy scheme bill draft regulation guidelines rules notification ministry reform subsidy welfare"),
            ("elections", "Elections", "election poll polls voter voting ballot evm campaign candidate constituency bypoll electoral"),
            ("protests", "Protests & civic movements", "protest protests protesters demonstration demonstrators rally agitation dharna jantar_mantar unrest hunger_strike"),
            ("diplomacy", "Diplomacy", "diplomat diplomatic summit bilateral treaty embassy foreign_minister external_affairs ceasefire envoy security_council jaishankar"),
            ("rights_law", "Rights & legislation", "supreme_court high_court judgment verdict petition constitution constitutional legislation amendment bail"),
        ],
    },
    {
        "id": "science",
        "name": "Science & Innovation",
        "subfields": [
            ("space", "Space exploration", "isro nasa spacecraft rocket launch orbit satellite moon mars lunar spacex astronaut mission telescope esa gaganyaan"),
            ("ai", "Artificial intelligence", "ai artificial_intelligence machine_learning llm openai chatgpt neural gemini anthropic deepmind chatbot chatbots grok"),
            ("mobility", "Automobiles & mobility", "car cars ev electric_vehicle automobile tesla maruti tata_motors mahindra vehicle railway railways metro aviation airline"),
            ("robotics", "Robotics", "robot robotics humanoid drone automation autonomous"),
            ("energy", "Energy technology", "solar wind_power energy power_grid nuclear hydrogen renewable battery_storage coal electricity"),
            ("medicine", "Medicine & biotechnology", "hospital vaccine disease drug medical patients doctors cancer virus outbreak biotech gene clinical"),
            ("discoveries", "Scientific discoveries", "scientists researchers discovery fossil species physics chemistry astronomers telescope"),
        ],
    },
    {
        "id": "tech",
        "name": "Technology & Internet",
        "subfields": [
            ("open_source", "Open source & Linux", "linux kernel open_source open-source github gnu debian ubuntu fedora rust foss"),
            ("cybersecurity", "Cybersecurity", "hack hacked hacker hackers breach cyber cyberattack vulnerability ransomware malware exploit security_flaw cve phishing data_leak"),
            ("dev_tools", "Developer tools", "developer developers programming compiler api framework python javascript sdk devtools"),
            ("electronics", "Consumer electronics", "iphone smartphone smartphones apple samsung oneplus laptop chip chips processor gadget pixel android"),
            ("internet_culture", "Internet culture", "viral social_media instagram youtube youtuber meme influencer twitter reddit"),
            ("startups", "Startups", "startup startups funding raises series_a unicorn venture_capital founder seed_round valuation"),
        ],
    },
    {
        "id": "business",
        "name": "Business & Economy",
        "subfields": [
            ("indian_economy", "Indian economy", "rbi gdp inflation rupee sensex nifty fiscal budget gst repo_rate indian_economy"),
            ("global_markets", "Global markets", "stocks markets wall_street federal_reserve dow nasdaq bond oil_prices tariff dollar"),
            ("personal_finance", "Personal finance", "savings loan emi mutual_fund insurance credit_card income_tax pension"),
            ("companies", "Companies & startups", "profit revenue quarterly q2 shares ceo merger acquisition ipo"),
            ("employment", "Employment", "jobs layoffs hiring employment unemployment workers wages labour"),
            ("trade", "Trade & industry", "trade exports imports manufacturing tariffs supply_chain"),
        ],
    },
    {
        "id": "world",
        "name": "World & Society",
        "subfields": [
            ("conflict", "Conflict & security", "war military airstrike missile troops army conflict terror militants gaza ukraine israel iran"),
            ("environment", "Environment & climate", "climate pollution flood floods rain cyclone heatwave forest wildlife environment emissions air_quality monsoon"),
            ("education", "Education", "school university students exam education teachers college neet jee ugc"),
            ("kerala", "Kerala", "kerala kochi thiruvananthapuram kozhikode thrissur kannur malappuram sabarimala"),
            ("crime_justice", "Crime & justice", "police arrested murder crime accused investigation custody fir"),
            ("society", "Society & communities", "community caste religion women gender migrants rural urban social"),
        ],
    },
    {
        "id": "culture",
        "name": "Culture & Entertainment",
        "subfields": [
            ("cinema", "Cinema & OTT", "film movie cinema actor actress box_office ott netflix bollywood mollywood"),
            ("music", "Music", "music album singer concert song"),
            ("books_ideas", "Books & ideas", "book author novel literature festival essay"),
            ("sports", "Sports", "cricket football tournament ipl world_cup olympics fifa bcci badminton tennis french_open"),
            ("heritage", "History & heritage", "history heritage archaeology museum ancient monument temple"),
            ("food_travel", "Food & travel", "food travel tourism restaurant cuisine trip"),
        ],
    },
]

SUBFIELDS = {sid: {"id": sid, "name": name, "field": f["id"], "keywords": kw.split()} for f in FIELDS for sid, name, kw in f["subfields"]}


def public_taxonomy():
    return [{"id": f["id"], "name": f["name"], "subfields": [{"id": s, "name": n} for s, n, _ in f["subfields"]]} for f in FIELDS]


STORY_TYPES = {
    "policy": "policy protest bill scheme regulation rules draft notification",
    "protest": "protest protesters demonstration rally strike agitation dharna march",
    "election": "election poll voter voting candidate campaign bypoll",
    "court": "verdict judgment petition bench bail supreme_court high_court",
    "space": "isro nasa rocket launch spacecraft orbit satellite mission moon mars",
    "science": "scientists study researchers discovery found journal species",
    "tech_product": "launches unveils iphone smartphone device release",
    "security": "breach hack vulnerability ransomware malware exploit cve flaw",
    "markets": "shares stocks sensex nifty markets profit quarterly results revenue ipo",
    "economy": "gdp inflation rbi repo_rate economy fiscal budget tariff trade",
    "disaster": "flood cyclone earthquake landslide rain fire accident collapse dead toll",
    "conflict": "war attack strike missile troops military ceasefire killed militants",
    "diplomacy": "summit talks bilateral treaty visit diplomat envoy",
    "crime": "arrested police murder accused crime custody investigation",
    "sports": "match cricket football tournament wins defeats cup",
    "culture": "film movie actor music book festival",
    "health": "hospital vaccine disease outbreak patients health virus",
}
