# Usage: python3 -I cards.py posts.json assets_dir fonts_dir out_dir
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
e = lambda t: html.escape(t).replace('|','<br>')

LOGO = '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
<rect x="4" y="4" width="92" height="92" rx="22" fill="#0047BB"/>
<circle cx="50" cy="50" r="29" fill="none" stroke="#4D83D8" stroke-width="4"/>
<ellipse cx="50" cy="50" rx="13" ry="29" fill="none" stroke="#4D83D8" stroke-width="3.5"/>
<path d="M21 50 h58" stroke="#4D83D8" stroke-width="3.5"/>
<path d="M34 64 L44 54 L51 59 L66 41" fill="none" stroke="#E5A823" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="66" cy="41" r="4.5" fill="#E5A823"/></svg>'''

CSS = f'''
@font-face{{font-family:Lora;font-weight:600;src:url({F("lora/files/lora-latin-600-normal.woff2")})}}
@font-face{{font-family:Lora;font-weight:700;src:url({F("lora/files/lora-latin-700-normal.woff2")})}}
@font-face{{font-family:Nunito;font-weight:400;src:url({F("nunito-sans/files/nunito-sans-latin-400-normal.woff2")})}}
@font-face{{font-family:Nunito;font-weight:600;src:url({F("nunito-sans/files/nunito-sans-latin-600-normal.woff2")})}}
@font-face{{font-family:Nunito;font-weight:700;src:url({F("nunito-sans/files/nunito-sans-latin-700-normal.woff2")})}}
@font-face{{font-family:Nunito;font-weight:800;src:url({F("nunito-sans/files/nunito-sans-latin-800-normal.woff2")})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:1200px;overflow:hidden}}
body{{font-family:Nunito;color:#fff;position:relative;
  background:radial-gradient(1200px 900px at 100% 0%,#0B4FC4 0%,rgba(11,79,196,0) 60%),linear-gradient(160deg,#0A2540 0%,#0C2F57 100%)}}
.wrap{{position:absolute;inset:0;padding:80px 96px 0 96px;display:flex;flex-direction:column}}
.eyebrow{{font-weight:800;font-size:26px;letter-spacing:4px;color:#F5C542;margin-bottom:28px}}
h1{{font-family:Lora;font-weight:700;font-size:80px;line-height:1.08;letter-spacing:-0.5px;max-width:1000px}}
.main{{flex:1;display:flex;flex-direction:column;justify-content:center;padding:30px 0 34px}}
.foot{{height:270px;background:#fff;color:#0A2540;display:flex;align-items:center;gap:36px;margin:0 -96px;padding:0 70px}}
.qrw{{flex:none;display:flex;flex-direction:column;align-items:center;gap:8px}}
.qr{{width:178px;height:178px;display:block}}
.qrl{{font-weight:800;font-size:16px;letter-spacing:2.5px;color:#0047BB}}
.fr{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:10px;border-left:2px solid #E3E9F0;padding-left:40px}}
.cline{{display:flex;align-items:center;gap:12px;font-size:21px;font-weight:600;color:#0A2540}}
.cline svg{{width:23px;height:23px;flex:none}}
.cline b{{font-weight:800;color:#0047BB;margin-right:7px}}
.web-t{{font-weight:800;letter-spacing:-0.2px}}
.logos{{display:flex;align-items:center;gap:36px;margin-top:8px}}
.lg{{height:98px;width:auto;display:block}}
.li{{display:flex;align-items:center;gap:30px;padding:24px 0;border-bottom:1px solid rgba(255,255,255,.12);font-size:38px;font-weight:600;line-height:1.25}}
.li:last-child{{border-bottom:0}}
.ck{{flex:none;width:54px;height:54px;border-radius:50%;background:#F5C542;display:flex;align-items:center;justify-content:center}}
.ck svg{{width:30px;height:30px}}
.tl{{display:flex;align-items:center;gap:34px;padding:22px 0}}
.pill{{flex:none;width:330px;background:#F5C542;color:#0A2540;font-weight:800;font-size:34px;border-radius:999px;padding:18px 0;text-align:center}}
.tlt{{font-size:40px;font-weight:700}}
.note{{font-size:24px;color:rgba(255,255,255,.6);margin-top:26px;font-weight:600}}
.stats{{display:flex;flex-direction:column;gap:28px}}
.stat{{background:#fff;border-radius:28px;padding:38px 46px;display:flex;align-items:center;gap:40px;color:#0A2540}}
.num{{font-family:Lora;font-weight:700;font-size:70px;color:#0047BB;flex:none;min-width:380px}}
.lab{{font-size:33px;font-weight:700;line-height:1.25}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}
.step{{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:24px;padding:28px 30px;display:flex;gap:22px;align-items:flex-start;min-height:150px}}
.sn{{flex:none;width:52px;height:52px;border-radius:14px;background:#F5C542;color:#0A2540;font-weight:800;font-size:28px;display:flex;align-items:center;justify-content:center}}
.st{{font-size:30px;font-weight:700;line-height:1.25}}
.photo{{position:absolute;inset:0;background-size:cover;background-position:center}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,37,64,.25) 0%,rgba(10,37,64,.55) 40%,rgba(10,37,64,.96) 78%)}}
.sub{{font-size:34px;font-weight:600;color:rgba(255,255,255,.88);margin-top:28px;line-height:1.3}}
'''

CHECK = '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#0A2540" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

GLOBE_SM = '<svg viewBox="0 0 24 24" fill="none" stroke="#0047BB" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.6 2.7 2.6 15.3 0 18M12 3c-2.6 2.7-2.6 15.3 0 18"/></svg>'
PHONE_SM = '<svg viewBox="0 0 24 24" fill="#0047BB"><path d="M6.6 2.6a1.5 1.5 0 0 1 1.45.95l1.1 2.75a1.5 1.5 0 0 1-.34 1.63L8.3 9.0a11.5 11.5 0 0 0 4.9 4.9l1.07-1.11a1.5 1.5 0 0 1 1.63-.34l2.75 1.1a1.5 1.5 0 0 1 .95 1.45v2.2a2 2 0 0 1-2.17 2A16.5 16.5 0 0 1 2.6 4.77 2 2 0 0 1 4.6 2.6h2z"/></svg>'

WA_SM = '<svg viewBox="0 0 24 24" fill="#0047BB"><path d="M12 2.2a9.8 9.8 0 0 0-8.4 14.8L2.3 21.8l4.9-1.3A9.8 9.8 0 1 0 12 2.2zm0 1.9a7.9 7.9 0 0 1 0 15.8 7.8 7.8 0 0 1-3.9-1l-.28-.17-2.9.76.78-2.83-.18-.29A7.9 7.9 0 0 1 12 4.1zM8.9 7.9c-.15 0-.4.06-.6.3-.21.24-.8.78-.8 1.9 0 1.12.82 2.2.93 2.36.12.15 1.6 2.56 3.96 3.49 1.96.77 2.36.62 2.79.58.43-.04 1.37-.56 1.56-1.1.19-.54.19-1 .13-1.1-.06-.1-.21-.15-.45-.27-.24-.12-1.37-.68-1.58-.76-.21-.08-.37-.12-.53.12-.15.24-.6.76-.73.91-.13.15-.27.17-.5.06-.24-.12-1-.37-1.9-1.18-.7-.62-1.18-1.4-1.32-1.64-.14-.24-.01-.37.1-.49.11-.11.24-.28.36-.42.12-.15.16-.25.24-.41.08-.16.04-.3-.02-.42-.06-.12-.53-1.3-.73-1.78-.19-.46-.38-.4-.53-.41h-.45z"/></svg>'

def foot(light=False):
    logos = ''.join(f'<img class="lg" src="data:image/png;base64,{b}">' for b in LOGOS)
    return (f'<div class="foot"><div class="qrw"><img class="qr" src="data:image/png;base64,{QR}"><div class="qrl">SCAN TO VISIT</div></div>'
            f'<div class="fr">'
            f'<div class="cline">{GLOBE_SM}<span class="web-t">www.globalbookkeepingservices.com</span></div>'
            f'<div class="cline">{PHONE_SM}<span>+1 (646) 837-7740</span></div>'
            f'<div class="cline">{WA_SM}<span>+91 94083 19123</span></div>'
            f'<div class="logos">{logos}</div></div></div>')

def page(body, extra_css=''):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{extra_css}</style></head><body>{body}</body></html>'

def card(c):
    k = c['kind']
    eb = f'<div class="eyebrow">{e(c["eyebrow"])}</div>' if c.get('eyebrow') else ''
    if k == 'list':
        items = ''.join(f'<div class="li"><div class="ck">{CHECK}</div><div>{e(t)}</div></div>' for t in c['items'])
        return page(f'<div class="wrap">{eb}<h1>{e(c["headline"])}</h1><div class="main">{items}</div>{foot()}</div>')
    if k == 'timeline':
        rows = ''.join(f'<div class="tl"><div class="pill">{e(a)}</div><div class="tlt">{e(b)}</div></div>' for a, b in c['steps'])
        return page(f'<div class="wrap">{eb}<h1>{e(c["headline"])}</h1><div class="main">{rows}<div class="note">{e(c["note"])}</div></div>{foot()}</div>')
    if k == 'stats':
        rows = ''.join(f'<div class="stat"><div class="num">{e(a)}</div><div class="lab">{e(b)}</div></div>' for a, b in c['stats'])
        return page(f'<div class="wrap">{eb}<h1>{e(c["headline"])}</h1><div class="main"><div class="stats">{rows}</div></div>{foot()}</div>')
    if k == 'steps':
        rows = ''.join(f'<div class="step"><div class="sn">{i+1}</div><div class="st">{e(t)}</div></div>' for i, t in enumerate(c['items']))
        return page(f'<div class="wrap">{eb}<h1>{e(c["headline"])}</h1><div class="main"><div class="grid">{rows}</div></div>{foot()}</div>', 'h1{font-size:72px}')
    if k == 'photo':
        img = base64.b64encode(open(os.path.join(assets, c['photo']), 'rb').read()).decode()
        body = (f'<div class="photo" style="background-image:url(data:image/jpeg;base64,{img})"></div><div class="shade"></div>'
                f'<div class="wrap"><div class="main" style="justify-content:flex-end;padding-bottom:56px">{eb}<h1>{e(c["headline"])}</h1><div class="sub">{e(c["sub"])}</div></div>{foot()}</div>')
        return page(body)
    if k == 'holiday':
        leaves = ''
        import random
        random.seed(11)
        cols = ['#E5A823', '#D9822B', '#B5541C', '#F2C25C', '#9C3D10']
        spots = [(70, 70), (980, 50), (1090, 290), (30, 520), (1070, 760), (130, 780), (860, 180), (330, 80), (660, 790), (400, 800)]
        for (x, y) in spots:
            s = random.randint(70, 130); r = random.randint(0, 360); col = random.choice(cols)
            leaves += (f'<svg style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;transform:rotate({r}deg);opacity:.9" viewBox="0 0 100 100">'
                       f'<path d="M50 4 C62 20 82 22 94 34 C82 40 86 56 96 66 C80 68 70 78 66 94 C58 84 54 80 50 96 C46 80 42 84 34 94 C30 78 20 68 4 66 C14 56 18 40 6 34 C18 22 38 20 50 4Z" fill="{col}"/>'
                       f'<path d="M50 20 V92" stroke="rgba(0,0,0,.25)" stroke-width="3"/></svg>')
        css = 'body{background:radial-gradient(900px 700px at 50% 40%,#5A2A10 0%,#3A1A0A 100%)} h1{font-size:120px;text-align:center;color:#FFF3DC;max-width:none} .sub{text-align:center;color:#F7D9A8}'
        body = f'{leaves}<div class="wrap"><div class="main" style="align-items:center"><h1>{e(c["headline"])}</h1><div class="sub">{e(c["sub"])}</div></div>{foot()}</div>'
        return page(body, css)
    raise ValueError(k)

for i, p in enumerate(data['posts'], 1):
    fn = os.path.join(out, f'post-{i:02d}.html')
    open(fn, 'w', encoding='utf-8').write(card(p['card']))
    print(fn)
