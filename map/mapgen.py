#!/usr/bin/env python3
"""Generate the world map for THE ABSENT FLAME (Destiny-borrowed place names)."""
import math, random

random.seed(1721)

W, H = 1800, 1200
MAP = dict(x0=40, y0=56, x1=1444, y1=1146)      # map plate
RAIL = dict(x0=1470, y0=56, x1=1774, y1=1146)   # legend rail

# ---------------------------------------------------------------- palette
C = dict(
    # matched to the invitation's night palette
    void="#0B0A12",      # --night, shifted a hair darker for the plate
    sea="#13111C",
    sea2="#1A1728",
    land="#26242E",
    land_hi="#332F3C",
    coast="#8E96A4",
    ink="#7C8590",
    ink_soft="#5A616C",
    text="#D8D0BE",      # --bone
    text_dim="#8C8577",  # --bone-dim
    gold="#A8BECF",      # --steel. they shine like steel swords
    gold_dim="#6E7C8A",
    frost="#A8BECF",     # --steel
    gloam="#6b4a86",
    war="#C4562F",       # --ember
    toll="#8C8577",
    ash="#D8D0BE",
    ember="#C4562F",     # --ember
    coal="#7A2B1C",      # --coal
)

out = []
def e(s): out.append(s)

def esc(s):
    return s.replace("&", "and").replace("<", "").replace(">", "")

def txt(x, y, s, size=13, fill=None, ls=0, anchor="middle", style="normal",
        weight="normal", op=1.0, rot=None, fam=None, upper=False, cls=""):
    fill = fill or C["text"]
    s = esc(s.upper() if upper else s)
    tr = f' transform="rotate({rot} {x} {y})"' if rot is not None else ""
    fm = f' font-family="{fam}"' if fam else ""
    e(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
      f'letter-spacing="{ls}" text-anchor="{anchor}" font-style="{style}" '
      f'font-weight="{weight}" opacity="{op}"{fm}{tr}{cls}>{s}</text>')

# ---------------------------------------------------------------- geometry
def subdivide(pts, rounds=4, amp=0.11):
    for _ in range(rounds):
        new = []
        n = len(pts)
        for i in range(n):
            p, q = pts[i], pts[(i + 1) % n]
            new.append(p)
            dx, dy = q[0] - p[0], q[1] - p[1]
            L = math.hypot(dx, dy) or 1
            nx, ny = -dy / L, dx / L
            d = random.uniform(-1, 1) * amp * L
            new.append(((p[0] + q[0]) / 2 + nx * d, (p[1] + q[1]) / 2 + ny * d))
        pts = new
        amp *= 0.55
    return pts

def chaikin(pts, passes=1):
    for _ in range(passes):
        new = []
        n = len(pts)
        for i in range(n):
            p, q = pts[i], pts[(i + 1) % n]
            new.append((p[0] * .75 + q[0] * .25, p[1] * .75 + q[1] * .25))
            new.append((p[0] * .25 + q[0] * .75, p[1] * .25 + q[1] * .75))
        pts = new
    return pts

def path_of(pts):
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    return d

def inside(pt, poly):
    x, y = pt
    ok = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi):
            ok = not ok
        j = i
    return ok

base = [
    (165,340),(250,275),(345,250),(440,275),(525,225),(620,210),(715,240),
    (805,205),(895,225),(985,200),(1075,240),(1160,215),(1240,265),(1300,250),
    (1330,320),(1350,405),(1330,490),(1355,570),(1330,655),(1350,735),
    (1315,815),(1275,880),
    (1225,935),(1145,965),(1055,945),(965,985),(875,1005),(785,980),(695,1010),
    (605,990),(515,1020),(430,995),(350,955),(280,965),(220,915),
    (180,855),(200,775),(165,705),(190,625),(160,545),(195,475),(165,410),
]
LAND = chaikin(subdivide(base, 4, 0.10), 1)

