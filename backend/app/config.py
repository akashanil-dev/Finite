import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

APP_NAME = "Finite"
DATA_DIR = Path(os.getenv("FINITE_DATA_DIR", str(ROOT / "data")))
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "finite.db"
LLM_CACHE_DIR = DATA_DIR / "llm_cache"
LLM_CACHE_DIR.mkdir(exist_ok=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
MOCK_MODE = not OPENAI_API_KEY
FAST_MODEL = os.getenv("FINITE_FAST_MODEL", "gpt-6-luna")
SMART_MODEL = os.getenv("FINITE_SMART_MODEL", "gpt-6.1-sol")
EMBED_MODEL = os.getenv("FINITE_EMBED_MODEL", "text-embedding-3-small")

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) FiniteNewsBot/0.1 (+https://github.com/finite)"
INGEST_INTERVAL_MIN = int(os.getenv("FINITE_INGEST_INTERVAL_MIN", "60"))
PREPARE_BEFORE_MIN = 30
MAX_DEPTH = 2
