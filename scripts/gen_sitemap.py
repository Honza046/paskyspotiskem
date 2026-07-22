#!/usr/bin/env python3
"""Generate robots.txt and sitemap.xml for the static site."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from seo import SITE_URL

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()


def collect_urls() -> list[tuple[str, str, str]]:
    """Return list of (path, changefreq, priority)."""
    urls: list[tuple[str, str, str]] = [
        ('/', 'weekly', '1.0'),
        ('/sortiment', 'weekly', '0.9'),
        ('/galerie', 'weekly', '0.8'),
        ('/faq', 'monthly', '0.7'),
    ]
    sortiment_root = ROOT / 'sortiment'
    if sortiment_root.is_dir():
        for html_path in sorted(sortiment_root.rglob('index.html')):
            rel = html_path.relative_to(ROOT).as_posix()
            if rel == 'sortiment/index.html':
                continue
            path = '/' + rel[:-len('index.html')]
            if path.endswith('/'):
                path = path[:-1]
            depth = path.count('/')
            if depth <= 2:
                priority = '0.85'
            elif depth == 3:
                priority = '0.7'
            else:
                priority = '0.65'
            urls.append((path, 'monthly', priority))
    return urls


def write_robots() -> None:
    content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    (ROOT / 'robots.txt').write_text(content, encoding='utf-8')
    print('  wrote robots.txt')


def write_sitemap() -> None:
    urls = collect_urls()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, changefreq, priority in urls:
        loc = SITE_URL + (path if path != '/' else '/')
        lines.extend([
            '  <url>',
            f'    <loc>{loc}</loc>',
            f'    <lastmod>{TODAY}</lastmod>',
            f'    <changefreq>{changefreq}</changefreq>',
            f'    <priority>{priority}</priority>',
            '  </url>',
        ])
    lines.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'  wrote sitemap.xml ({len(urls)} URLs)')


def main() -> int:
    print('Generating SEO files…')
    write_robots()
    write_sitemap()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