isle_base = [(1385,586),(1412,606),(1418,634),(1396,660),(1368,656),(1354,624),(1362,598)]
ISLE = chaikin(subdivide(isle_base, 3, 0.09), 1)

# ---------------------------------------------------------------- sites
SITES = [
    ("I",   600,  545, "TWILIGHT GAP",        "the Ember",     "ch. 1"),
    ("II",  1122, 342, "FELWINTER PEAK",      "the Dawn",      "ch. 2"),
    ("III", 1152, 792, "HELLMOUTH",       "the Vigil",     "ch. 3"),
    ("IV",  322,  462, "DUST PALACE",     "the Feast",     "ch. 4"),
    ("V",   560,  928, "SIX FRONTS",          "the Truce",     "ch. 5"),
    ("VI",  855,  440, "KAVZAR",              "the Hush",      "ch. 6"),
    ("VII", 1384, 622, "HARBINGER'S SECLUDE", "the Solitude",  "ch. 7"),
]
HEART = (880, 792)

EXCL = [(x, y, 78) for _, x, y, _, _, _ in SITES] + [(HEART[0], HEART[1], 90)]

MINOR = [  # x, y, label, size, style
    (486, 302, "Glacial Drift", 13, "italic"),
    (452, 388, "Mothyards", 12, "italic"),
    (250, 402, "Fields of Glass", 12, "italic"),
    (256, 592, "Charon's Crossing", 12, "italic"),
    (216, 700, "Lost Oasis", 12, "italic"),
    (398, 692, "Scablands", 12, "italic"),
    (388, 420, "Giant's Scar", 12, "italic"),
    (508, 476, "Widow's Court", 12, "italic"),
    (752, 664, "Trostland", 13, "italic"),
    (726, 706, "Sanctuary", 12, "italic"),
    (660, 862, "Bannerfall", 12, "italic"),
    (452, 856, "Firebase Delphi", 12, "italic"),
    (1014, 612, "Winding Cove", 12, "italic"),
    (1300, 524, "Liming Harbor", 12, "italic"),
    (1062, 852, "Sorrow's Harbor", 12, "italic"),
    (1224, 856, "Circle of Bones", 11, "italic"),
    (1078, 402, "Archer's Line", 12, "italic"),
    (1222, 288, "Skywatch", 12, "italic"),
    (1150, 380, "Anchor of Light", 12, "italic"),
    (792, 392, "Divalian Mists", 11, "italic"),
    (948, 508, "Spine of Keres", 11, "italic"),
    (884, 728, "Cadmus Ridge", 12, "italic"),
    (772, 762, "Firebase Rubicon", 12, "italic"),
    (932, 282, "Watcher's Grave", 12, "italic"),
    (1216, 548, "Dark Forest", 12, "italic"),
    (1004, 884, "Miasma", 12, "italic"),
    (1088, 934, "Weeping Well", 12, "italic"),
]
for x, y, *_ in MINOR:
    EXCL.append((x, y, 46))

def blocked(p):
    for cx, cy, r in EXCL:
        if (p[0] - cx) ** 2 + (p[1] - cy) ** 2 < r * r:
            return True
    return False

def scatter(cx, cy, rx, ry, n, poly=LAND, jitter=True, tries=None):
    pts = []
    tries = tries or n * 30
    for _ in range(tries):
        if len(pts) >= n:
            break
        a = random.uniform(0, math.tau)
        r = math.sqrt(random.uniform(0, 1))
        p = (cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r)
        if not inside(p, poly) or blocked(p):
            continue
        if any((p[0]-q[0])**2 + (p[1]-q[1])**2 < 460 for q in pts):
            continue
        pts.append(p)
    return pts

# ---------------------------------------------------------------- svg head
e(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
  f'height="{H}" font-family="\'Iowan Old Style\',\'Palatino Linotype\',Palatino,'
  f'\'Book Antiqua\',Georgia,serif">')

