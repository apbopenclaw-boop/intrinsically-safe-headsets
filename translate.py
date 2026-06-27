#!/usr/bin/env python3
"""Translate HTML pages using DeepL API. Preserves HTML tags."""
import os, sys, json, urllib.request, urllib.parse, re

DEEPL_KEY = "f79f09e9-9b21-4ed6-a9d4-798b02725484:fx"
DEEPL_URL = "https://api-free.deepl.com/v2/translate"

LANGUAGES = {
    "de": "DE",
    "nl": "NL",
    "es": "ES",
    "pt-br": "PT-BR",
}

PAGES = [
    "index.html",
    "best-atex-headsets-2026.html",
    "what-is-an-intrinsically-safe-headset.html",
]

def translate_html(html_content, target_lang):
    """Translate HTML content using DeepL, preserving tags."""
    data = urllib.parse.urlencode({
        "auth_key": DEEPL_KEY,
        "text": html_content,
        "source_lang": "EN",
        "target_lang": target_lang,
        "tag_handling": "html",
        "ignore_tags": "script,style,code,pre",
    }).encode("utf-8")
    
    req = urllib.request.Request(DEEPL_URL, data=data)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["translations"][0]["text"]
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def fix_translated_html(html, lang_code, lang_deepl):
    """Fix lang attribute and canonical URLs for translated version."""
    # Fix lang attribute
    html = html.replace('lang="en"', f'lang="{lang_code}"')
    
    # Fix canonical to point to translated version
    html = re.sub(
        r'href="https://intrinsicallysafeheadsets\.com/(.*?)"',
        lambda m: f'href="https://intrinsicallysafeheadsets.com/{lang_code}/{m.group(1)}"' 
            if 'canonical' in html[max(0,m.start()-50):m.start()] else m.group(0),
        html
    )
    
    # Update internal links to point to translated versions
    for page in PAGES:
        if page == "index.html":
            html = html.replace(f'href="/"', f'href="/{lang_code}/"')
        else:
            html = html.replace(f'href="/{page}"', f'href="/{lang_code}/{page}"')
    
    # Fix language switcher links to go back to EN for current lang
    html = html.replace(f'href="/{lang_code}/" class="text-[13px] text-muted', f'href="/" class="text-[13px] text-white font-bold')
    
    return html

for lang_code, deepl_lang in LANGUAGES.items():
    os.makedirs(lang_code, exist_ok=True)
    print(f"\n=== Translating to {lang_code} ({deepl_lang}) ===")
    
    for page in PAGES:
        print(f"  {page}...", end=" ", flush=True)
        with open(page, "r") as f:
            content = f.read()
        
        translated = translate_html(content, deepl_lang)
        if translated:
            translated = fix_translated_html(translated, lang_code, deepl_lang)
            out_path = os.path.join(lang_code, page)
            with open(out_path, "w") as f:
                f.write(translated)
            print(f"OK ({len(translated)} bytes)")
        else:
            print("FAILED")

print("\nDone!")
