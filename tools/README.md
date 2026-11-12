# Card renderer
Renders 1200x1200 post images.

    cd tools && npm install --silent
    python3 -I cards.py <posts.json> "$PWD/assets" "$PWD" <out_dir_abs>
    node shoot.js <out_dir_abs>      # writes post-NN.png next to post-NN.html

Paths passed to cards.py and shoot.js must be absolute.
Card kinds: list, timeline, stats, steps, photo (photo = a hero-*.jpg in assets), holiday.
Images for posts live in YYYY-MM/ folders and are added only after approval.