e(f'''<defs>
<radialGradient id="seaG" cx="50%" cy="42%" r="72%">
  <stop offset="0%" stop-color="{C['sea2']}"/><stop offset="100%" stop-color="{C['void']}"/>
</radialGradient>
<radialGradient id="landG" cx="46%" cy="36%" r="70%">
  <stop offset="0%" stop-color="{C['land_hi']}"/><stop offset="100%" stop-color="{C['land']}"/>
</radialGradient>
<radialGradient id="dawnG" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="#eaf6ff" stop-opacity=".50"/>
  <stop offset="45%" stop-color="#9fd8e8" stop-opacity=".16"/>
  <stop offset="100%" stop-color="#9fd8e8" stop-opacity="0"/>
</radialGradient>
<radialGradient id="emberField" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="#C4562F" stop-opacity=".20"/>
  <stop offset="55%" stop-color="#7A2B1C" stop-opacity=".09"/>
  <stop offset="100%" stop-color="#7A2B1C" stop-opacity="0"/>
</radialGradient>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" seed="7"/>
  <feColorMatrix type="saturate" values="0"/></filter>
<filter id="soft"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="soft2"><feGaussianBlur stdDeviation="2.2"/></filter>
<clipPath id="landClip"><path d="{path_of(LAND)}"/></clipPath>
<clipPath id="plateClip"><rect x="{MAP['x0']}" y="{MAP['y0']}" width="{MAP['x1']-MAP['x0']}" height="{MAP['y1']-MAP['y0']}"/></clipPath>
<g id="mtn"><path d="M -19 0 L -6 -17 L 2 -8 L 9 -21 L 20 0" fill="none" stroke="{C['ink']}" stroke-width="1.5" stroke-linejoin="round"/>
  <path d="M -6 -17 L -10 -7 M 9 -21 L 5 -9" stroke="{C['ink_soft']}" stroke-width="1"/></g>
<g id="hill"><path d="M -13 0 Q -6 -10 0 -10 Q 7 -10 13 0" fill="none" stroke="{C['ink_soft']}" stroke-width="1.3"/></g>
<g id="tree"><path d="M 0 0 L 0 -6" stroke="{C['ink_soft']}" stroke-width="1"/>
  <path d="M -6 -5 L 0 -17 L 6 -5 Z" fill="none" stroke="{C['ink']}" stroke-width="1.1"/></g>
<g id="dead"><path d="M 0 0 L 0 -13 M 0 -9 L -6 -15 M 0 -6 L 6 -12" stroke="{C['ink_soft']}" stroke-width="1.1" fill="none"/></g>
<g id="marsh"><path d="M -9 0 h 18 M -6 -5 h 12 M -3 -10 h 6" stroke="{C['ink_soft']}" stroke-width="1.1"/></g>
<g id="ruin"><path d="M -7 0 v -8 h 3 v 8 M 1 0 v -12 h 4 v 12" fill="none" stroke="{C['ink_soft']}" stroke-width="1.2"/></g>
</defs>''')

# ---------------------------------------------------------------- plate
e(f'<rect width="{W}" height="{H}" fill="{C["void"]}"/>')
e(f'<g clip-path="url(#plateClip)">')
e(f'<rect x="{MAP["x0"]}" y="{MAP["y0"]}" width="{MAP["x1"]-MAP["x0"]}" '
  f'height="{MAP["y1"]-MAP["y0"]}" fill="url(#seaG)"/>')

# sea hatching (latitude lines)
for y in range(MAP["y0"] + 30, MAP["y1"], 34):
    e(f'<line x1="{MAP["x0"]}" y1="{y}" x2="{MAP["x1"]}" y2="{y}" stroke="#1a2733" '
      f'stroke-width="0.6" opacity=".38"/>')

# ---------------------------------------------------------------- land
for poly in (LAND, ISLE):
    e(f'<path d="{path_of(poly)}" fill="#000" opacity=".55" filter="url(#soft)" transform="translate(5,7)"/>')
    e(f'<path d="{path_of(poly)}" fill="url(#landG)" stroke="{C["coast"]}" stroke-width="1.9"/>')
    # coastal fringe
    for k, o in ((6, .30), (12, .18), (19, .09)):
        e(f'<path d="{path_of(poly)}" fill="none" stroke="{C["coast"]}" stroke-width="1" '
          f'opacity="{o}" transform="translate({-k*0.14:.1f},{-k*0.10:.1f}) scale(1)" />')

