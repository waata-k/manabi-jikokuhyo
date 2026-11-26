"""Build the installable web app (index.html) from src/app.html.

    python3 tools/build.py                       # -> index.html (no data inside; for GitHub Pages)
    python3 tools/build.py --embed my-data.json --out private/manabi.html
                                                 # -> one file with your data built in (keep it private)
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="単元チェック・今日やること・通学経路・勉強タイマーをまとめた勉強用アプリ。データは各自の端末に保存されます。">
<meta name="theme-color" content="#F1F3EF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0E1215" media="(prefers-color-scheme: dark)">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="まなび時刻表">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px/1.4 system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
"""

SW_REGISTER = """<script>
if ('serviceWorker' in navigator && /^https?:$/.test(location.protocol)) {
  addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
}
</script>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--embed', help='data file (manabi-data JSON) to build into the page')
    ap.add_argument('--out', default=os.path.join(ROOT, 'index.html'))
    args = ap.parse_args()

    app = open(os.path.join(ROOT, 'src', 'app.html'), encoding='utf-8').read()
    # everything before the first <header> (title, font links, styles) belongs in <head>
    cut = app.index('<header class="top">')
    head_part, body_part = app[:cut], app[cut:]
    head_part = head_part.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')

    if args.embed:
        pack = json.load(open(args.embed, encoding='utf-8'))
        assert pack.get('format') == 'manabi-data', 'not a manabi-data file'
        blob = json.dumps(pack, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
        body_part = body_part.replace('<!--DATA_PACK-->', f'<script type="application/json" id="data-pack">{blob}</script>')

    html = HEAD + head_part + '</head>\n<body>\n' + body_part + (SW_REGISTER if not args.embed else '') + '</body>\n</html>\n'
    open(args.out, 'w', encoding='utf-8').write(html)
    print(f'wrote {os.path.relpath(args.out, ROOT)} ({len(html.encode("utf-8")):,} bytes)')


if __name__ == '__main__':
    main()
