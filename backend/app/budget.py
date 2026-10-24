"""Persistent, conservative $1 allowance for this installation's OpenAI calls.

Reservations are never refunded: even a timeout may have incurred a charge.
This is an application guard, not an account-wide billing limit.
"""
from contextlib import closing
import sqlite3
import time

from .config import DATA_DIR

BUDGET_PATH = DATA_DIR / "ai_budget.sqlite3"
LIMIT_MICRODOLLARS = 1_000_000
MAX_CALLS = 100
# Conservative rates above standard pricing, including long-context pricing.
# USD per million tokens == microdollars per token. Reviewed 2026-10-25:
# https://developers.openai.com/api/docs/pricing
RATES = {"gpt-6-luna": (1, 2), "gpt-6.1-sol": (8, 30),
         "text-embedding-3-small": (1, 0)}


class BudgetBlocked(ValueError):
    pass


def reserve(model, texts, output_tokens=0):
    if model not in RATES:
        raise BudgetBlocked("Model has no reviewed budget rate")
    if type(output_tokens) is not int or not 0 <= output_tokens <= 12000:
        raise BudgetBlocked("Output token limit must be between 0 and 12000")
    # UTF-8 bytes conservatively bound text tokens; allowance covers framing.
    input_bound = sum(len(t.encode("utf-8")) + 512 for t in texts)
    if input_bound > 100_000:
        raise BudgetBlocked("Request exceeds the guarded input size")
    rate_in, rate_out = RATES[model]
    amount = input_bound * rate_in + output_tokens * rate_out
    with closing(sqlite3.connect(BUDGET_PATH, timeout=30)) as conn, conn:
        conn.execute("CREATE TABLE IF NOT EXISTS reservations (id INTEGER PRIMARY KEY, model TEXT, amount INTEGER, created_at REAL)")
        conn.execute("BEGIN IMMEDIATE")
        used, calls = conn.execute("SELECT COALESCE(SUM(amount),0), COUNT(*) FROM reservations").fetchone()
        if used + amount > LIMIT_MICRODOLLARS or calls >= MAX_CALLS:
            raise BudgetBlocked("Finite's $1 AI allowance cannot cover another request; using extractive mode")
        conn.execute("INSERT INTO reservations(model,amount,created_at) VALUES(?,?,?)", (model, amount, time.time()))
    return amount


def status():
    if not BUDGET_PATH.exists():
        used, calls = 0, 0
    else:
        with closing(sqlite3.connect(BUDGET_PATH)) as conn:
            used, calls = conn.execute("SELECT COALESCE(SUM(amount),0), COUNT(*) FROM reservations").fetchone()
    return {"limit_usd": 1, "reserved_usd": used / 1_000_000,
            "remaining_usd": max(0, LIMIT_MICRODOLLARS - used) / 1_000_000,
            "requests": calls, "max_requests": MAX_CALLS,
            "scope": "This installation; conservative reservations, not billed usage"}