e(f'<g clip-path="url(#landClip)"><rect x="0" y="0" width="{W}" height="{H}" '
  f'filter="url(#grain)" opacity=".095"/></g>')

# ---------------------------------------------------------------- terrain
e('<g id="terrain">')
ranges = [
    (1150, 320, 130, 78, 16),   # Endless Steps / Felwinter
    (1040, 300, 90, 45, 8),
    (950, 510, 130, 40, 10),    # Spine of Keres
    (620, 508, 110, 42, 9),     # Twilight Gap — the north wall
    (556, 634, 108, 40, 8),     # Twilight Gap — the south wall
    (1230, 720, 90, 70, 7),
    (300, 470, 90, 60, 7),
]
for cx, cy, rx, ry, n in ranges:
    for x, y in scatter(cx, cy, rx, ry, n):
        s = random.uniform(0.85, 1.35)
        e(f'<use href="#mtn" transform="translate({x:.0f},{y:.0f}) scale({s:.2f})"/>')

hills = [(430, 620, 120, 70, 9), (760, 620, 130, 60, 9), (1060, 640, 110, 60, 8),
         (700, 880, 120, 60, 8), (250, 830, 90, 70, 6)]
for cx, cy, rx, ry, n in hills:
    for x, y in scatter(cx, cy, rx, ry, n):
        e(f'<use href="#hill" transform="translate({x:.0f},{y:.0f}) scale({random.uniform(.8,1.2):.2f})"/>')

forests = [(300, 320, 110, 60, 14), (930, 285, 95, 50, 12), (1215, 555, 85, 60, 11),
           (830, 560, 70, 45, 7)]
for cx, cy, rx, ry, n in forests:
    for x, y in scatter(cx, cy, rx, ry, n):
        e(f'<use href="#tree" transform="translate({x:.0f},{y:.0f}) scale({random.uniform(.8,1.15):.2f})"/>')

for x, y in scatter(430, 400, 130, 70, 14):   # Mothyards: dead orchard
    e(f'<use href="#dead" transform="translate({x:.0f},{y:.0f}) scale({random.uniform(.8,1.2):.2f})"/>')

for x, y in scatter(1040, 890, 130, 60, 10):  # Sludge / Quagmire
    e(f'<use href="#marsh" transform="translate({x:.0f},{y:.0f}) scale({random.uniform(.8,1.2):.2f})"/>')

for x, y in scatter(690, 780, 150, 90, 9):    # Rusted Lands ruins
    e(f'<use href="#ruin" transform="translate({x:.0f},{y:.0f}) scale({random.uniform(.9,1.3):.2f})"/>')
e('</g>')

# an ember low on the plate — the same glow the invitation carries
e(f'<ellipse cx="{(MAP["x0"]+MAP["x1"])/2:.0f}" cy="{MAP["y1"]+30}" rx="640" ry="330" '
  f'fill="url(#emberField)"/>')

# ---------------------------------------------------------------- rivers
def river(pts, w=1.6):
    d = "M " + f"{pts[0][0]} {pts[0][1]}"
    for i in range(1, len(pts) - 1):
        mx = (pts[i][0] + pts[i+1][0]) / 2
        my = (pts[i][1] + pts[i+1][1]) / 2
        d += f" Q {pts[i][0]} {pts[i][1]} {mx} {my}"
    d += f" T {pts[-1][0]} {pts[-1][1]}"
    e(f'<path d="{d}" fill="none" stroke="#4d6a7d" stroke-width="{w}" opacity=".75"/>')

