"""Resolve HN discovery metadata without treating it as source evidence."""
import ipaddress
import re
import socket
import time
from urllib.parse import urljoin, urlsplit, quote

import httpx
import trafilatura

VERSION = 1


def metadata(text):
    return bool(re.search(r'Article URL:|Comments URL:|# Comments:', text or '', re.I))


def public_url(url):
    p = urlsplit(url)
    if p.scheme not in {'http', 'https'} or not p.hostname or p.username or p.password or p.port not in {None, 80, 443}:
        raise ValueError('Unsupported source URL')
    addresses = socket.getaddrinfo(p.hostname, p.port or (443 if p.scheme == 'https' else 80), type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
        raise ValueError('Non-public source URL')
    return addresses[0][4][0]


def fetch(url):
    # Validate every redirect; bound response size and never execute repository code.
    for _ in range(4):
        address = public_url(url)
        parsed = urlsplit(url)
        host = parsed.hostname
        target = httpx.URL(url).copy_with(host=address)
        with httpx.Client(trust_env=False) as client, client.stream('GET', target, headers={'Host': parsed.netloc}, extensions={'sni_hostname': host}, timeout=12, follow_redirects=False) as r:
            if r.is_redirect:
                url = urljoin(url, r.headers['location'])
                continue
            r.raise_for_status()
            kind = r.headers.get('content-type', '')
            if not any(t in kind for t in ('text/', 'application/json', 'application/xhtml')):
                raise ValueError('Unsupported content type')
            chunks, size = [], 0
            for part in r.iter_bytes():
                size += len(part)
                if size > 2_000_000:
                    raise ValueError('Source too large')
                chunks.append(part)
            return b''.join(chunks).decode('utf-8', errors='replace'), kind
    raise ValueError('Too many redirects')


def readme_prose(text):
    """Keep prose, excluding code blocks and tables from extractive previews."""
    text = re.sub(r"```[\s\S]*?```|~~~[\s\S]*?~~~", "", text)
    lines = [line for line in text.splitlines() if not re.match(r"^\s*(?:#|\||<|!\[)", line)]
    text = "\n".join(lines)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return re.sub(r"[*`_]", "", text).strip()


def resolve(article):
    desc = article.get('description') or ''
    original = re.search(r'Article URL:\s*(https?://\S+)', desc)
    discussion = re.search(r'Comments URL:\s*(https?://news\.ycombinator\.com/\S+)', desc)
    url = original.group(1) if original else article['url']
    info = {'version': VERSION, 'url': url, 'discussion_url': discussion.group(1) if discussion else None,
            'checked_at': time.time(), 'content': '', 'status': 'unavailable'}
    try:
        p = urlsplit(url)
        if p.hostname == 'news.ycombinator.com':
            # Self posts are discussion, not independent article evidence.
            return info
        if p.hostname == 'gitlab.com' and len(p.path.strip('/').split('/')) == 2:
            project = quote(p.path.strip('/'), safe='')
            raw, _ = fetch(f'https://gitlab.com/api/v4/projects/{project}/repository/files/README.md/raw?ref=HEAD')
            text = readme_prose(raw)
        else:
            raw, kind = fetch(url)
            text = trafilatura.extract(raw, include_comments=False, favor_precision=True) if 'html' in kind else raw
        text = (text or '').strip()
        if len(text.split()) >= 40 and not metadata(text) and not re.search(r'just a moment|verify you are human|enable javascript', text[:400], re.I):
            info.update(content=text[:20000], status='available')
    except (httpx.HTTPError, ValueError, OSError, KeyError):
        pass
    return info
