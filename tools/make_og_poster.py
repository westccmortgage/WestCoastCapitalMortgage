#!/usr/bin/env python3
"""
Generate California Mortgage images (no deps):
  public/images/california_mortgage_poster.png  -> CLEAN warm gradient (hero <video>
        poster + mobile fallback). No centered icon, so nothing odd shows over the hero.
  public/images/california_mortgage_og.png       -> branded share image (gradient +
        bronze roofline mark) for Open Graph / Twitter cards.
Run: python3 tools/make_og_poster.py
"""
import os, zlib, struct, math

W, H = 1200, 630
IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "californiamtg", "public", "images")

IVORY = (0xFB, 0xF8, 0xF2); SAND = (0xEC, 0xE2, 0xD2); TAUPE = (0xD8, 0xCB, 0xB6)
BRONZE = (0x8A, 0x6A, 0x37); CHARCOAL = (0x2C, 0x27, 0x22)

def lerp(a, b, t): return a + (b - a) * t
def mix(c1, c2, t): return tuple(int(round(lerp(c1[i], c2[i], t))) for i in range(3))

def base_gradient():
    buf = bytearray(W * H * 3)
    for y in range(H):
        for x in range(W):
            t = (x / W) * 0.45 + (y / H) * 0.55
            c = mix(IVORY, SAND, t / 0.5) if t < 0.5 else mix(SAND, TAUPE, (t - 0.5) / 0.5)
            i = (y * W + x) * 3
            buf[i], buf[i+1], buf[i+2] = c
    # soft warm glow top-right
    for y in range(H):
        for x in range(W):
            d = math.hypot(x - W * 0.8, y - H * 0.18)
            g = max(0.0, 1.0 - d / (W * 0.5)) * 0.10
            if g > 0:
                i = (y * W + x) * 3
                buf[i]   = min(255, int(buf[i]   + (205 - buf[i])   * g))
                buf[i+1] = min(255, int(buf[i+1] + (175 - buf[i+1]) * g))
                buf[i+2] = min(255, int(buf[i+2] + (120 - buf[i+2]) * g))
    return buf

def setpx(buf, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3; buf[i], buf[i+1], buf[i+2] = c

def thick_line(buf, p0, p1, color, width):
    (x0, y0), (x1, y1) = p0, p1
    vx, vy = x1 - x0, y1 - y0; seg2 = vx * vx + vy * vy or 1; r = width / 2.0
    for y in range(int(min(y0, y1) - width), int(max(y0, y1) + width) + 1):
        for x in range(int(min(x0, x1) - width), int(max(x0, x1) + width) + 1):
            t = max(0.0, min(1.0, ((x - x0) * vx + (y - y0) * vy) / seg2))
            if math.hypot(x - (x0 + t * vx), y - (y0 + t * vy)) <= r:
                setpx(buf, x, y, color)

def fill_rect(buf, x0, y0, x1, y1, color):
    for y in range(int(y0), int(y1)):
        for x in range(int(x0), int(x1)):
            setpx(buf, x, y, color)

def draw_mark(buf):
    s = 7.0; ox = W / 2 - 32 * s; oy = H / 2 - 33 * s
    P = lambda px, py: (ox + px * s, oy + py * s)
    thick_line(buf, P(14, 36), P(32, 18), BRONZE, 9)
    thick_line(buf, P(32, 18), P(50, 36), BRONZE, 9)
    thick_line(buf, P(20, 34), P(20, 48), CHARCOAL, 7)
    thick_line(buf, P(20, 48), P(44, 48), CHARCOAL, 7)
    thick_line(buf, P(44, 48), P(44, 34), CHARCOAL, 7)
    fill_rect(buf, P(29, 40)[0], P(29, 40)[1], P(35, 48)[0], P(35, 48)[1], BRONZE)

def write_png(path, buf):
    raw = bytearray()
    for y in range(H):
        raw.append(0); raw.extend(buf[y * W * 3:(y + 1) * W * 3])
    comp = zlib.compress(bytes(raw), 9)
    def chunk(typ, data):
        c = typ + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", comp) + chunk(b"IEND", b""))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)
    print("wrote", os.path.basename(path), "(%d KB)" % (len(png) // 1024))

if __name__ == "__main__":
    base = base_gradient()
    write_png(os.path.join(IMG_DIR, "california_mortgage_poster.png"), bytes(base))  # clean, no icon
    og = bytearray(base); draw_mark(og)
    write_png(os.path.join(IMG_DIR, "california_mortgage_og.png"), og)               # branded share image