river([(870, 250), (845, 350), (880, 460), (826, 570), (790, 690), (772, 800), (800, 900), (842, 1000)], 2.0)
river([(300, 300), (360, 400), (400, 520), (370, 640), (300, 760), (250, 900)], 1.5)
river([(1290, 300), (1230, 400), (1240, 520), (1180, 640), (1200, 760), (1250, 880)], 1.5)
river([(600, 560), (680, 640), (700, 760), (640, 870), (600, 980)], 1.4)

# ---------------------------------------------------------------- roads
def road(pts, dash="7 7", col=None, w=1.5, op=.7):
    col = col or C["ink_soft"]
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
    e(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" '
      f'stroke-dasharray="{dash}" opacity="{op}" stroke-linecap="round"/>')

road([(322,462),(430,500),(508,520),(600,545)])
road([(600,545),(690,600),(752,650),(820,540),(855,470)])
road([(752,664),(700,780),(660,850),(560,928)])
road([(560,928),(470,868)])
road([(855,440),(960,400),(1050,380),(1122,342)])
road([(855,470),(950,540),(1014,612),(1100,700),(1152,792)])
road([(855,440),(1010,470),(1160,500),(1300,524)])
road([(1250,524),(1312,556),(1358,594)], dash="4 9", col="#4d6a7d")
road([(1062,852),(1152,792)])

# ---------------------------------------------------------------- overlays
# 2. the famine front — advancing out of the northwest
front = [(150,196),(270,300),(330,420),(420,520),(470,640),(430,760),(360,880)]
d = "M " + " ".join(f"{x} {y}" for x, y in front[:1]) + " " + \
    " ".join(f"L {x} {y}" for x, y in front[1:])
e(f'<path d="{d}" fill="none" stroke="{C["frost"]}" stroke-width="2.4" '
  f'stroke-dasharray="14 8" opacity=".75"/>')
for i in range(len(front) - 1):
    x1, y1 = front[i]; x2, y2 = front[i + 1]
    for t in (0.25, 0.6, 0.9):
        px, py = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        e(f'<path d="M 0 0 L 13 0" stroke="{C["frost"]}" stroke-width="1.6" opacity=".55" '
          f'transform="translate({px:.0f},{py:.0f}) rotate({ang+90:.0f})"/>')
e(f'<path d="{d}" fill="none" stroke="{C["frost"]}" stroke-width="76" opacity=".05" '
  f'filter="url(#soft)" stroke-linejoin="round"/>')

# 4. war fever
def blades(x, y, s=1.0, op=.8):
    e(f'<g transform="translate({x},{y}) scale({s})" opacity="{op}" stroke="{C["war"]}" '
      f'stroke-width="1.8" fill="none" stroke-linecap="round">'
      f'<path d="M -9 -9 L 9 9 M 9 -9 L -9 9"/>'
      f'<path d="M -12 -6 L -6 -12 M 12 -6 L 6 -12"/></g>')
for bx, by, bs in ((600,545,1.25),(560,928,1.35),(660,862,.9),(452,856,.85),
                   (700,700,.8),(500,980,.75),(760,900,.7)):
    blades(bx, by, bs)

# 5. glows
e(f'<ellipse cx="1122" cy="342" rx="150" ry="120" fill="url(#dawnG)"/>')

# ---------------------------------------------------------------- the Hellas Basin / Pale Heart
e(f'<g opacity=".85">')
for r in (150, 120, 92):
    e(f'<ellipse cx="{HEART[0]}" cy="{HEART[1]}" rx="{r}" ry="{r*0.72:.0f}" fill="none" '
      f'stroke="{C["ink_soft"]}" stroke-width="1" stroke-dasharray="2 6" opacity=".55"/>')
for i in range(36):
    a = math.tau * i / 36
    x1 = HEART[0] + math.cos(a) * 150; y1 = HEART[1] + math.sin(a) * 108
    x2 = HEART[0] + math.cos(a) * 136; y2 = HEART[1] + math.sin(a) * 98
    e(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{C["ink_soft"]}" '
      f'stroke-width="1" opacity=".5"/>')
e('</g>')

