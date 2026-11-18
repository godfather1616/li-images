# Card renderer
Renders 1200x1200 post images with rotating layouts and palettes and a compact footer
(QR + "SCAN TO VISIT", website, both phone numbers, CA India / ICAEW / CAW logos; never the firm name).

    cd tools && npm install --silent && pip install qrcode pillow
    python3 -I cards.py <posts.json> "$PWD/assets" "$PWD" <out_dir_abs>
    node shoot.js <out_dir_abs>      # writes post-NN.png next to post-NN.html

Paths passed to cards.py and shoot.js must be absolute. posts.json = {"posts":[{"card":{...}}]}.

## Card fields
Every card: "kind", "theme" (navy | emerald | plum | slate | teal), optional "eyebrow". "|" in a headline forces a line break.
- bignum    one figure: "headline", "num", "label".  Two figures: "headline", "stats": [[num, label], [num, label]]
- checklist "headline", "items": [3-5 short lines]
- split     "headline" + "photo": "hero-*.jpg" (+ optional "sub"), or "headline" + "items": [3-5 chips]
- timeline  "headline", "steps": [[date, text], ...], optional "note"
- steps     "headline", "items": [numbered steps, up to 6]
- quote     "headline" (statement; wrap a word in *asterisks* to highlight it), optional "sub"
- photo     full-bleed "photo": "hero-*.jpg" (assets only), "headline", optional "sub"
- holiday   warm palette (theme ignored): "headline" (2-4 words), "sub"

## Variety rule
No two consecutive posts may share the same kind or the same theme. Check the previous posts'
cards in linkedin/queue.json before choosing.

Images for posts live in YYYY-MM/ folders and are added only after approval.
