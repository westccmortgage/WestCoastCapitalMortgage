#!/usr/bin/env python3
"""
Generate the California Mortgage social/hero poster as a PNG (no deps).

Output: ../californiamtg/public/images/california_mortgage_poster.png
- 1200x630 (Open Graph / Twitter card size; also the hero poster fallback)
- warm sand -> stone gradient with the bronze roofline mark
Run: python3 tools/make_og_poster.py
"""
import os, zlib, struct, math

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(__file__), "..", "californiamtg", "public", "images", "california_mortgage_poster.png")

def lerp(a, b, t): return a + (b - a) * t
def mix(c1, c2, t): return tuple(int(round(lerp(c1[i], c2[i], t))) for i in range(3))

IVORY = (0xFB, 0xF8, 0xF2)
SAND  = (0xEC, 0xE2, 0xD2)
TAUPE = (0xD8, 0xCB, 0xB6)
BRONZE = (0x8A, 0x6A, 0x37)
CHARCOAL = (0x2C, 0x27, 0x22)

# pixel buffer
buf = bytearray(W * H * 3)
def setpx(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = c[0]; buf[i+1] = c[1]; buf[i+2] = c[2]

# warm diagonal gradient
for y in range(H):
    for x in range(W):
        t = (x / W) * 0.45 + (y / H) * 0.55
        if t < 0.5:
            c = mix(IVORY, SAND, t / 0.5)
        else:
            c = mix(SAND, TAUPE, (t - 0.5) / 0.5)
        i = (y * W + x) * 3
        buf[i] = c[0]; buf[i+1] = c[1]; buf[i+2] = c[2]

# soft warm glow top-right
for y in range(H):
    for x in range(W):
        dx = (x - W * 0.8); dy = (y - H * 0.18)
        d = math.sqrt(dx * dx + dy * dy)
        g = max(0.0, 1.0 - d / (W * 0.5)) * 0.10
        if g > 0:
            i = (y * W + x) * 3
            buf[i]   = min(255, int(buf[i]   + (205 - buf[i])   * g))
            buf[i+1] = min(255, int(buf[i+1] + (175 - buf[i+1]) * g))
            buf[i+2] = min(255, int(buf[i+2] + (120 - buf[i+2]) * g))

def thick_line(p0, p1, color, width):
    (x0, y0), (x1, y1) = p0, p1
    minx = int(min(x0, x1) - width); maxx = int(max(x0, x1) + width)
    miny = int(min(y0, y1) - width); maxy = int(max(y0, y1) + width)
    vx, vy = x1 - x0, y1 - y0
    seg2 = vx * vx + vy * vy or 1
    r = width / 2.0
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            t = ((x - x0) * vx + (y - y0) * vy) / seg2
            t = max(0.0, min(1.0, t))
            px, py = x0 + t * vx, y0 + t * vy
            d = math.hypot(x - px, y - py)
            if d <= r:
                setpx(x, y, color)

def fill_rect(x0, y0, x1, y1, color):
    for y in range(int(y0), int(y1)):
        for x in range(int(x0), int(x1)):
            setpx(x, y, color)

# Roofline mark, centered, scaled from the 64-unit favicon grid
s = 7.0
ox = W / 2 - 32 * s
oy = H / 2 - 33 * s
def P(px, py): return (ox + px * s, oy + py * s)
# roof (bronze)
thick_line(P(14, 36), P(32, 18), BRONZE, 9)
thick_line(P(32, 18), P(50, 36), BRONZE, 9)
# house body (charcoal)
thick_line(P(20, 34), P(20, 48), CHARCOAL, 7)
thick_line(P(20, 48), P(44, 48), CHARCOAL, 7)
thick_line(P(44, 48), P(44, 34), CHARCOAL, 7)
# door (bronze)
fill_rect(P(29, 40)[0], P(29, 40)[1], P(35, 48)[0], P(35, 48)[1], BRONZE)

# encode PNG
raw = bytearray()
for y in range(H):
    raw.append(0)
    raw.extend(buf[y * W * 3:(y + 1) * W * 3])
comp = zlib.compress(bytes(raw), 9)

def chunk(typ, data):
    c = typ + data
    return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)

png = b"\x89PNG\r\n\x1a\n"
png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
png += chunk(b"IDAT", comp)
png += chunk(b"IEND", b"")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "wb") as f:
    f.write(png)
print("wrote", OUT, "(%d KB)" % (len(png) // 1024))