# ---------------------------------------------------------------- star-fall streaks (signature)
e('<g id="fall">')
for (_, sx, sy, *_ ) in SITES:
    L = random.uniform(150, 215)
    ex_, ey = sx + random.uniform(-40, 40), sy - L
    e(f'<line x1="{sx}" y1="{sy}" x2="{ex_:.0f}" y2="{ey:.0f}" stroke="{C["gold"]}" '
      f'stroke-width="1.3" opacity=".11" stroke-linecap="round"/>')
e('</g>')

# ---------------------------------------------------------------- water labels
txt(640, 150, "Ocean of Storms", 19, "#4f6b7e", ls=5, style="italic", op=.9)
txt(1398, 300, "Ecliptic Drift", 15, "#4f6b7e", ls=3, style="italic", op=.9, rot=90)
txt(880, 1090, "Shores of Time", 18, "#4f6b7e", ls=5, style="italic", op=.9)
txt(300, 1090, "Sunken Isles", 14, "#4f6b7e", ls=3, style="italic", op=.75)
for ix, iy, ir in ((360,1046,9),(408,1064,6),(452,1040,7),(300,1058,5)):
    e(f'<ellipse cx="{ix}" cy="{iy}" rx="{ir}" ry="{ir*0.6:.0f}" fill="{C["land"]}" '
      f'stroke="{C["coast"]}" stroke-width="1" opacity=".85"/>')

# ---------------------------------------------------------------- region labels
REGIONS = [
    (330, 560, "STEPPES", 22, 0),
    (986, 202, "ENDLESS STEPS", 16, -7),
    (700, 616, "RUSTED LANDS", 18, -3),
    (286, 790, "VALLEY OF THE KINGS", 17, 0),
    (1006, 786, "HELLAS BASIN", 16, 0),
    (1176, 690, "DEEP COUNTRY", 16, 8),
    (240, 232, "FORGOTTEN SHORE", 14, -14),
    (296, 322, "INFINITE FOREST", 14, 0),
    (742, 978, "UNFINISHED FIELD", 14, -3),
]
for x, y, s, size, rot in REGIONS:
    txt(x, y, s, size, C["text_dim"], ls=6, op=.42, rot=rot)

for x, y, s, size, style in MINOR:
    txt(x, y, s, size, C["text_dim"], ls=.5, style=style, op=.82)


# ---------------------------------------------------------------- site markers
def sword(x, y, s=1.0, col=None):
    col = col or C["gold"]
    e(f'<g transform="translate({x},{y}) scale({s})">'
      f'<circle r="30" fill="{col}" opacity=".10" filter="url(#soft2)"/>'
      f'<path d="M 0 6 L 0 -30" stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>'
      f'<path d="M -11 -22 L 11 -22" stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>'
      f'<circle cy="-34" r="3.4" fill="none" stroke="{col}" stroke-width="2.2"/>'
      f'<path d="M -13 7 Q 0 13 13 7" fill="none" stroke="{col}" stroke-width="1.5" opacity=".8"/>'
      f'</g>')

for num, x, y, name, blade, ch in SITES:
    sword(x, y)
    if x > 1300:                      # label inboard, not off the plate edge
        txt(x - 34, y + 2, name, 15, C["gold"], ls=2.2, upper=True, anchor="end")
        txt(x - 34, y + 19, blade, 11.5, C["gold_dim"], ls=1.4, style="italic", anchor="end")
    else:
        txt(x, y + 34, name, 15, C["gold"], ls=2.2, upper=True)
        txt(x, y + 51, blade, 11.5, C["gold_dim"], ls=1.4, style="italic")

# Kavzar tower glyph
e(f'<path d="M 838 424 L 846 380 L 856 378 L 862 424 Z" fill="{C["void"]}" stroke="{C["toll"]}" '
  f'stroke-width="1.4" opacity=".9" transform="rotate(-9 850 400)"/>')

