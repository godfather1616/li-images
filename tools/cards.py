# Usage: python3 -I cards.py posts.json assets_dir fonts_dir out_dir
# Each post's card has: kind + optional theme. Renderer rotates layouts & palettes
# so no two posts look alike. Kinds: photo, bignum, split, checklist, timeline,
# steps, quote, holiday. Footer carries QR + contacts + logos (compact), never the firm name.
import sys, json, html, os, base64
posts_file, assets, fonts, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
data = json.load(open(posts_file, encoding='utf-8'))
import qrcode, io
_q = qrcode.QRCode(border=1, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
_q.add_data('https://globalbookkeepingservices.com'); _q.make(fit=True)
_b = io.BytesIO(); _q.make_image(fill_color='#0A2540', back_color='white').save(_b, format='PNG')
QR = base64.b64encode(_b.getvalue()).decode()
B64 = lambda f: base64.b64encode(open(os.path.join(assets, f), 'rb').read()).decode()
LOGOS = [B64('logo-ca-india.png'), B64('logo-icaew.png'), B64('logo-caw.png')]
F = lambda n: f"file://{fonts}/node_modules/@fontsource/{n}"
e = lambda t: html.escape(t).replace('|', '<br>')

# ---- Palettes. Each post gets a theme; adjacent posts should differ (set in posts.json). ----
THEMES = {
    'navy':    {'bg': 'radial-gradient(1100px 850px at 100% 0%,#0B4FC4 0%,rgba(11,79,196,0) 58%),linear-gradient(158deg,#0A2540 0%,#0C2F57 100%)',
                'accent': '#F5C542', 'ink': '#0A2540', 'soft': 'rgba(255,255,255,.10)', 'line': 'rgba(255,255,255,.14)'},
    'emerald': {'bg': 'radial-gradient(1100px 850px at 0% 0%,#0E6B55 0%,rgba(14,107,85,0) 58%),linear-gradient(158deg,#06352E 0%,#0A4A40 100%)',
                'accent': '#64E0B0', 'ink': '#063129', 'soft': 'rgba(255,255,255,.09)', 'line': 'rgba(255,255,255,.14)'},
    'plum':    {'bg': 'radial-gradient(1100px 850px at 100% 0%,#7A3FA6 0%,rgba(122,63,166,0) 58%),linear-gradient(158deg,#2C1540 0%,#44225C 100%)',
                'accent': '#F3C969', 'ink': '#2A1540', 'soft': 'rgba(255,255,255,.10)', 'line': 'rgba(255,255,255,.15)'},
    'slate':   {'bg': 'radial-gradient(1100px 850px at 100% 0%,#2C4A6E 0%,rgba(44,74,110,0) 58%),linear-gradient(158deg,#132235 0%,#1B3350 100%)',
                'accent': '#FF8E6E', 'ink': '#14263B', 'soft': 'rgba(255,255,255,.08)', 'line': 'rgba(255,255,255,.13)'},
    'teal':    {'bg': 'radial-gradient(1100px 850px at 0% 100%,#0E7C86 0%,rgba(14,124,134,0) 58%),linear-gradient(158deg,#07323A 0%,#0B4852 100%)',
                'accent': '#F6C85F', 'ink': '#06313A', 'soft': 'rgba(255,255,255,.09)', 'line': 'rgba(255,255,255,.14)'},
}
def theme(c):
    return THEMES.get(c.get('theme', 'navy'), THEMES['navy'])

CSS = f'''
@font-face{{font-family:Lora;font-weight:600;src:url({F("lora/files/lora-latin-600-normal.woff2")})}}
@font-face{{font-family:Lora;font-weight:700;src:url({F("lora/files/lora-latin-700-normal.woff2")})}}
@font-face{{font-family:Lora;font-weight:700;font-style:italic;src:url({F("lora/files/lora-latin-700-italic.woff2")})}}
@font-face{{font-family:Nunito;font-weight:400;src:url({F("nunito-sans/files/nunito-sans-latin-400-normal.woff2")})}}
@font-face{{font-family:Nunito;font-weight:600;src:url({F("nunito-sans/files/nunito-sans-latin-600-normal.woff2")})}}
@font-face{{font-family:Nunito;font-weight:700;src:url({F("nunito-sans/files/nunito-sans-latin-700-normal.woff2")})}}
@font-face{{font-family:Nunito;font-weight:800;src:url({F("nunito-sans/files/nunito-sans-latin-800-normal.woff2")})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:1200px;overflow:hidden}}
body{{font-family:Nunito;color:#fff;position:relative}}
.wrap{{position:absolute;inset:0;padding:78px 88px 0 88px;display:flex;flex-direction:column}}
.eyebrow{{font-weight:800;font-size:24px;letter-spacing:4px;text-transform:uppercase;margin-bottom:22px;display:flex;align-items:center;gap:16px}}
.eyebrow::before{{content:"";width:46px;height:5px;border-radius:3px;background:var(--acc)}}
h1{{font-family:Lora;font-weight:700;font-size:78px;line-height:1.07;letter-spacing:-0.5px}}
.main{{flex:1;display:flex;flex-direction:column;justify-content:center;padding:26px 0 30px;min-height:0}}
.sub{{font-size:33px;font-weight:600;color:rgba(255,255,255,.86);margin-top:24px;line-height:1.32;max-width:940px}}

/* ---- compact footer (≈150px, was 270) ---- */
.foot{{height:152px;background:#fff;color:#0A2540;display:flex;align-items:center;gap:30px;margin:0 -88px;padding:0 64px}}
.qrw{{flex:none;display:flex;flex-direction:column;align-items:center;gap:5px}}
.qr{{width:112px;height:112px;display:block}}
.qrl{{font-weight:800;font-size:12px;letter-spacing:2px;color:#0047BB}}
.fr{{flex:1;display:flex;align-items:center;justify-content:space-between;gap:28px;border-left:2px solid #E3E9F0;padding-left:34px}}
.contacts{{display:flex;flex-direction:column;gap:7px}}
.cline{{display:flex;align-items:center;gap:11px;font-size:18px;font-weight:700;color:#0A2540}}
.cline svg{{width:19px;height:19px;flex:none}}
.web-t{{font-weight:800}}
.logos{{display:flex;align-items:center;gap:26px;flex:none}}
.lg{{height:66px;width:auto;display:block}}

/* ---- checklist ---- */
.cards{{display:flex;flex-direction:column;gap:20px}}
.crow{{background:var(--soft);border-left:7px solid var(--acc);border-radius:16px;padding:26px 30px;display:flex;align-items:center;gap:24px;font-size:35px;font-weight:700;line-height:1.22}}
.ck{{flex:none;width:50px;height:50px;border-radius:13px;background:var(--acc);display:flex;align-items:center;justify-content:center}}
.ck svg{{width:28px;height:28px}}

/* ---- bignum ---- */
.bq{{font-family:Lora;font-weight:700;font-size:58px;line-height:1.12;max-width:980px}}
.bnum{{font-family:Lora;font-weight:700;font-size:210px;line-height:.9;color:var(--acc);letter-spacing:-3px;margin:18px 0 6px}}
.blab{{font-size:34px;font-weight:700;color:rgba(255,255,255,.9);max-width:820px;line-height:1.28}}
.bnum2{{display:flex;align-items:baseline;gap:40px;flex-wrap:wrap}}
.bn2{{font-family:Lora;font-weight:700;font-size:120px;line-height:.95;color:var(--acc);letter-spacing:-2px}}
.bn2 span{{display:block;font-family:Nunito;font-size:26px;font-weight:700;color:rgba(255,255,255,.85);letter-spacing:0;margin-top:10px}}

/* ---- split ---- */
.split{{display:flex;gap:46px;align-items:stretch}}
.spL{{flex:1;display:flex;flex-direction:column;justify-content:center}}
.spR{{flex:none;width:420px;display:flex;flex-direction:column;gap:16px;justify-content:center}}
.chip{{background:var(--soft);border:1px solid var(--line);border-radius:18px;padding:22px 26px;font-size:28px;font-weight:700;line-height:1.22;display:flex;gap:16px;align-items:flex-start}}
.chip .d{{flex:none;width:14px;height:14px;border-radius:50%;background:var(--acc);margin-top:12px}}
.spPhoto{{flex:none;width:430px;border-radius:26px;background-size:cover;background-position:center;align-self:stretch;margin:6px 0}}

/* ---- timeline ---- */
.tlwrap{{position:relative;padding-left:48px}}
.tlwrap::before{{content:"";position:absolute;left:14px;top:12px;bottom:12px;width:4px;background:var(--line);border-radius:2px}}
.tlr{{position:relative;padding:18px 0;display:flex;align-items:baseline;gap:30px}}
.tlr::before{{content:"";position:absolute;left:-41px;top:26px;width:24px;height:24px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 7px var(--soft)}}
.tdate{{flex:none;min-width:270px;font-family:Lora;font-weight:700;font-size:44px;color:var(--acc)}}
.ttxt{{font-size:33px;font-weight:700;line-height:1.24}}
.note{{font-size:23px;color:rgba(255,255,255,.58);margin-top:24px;font-weight:600}}

/* ---- steps ---- */
.steps{{display:flex;flex-direction:column;gap:18px}}
.srow{{display:flex;gap:28px;align-items:center}}
.sn{{flex:none;width:76px;height:76px;border-radius:50%;background:var(--acc);color:var(--ink);font-family:Lora;font-weight:700;font-size:40px;display:flex;align-items:center;justify-content:center}}
.stx{{font-size:34px;font-weight:700;line-height:1.22}}

/* ---- quote ---- */
.quote{{font-family:Lora;font-weight:700;font-size:72px;line-height:1.14;letter-spacing:-0.5px;max-width:1010px}}
.quote .hl{{color:var(--acc)}}
.qrule{{width:120px;height:7px;border-radius:4px;background:var(--acc);margin-bottom:40px}}

/* ---- photo ---- */
.photo{{position:absolute;inset:0;background-size:cover;background-position:center}}
.shade{{position:absolute;inset:0;background:linear-gradient(175deg,rgba(10,22,40,.30) 0%,rgba(10,22,40,.48) 38%,rgba(10,22,40,.92) 80%)}}
'''

CHECK = '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="var(--ink)" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
GLOBE_SM = '<svg viewBox="0 0 24 24" fill="none" stroke="#0047BB" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.6 2.7 2.6 15.3 0 18M12 3c-2.6 2.7-2.6 15.3 0 18"/></svg>'
PHONE_SM = '<svg viewBox="0 0 24 24" fill="#0047BB"><path d="M6.6 2.6a1.5 1.5 0 0 1 1.45.95l1.1 2.75a1.5 1.5 0 0 1-.34 1.63L8.3 9.0a11.5 11.5 0 0 0 4.9 4.9l1.07-1.11a1.5 1.5 0 0 1 1.63-.34l2.75 1.1a1.5 1.5 0 0 1 .95 1.45v2.2a2 2 0 0 1-2.17 2A16.5 16.5 0 0 1 2.6 4.77 2 2 0 0 1 4.6 2.6h2z"/></svg>'
WA_SM = '<svg viewBox="0 0 24 24" fill="#0047BB"><path d="M12 2.2a9.8 9.8 0 0 0-8.4 14.8L2.3 21.8l4.9-1.3A9.8 9.8 0 1 0 12 2.2zm0 1.9a7.9 7.9 0 0 1 0 15.8 7.8 7.8 0 0 1-3.9-1l-.28-.17-2.9.76.78-2.83-.18-.29A7.9 7.9 0 0 1 12 4.1zM8.9 7.9c-.15 0-.4.06-.6.3-.21.24-.8.78-.8 1.9 0 1.12.82 2.2.93 2.36.12.15 1.6 2.56 3.96 3.49 1.96.77 2.36.62 2.79.58.43-.04 1.37-.56 1.56-1.1.19-.54.19-1 .13-1.1-.06-.1-.21-.15-.45-.27-.24-.12-1.37-.68-1.58-.76-.21-.08-.37-.12-.53.12-.15.24-.6.76-.73.91-.13.15-.27.17-.5.06-.24-.12-1-.37-1.9-1.18-.7-.62-1.18-1.4-1.32-1.64-.14-.24-.01-.37.1-.49.11-.11.24-.28.36-.42.12-.15.16-.25.24-.41.08-.16.04-.3-.02-.42-.06-.12-.53-1.3-.73-1.78-.19-.46-.38-.4-.53-.41h-.45z"/></svg>'

def foot():
    logos = ''.join(f'<img class="lg" src="data:image/png;base64,{b}">' for b in LOGOS)
    return (f'<div class="foot"><div class="qrw"><img class="qr" src="data:image/png;base64,{QR}"><div class="qrl">SCAN TO VISIT</div></div>'
            f'<div class="fr"><div class="contacts">'
            f'<div class="cline">{GLOBE_SM}<span class="web-t">www.globalbookkeepingservices.com</span></div>'
            f'<div class="cline">{PHONE_SM}<span>+1 (646) 837-7740</span></div>'
            f'<div class="cline">{WA_SM}<span>+91 94083 19123</span></div>'
            f'</div><div class="logos">{logos}</div></div></div>')

def page(body, th, extra_css=''):
    root = f':root{{--acc:{th["accent"]};--ink:{th["ink"]};--soft:{th["soft"]};--line:{th["line"]}}}body{{background:{th["bg"]}}}'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{root}{extra_css}</style></head><body>{body}</body></html>'

def eb_html(c):
    return f'<div class="eyebrow">{e(c["eyebrow"])}</div>' if c.get('eyebrow') else ''

def card(c):
    k = c['kind']; th = theme(c); eb = eb_html(c)

    if k == 'checklist':
        items = ''.join(f'<div class="crow"><div class="ck">{CHECK}</div><div>{e(t)}</div></div>' for t in c['items'])
        return page(f'<div class="wrap">{eb}<h1>{e(c["headline"])}</h1><div class="main"><div class="cards">{items}</div></div>{foot()}</div>', th)

    if k == 'bignum':
        # one big number, or two side by side (stats-style [[num,label],...])
        if c.get('stats'):
            cells = ''.join(f'<div class="bn2">{e(a)}<span>{e(b)}</span></div>' for a, b in c['stats'])
            body = f'<h1 style="font-size:60px;max-width:960px">{e(c["headline"])}</h1><div class="main"><div class="bnum2">{cells}</div></div>'
        else:
            body = (f'<div class="bq">{e(c["headline"])}</div><div class="main" style="justify-content:flex-start;padding-top:10px">'
                    f'<div class="bnum">{e(c["num"])}</div><div class="blab">{e(c["label"])}</div></div>')
        return page(f'<div class="wrap">{eb}{body}{foot()}</div>', th)

    if k == 'split':
        if c.get('photo'):
            img = B64(c['photo'])
            right = f'<div class="spPhoto" style="background-image:url(data:image/jpeg;base64,{img})"></div>'
        else:
            right = ''.join(f'<div class="chip"><span class="d"></span><span>{e(t)}</span></div>' for t in c['items'])
            right = f'<div class="spR">{right}</div>'
        if c.get('photo'):
            layout = f'<div class="split"><div class="spL">{eb}<h1>{e(c["headline"])}</h1>{("<div class=sub>"+e(c["sub"])+"</div>") if c.get("sub") else ""}</div>{right}</div>'
        else:
            layout = f'<div class="split"><div class="spL">{eb}<h1 style="font-size:66px">{e(c["headline"])}</h1></div>{right}</div>'
        return page(f'<div class="wrap"><div class="main" style="justify-content:center">{layout}</div>{foot()}</div>', th)

    if k == 'timeline':
        rows = ''.join(f'<div class="tlr"><div class="tdate">{e(a)}</div><div class="ttxt">{e(b)}</div></div>' for a, b in c['steps'])
        note = f'<div class="note">{e(c["note"])}</div>' if c.get('note') else ''
        return page(f'<div class="wrap">{eb}<h1>{e(c["headline"])}</h1><div class="main"><div class="tlwrap">{rows}</div>{note}</div>{foot()}</div>', th)

    if k == 'steps':
        rows = ''.join(f'<div class="srow"><div class="sn">{i+1}</div><div class="stx">{e(t)}</div></div>' for i, t in enumerate(c['items']))
        return page(f'<div class="wrap">{eb}<h1>{e(c["headline"])}</h1><div class="main"><div class="steps">{rows}</div></div>{foot()}</div>', th)

    if k == 'quote':
        # headline: escape first, then *word* -> accent highlight, | -> line break
        hl = e(c["headline"])
        import re
        hl = re.sub(r'\*([^*]+)\*', r'<span class="hl">\1</span>', hl)
        return page(f'<div class="wrap">{eb}<div class="main" style="justify-content:center"><div class="qrule"></div><div class="quote">{hl}</div>{("<div class=sub>"+e(c["sub"])+"</div>") if c.get("sub") else ""}</div>{foot()}</div>', th)

    if k == 'photo':
        img = B64(c['photo'])
        body = (f'<div class="photo" style="background-image:url(data:image/jpeg;base64,{img})"></div><div class="shade"></div>'
                f'<div class="wrap"><div class="main" style="justify-content:flex-end;padding-bottom:40px">{eb}<h1>{e(c["headline"])}</h1>'
                f'{("<div class=sub>"+e(c["sub"])+"</div>") if c.get("sub") else ""}</div>{foot()}</div>')
        return page(body, th)

    if k == 'holiday':
        import random
        random.seed(c.get('seed', 11))
        cols = ['#E5A823', '#D9822B', '#B5541C', '#F2C25C', '#9C3D10']
        spots = [(70, 80), (980, 60), (1090, 300), (36, 540), (1070, 470), (150, 770), (870, 200), (330, 96), (690, 120), (430, 560)]
        leaves = ''
        for (x, y) in spots:
            s = random.randint(72, 128); r = random.randint(0, 360); col = random.choice(cols)
            leaves += (f'<svg style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;transform:rotate({r}deg);opacity:.9" viewBox="0 0 100 100">'
                       f'<path d="M50 4 C62 20 82 22 94 34 C82 40 86 56 96 66 C80 68 70 78 66 94 C58 84 54 80 50 96 C46 80 42 84 34 94 C30 78 20 68 4 66 C14 56 18 40 6 34 C18 22 38 20 50 4Z" fill="{col}"/>'
                       f'<path d="M50 20 V92" stroke="rgba(0,0,0,.25)" stroke-width="3"/></svg>')
        css = ('body{background:radial-gradient(900px 700px at 50% 38%,#5A2A10 0%,#3A1A0A 100%)}'
               'h1{font-size:118px;text-align:center;color:#FFF3DC;max-width:none}.sub{text-align:center;color:#F7D9A8;max-width:none}')
        body = f'{leaves}<div class="wrap"><div class="main" style="align-items:center;text-align:center">{eb}<h1>{e(c["headline"])}</h1><div class="sub">{e(c["sub"])}</div></div>{foot()}</div>'
        return page(body, th, css)

    raise ValueError(k)

for i, p in enumerate(data['posts'], 1):
    fn = os.path.join(out, f'post-{i:02d}.html')
    open(fn, 'w', encoding='utf-8').write(card(p['card']))
    print(fn)
