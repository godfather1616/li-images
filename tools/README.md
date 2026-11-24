# Card renderer
Renders 1200x1200 post images with rotating layouts and palettes and a compact footer
(QR + "SCAN TO VISIT", website, both phone numbers, CA India / ICAEW / CAW logos; never the firm name).

    cd tools && npm install --silent && pip install qrcode pillow
    python3 -I cards.py <posts.json> "$PWD/assets" "$PWD" <out_dir_abs>
    node shoot.js <out_dir_abs>      # writes post-NN.png next to post-NN.html

Paths passed to cards.py and shoot.js must be absolute. posts.json = {"posts":[{"card":{...}}]}.

## Card fields
Every card: "kind", "theme", "footer", optional "eyebrow". "|" in a headline forces a line break.
- theme  dark: navy | emerald | plum | slate | teal;  light: paper | sky | mint;  bold colour: coral | sun
- footer band  (white strip: QR left, contacts, logos right)
         tint  (strip in the theme's deep colour, logos on a white pill)
         float (rounded floating card: logos left, contacts, QR right)
         top   (logos pill at the TOP of the card; slim contact line + QR at the bottom)
  photo and holiday cards use band/tint/float only and always a dark ground.
- bignum    one figure: "headline", "num", "label".  Two figures: "headline", "stats": [[num, label], [num, label]]
- checklist "headline", "items": [3-5 short lines]
- split     "headline" + "photo": "hero-*.jpg" (+ optional "sub"), or "headline" + "items": [3-5 chips]
- timeline  "headline", "steps": [[date, text], ...], optional "note"; "layout": "cols" = side-by-side date cards
- steps     "headline", "items": [numbered steps, up to 6]
- quote     "headline" (statement; wrap a word in *asterisks* to highlight it), optional "sub"
- photo     full-bleed "photo": "hero-*.jpg" (assets only), "headline", optional "sub"
- holiday   warm palette (theme ignored): "headline" (2-4 words), "sub"

## Variety rule
No two consecutive posts may share the same kind, theme, footer style or ground (dark / light / bold).
Avoid repeating a kind or footer used in the last 3 posts. Aim for roughly a third light grounds.
Check the previous posts' cards in linkedin/queue.json before choosing.

Images for posts live in YYYY-MM/ folders and are added only after approval.