# ---------------------------------------------------------------- compass
cxc, cyc = 1130, 1052
e(f'<g transform="translate({cxc},{cyc})" opacity=".8">'
  f'<circle r="42" fill="none" stroke="{C["ink_soft"]}" stroke-width="1"/>'
  f'<circle r="31" fill="none" stroke="{C["ink_soft"]}" stroke-width=".7" stroke-dasharray="2 5"/>'
  f'<path d="M 0 -40 L 8 0 L 0 40 L -8 0 Z" fill="{C["ink_soft"]}" opacity=".35"/>'
  f'<path d="M 0 -40 L 8 0 L -8 0 Z" fill="{C["gold"]}" opacity=".8"/>'
  f'<path d="M -40 0 L 0 -7 L 40 0 L 0 7 Z" fill="{C["ink_soft"]}" opacity=".28"/></g>')
txt(cxc, cyc - 50, "N", 13, C["gold"], ls=1)

e('</g>')  # end plate clip

# map frame
e(f'<rect x="{MAP["x0"]}" y="{MAP["y0"]}" width="{MAP["x1"]-MAP["x0"]}" '
  f'height="{MAP["y1"]-MAP["y0"]}" fill="none" stroke="{C["gold_dim"]}" stroke-width="2"/>')
e(f'<rect x="{MAP["x0"]+7}" y="{MAP["y0"]+7}" width="{MAP["x1"]-MAP["x0"]-14}" '
  f'height="{MAP["y1"]-MAP["y0"]-14}" fill="none" stroke="{C["gold_dim"]}" stroke-width="0.8" opacity=".6"/>')

# ---------------------------------------------------------------- legend rail
rx0, ry0, rx1 = RAIL["x0"], RAIL["y0"], RAIL["x1"]
midr = (rx0 + rx1) / 2
e(f'<rect x="{rx0}" y="{ry0}" width="{rx1-rx0}" height="{RAIL["y1"]-ry0}" fill="#0b1016" '
  f'stroke="{C["gold_dim"]}" stroke-width="1.4"/>')

y = ry0 + 44
txt(midr, y, "THE ABSENT FLAME", 10.5, C["text_dim"], ls=3.6, upper=True); y += 32
txt(midr, y, "ELEUSINA", 34, C["text"], ls=6); y += 23
txt(midr, y, "a world map", 12, C["gold_dim"], ls=4, style="italic", upper=True); y += 20
e(f'<line x1="{rx0+26}" y1="{y}" x2="{rx1-26}" y2="{y}" stroke="{C["gold_dim"]}" stroke-width="1"/>')
y += 30
txt(midr, y, "Drawn the spring after the sky failed,", 12.5, C["text_dim"], style="italic"); y += 17
txt(midr, y, "from the accounts of people who walked it.", 12.5, C["text_dim"], style="italic"); y += 34

txt(midr, y, "WHERE THE STARS FELL", 13, C["ember"], ls=3); y += 8
e(f'<line x1="{rx0+26}" y1="{y}" x2="{rx1-26}" y2="{y}" stroke="{C["gold_dim"]}" stroke-width=".7" opacity=".6"/>')
y += 24

txt(midr, y + 14, "no order implied", 11, C["text_dim"], style="italic", ls=1.5)
y += 34

ENTRIES = [
    ("Twilight Gap",        "the Ember"),
    ("Felwinter Peak",      "the Dawn"),
    ("Hellmouth",       "the Vigil"),
    ("Dust Palace",     "the Feast"),
    ("Six Fronts",          "the Truce"),
    ("Kavzar",              "the Hush"),
    ("Harbinger's Seclude", "the Solitude"),
]
for place, blade in ENTRIES:
    gx, gy = rx0 + 40, y - 4
    e(f'<g transform="translate({gx},{gy}) scale(.42)" opacity=".92">'
      f'<path d="M 0 8 L 0 -26" stroke="{C["gold"]}" stroke-width="4.4" stroke-linecap="round"/>'
      f'<path d="M -11 -19 L 11 -19" stroke="{C["gold"]}" stroke-width="4.4" stroke-linecap="round"/>'
      f'</g>')
    txt(rx0 + 62, y - 5, place, 14, C["text"], anchor="start", ls=.4)
    txt(rx0 + 62, y + 11, blade, 11, C["gold_dim"], anchor="start", style="italic")
    y += 33

y += 6
txt(midr, y, "WHAT THE ROADS REPORT", 13, C["ember"], ls=3); y += 8
e(f'<line x1="{rx0+26}" y1="{y}" x2="{rx1-26}" y2="{y}" stroke="{C["gold_dim"]}" stroke-width=".7" opacity=".6"/>')
y += 28

def key(sym_fn, label, sub):
    global y
    sym_fn(rx0 + 42, y - 4)
    txt(rx0 + 66, y - 3, label, 13, C["text"], anchor="start", ls=.4)
    txt(rx0 + 66, y + 12, sub, 10.2, C["text_dim"], anchor="start", style="italic")
    y += 34

key(lambda x, yy: e(f'<line x1="{x-14}" y1="{yy}" x2="{x+14}" y2="{yy}" stroke="{C["frost"]}" '
                    f'stroke-width="2.2" stroke-dasharray="8 5"/>'),
    "Frost line", "cold that came with the dark, and stayed")
key(lambda x, yy: blades(x, yy, .8, .9),
    "Fever", "old grudges reigniting for no reason at all")
key(lambda x, yy: e(f'<line x1="{x-14}" y1="{yy}" x2="{x+14}" y2="{yy}" stroke="{C["ink_soft"]}" '
                    f'stroke-width="1.6" stroke-dasharray="6 6"/>'),
    "Roads", "where a line stops, so did whoever reported it")
key(lambda x, yy: e(f'<line x1="{x-14}" y1="{yy}" x2="{x+14}" y2="{yy}" stroke="#4d6a7d" '
                    f'stroke-width="1.6" stroke-dasharray="3 8"/>'),
    "Sea route", "Liming Harbor is the last port still chartering")


# the prophecy block
y = RAIL["y1"] - 330
e(f'<line x1="{rx0+26}" y1="{y}" x2="{rx1-26}" y2="{y}" stroke="{C["gold_dim"]}" stroke-width=".7" opacity=".6"/>')
y += 34
for line, size, style in (
    ("Find the seven.", 17, "italic"),
    ("Before the four.", 17, "italic"),
    ("", 8, "italic"),
    ("Four to bind, three to heal —", 13, "italic"),
    ("the healing does not bind,", 13, "italic"),
    ("and the binding does not heal.", 13, "italic"),
):
    if line:
        txt(midr, y, line, size, C["ash"], style=style, op=.9)
    y += size + 9
y += 6
txt(midr, y, "read from a finger-bone at Twilight Gap,", 10.5, C["text_dim"], style="italic")
y += 15
txt(midr, y, "the night the sky failed", 10.5, C["text_dim"], style="italic")

# scale bar
y = RAIL["y1"] - 96
e(f'<line x1="{rx0+30}" y1="{y}" x2="{rx1-30}" y2="{y}" stroke="{C["gold_dim"]}" stroke-width=".7" opacity=".6"/>')
y += 34
bx, bw = rx0 + 40, 190
e(f'<rect x="{bx}" y="{y-9}" width="{bw/2}" height="9" fill="{C["text_dim"]}" opacity=".8"/>')
e(f'<rect x="{bx+bw/2}" y="{y-9}" width="{bw/2}" height="9" fill="none" stroke="{C["text_dim"]}" stroke-width="1"/>')
txt(bx, y + 15, "0", 10, C["text_dim"], anchor="middle")
txt(bx + bw, y + 15, "100 leagues", 10, C["text_dim"], anchor="middle")
txt(bx + bw / 2, y - 16, "twelve days' march, in the old light", 10.5, C["text_dim"], style="italic")

e('</svg>')

svg = "\n".join(out)
with open("/mnt/user-data/outputs/absent-flame-world-map.svg", "w") as f:
    f.write(svg)
print("bytes:", len(svg))
