#!/usr/bin/env python3
"""Generates the animated LEO//OS SVGs for the GitHub profile README (assets/*.svg).

Everything animates with CSS keyframes or SMIL inside the SVG itself, so it plays on
github.com with no external service. Palette: leolennards.vercel.app.
"""
import math
import os
from html import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

VOID, PANEL, PANEL2 = "#04060a", "#0a0f16", "#0e151f"
LINE, LINEB, FAINT, DIM, INK = "#18222f", "#253345", "#4d5b6c", "#8b98a8", "#e6edf3"
SIGNAL, ICE, VIOLET, AMBER, ALERT, TEAL = "#3dff9a", "#6cc7ff", "#b18cff", "#ffb547", "#ff5f6d", "#4fe3cf"
MONO = "'JetBrains Mono','SFMono-Regular',ui-monospace,Menlo,Consolas,'Liberation Mono',monospace"

BASE_CSS = f"""
  text {{ font-family: {MONO}; }}
  .fade {{ animation: fade .5s ease both; }}
  @keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  .rise {{ animation: rise .6s cubic-bezier(.2,.8,.2,1) both; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
  .pulse {{ animation: pulse 2s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
  .ring {{ animation: ring 2s ease-out infinite; transform-box: fill-box; transform-origin: center; }}
  @keyframes ring {{ from {{ opacity: .7; transform: scale(1); }} to {{ opacity: 0; transform: scale(3.2); }} }}
  .blink {{ animation: blink 1.05s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""


def svg(w, h, body, css="", title=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<style>{BASE_CSS}{css}</style>
{body}
</svg>
"""


def frame(w, h, r=14):
    """Card background: void panel, grid, corner glows, border, HUD corner ticks."""
    t = 14
    ticks = "".join(
        f'<path d="M{x} {y + dy * t} V{y} H{x + dx * t}" stroke="{FAINT}" stroke-width="2" fill="none"/>'
        for x, y, dx, dy in [(10, 10, 1, 1), (w - 10, 10, -1, 1), (10, h - 10, 1, -1), (w - 10, h - 10, -1, -1)]
    )
    return f"""
<defs>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" fill="none" stroke="{LINE}" stroke-width="1" opacity=".55"/>
    <animateTransform attributeName="patternTransform" type="translate" from="0 0" to="32 32" dur="12s" repeatCount="indefinite"/>
  </pattern>
  <radialGradient id="glowA" cx="0" cy="1" r="0.9"><stop offset="0" stop-color="{SIGNAL}" stop-opacity=".13"/><stop offset="1" stop-color="{SIGNAL}" stop-opacity="0"/></radialGradient>
  <radialGradient id="glowB" cx="1" cy="0" r="0.9"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".13"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <clipPath id="card"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="{VOID}"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
  <rect width="{w}" height="{h}" fill="url(#glowA)"/>
  <rect width="{w}" height="{h}" fill="url(#glowB)"/>
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{r}" fill="none" stroke="{LINEB}"/>
{ticks}
"""


def ok_line(x, y, verb, what, delay, size=15):
    return (f'<g class="fade" style="animation-delay:{delay:.2f}s">'
            f'<text x="{x}" y="{y}" font-size="{size}"><tspan fill="{LINEB}">[</tspan><tspan fill="{SIGNAL}">  OK  </tspan>'
            f'<tspan fill="{LINEB}">]</tspan><tspan fill="{FAINT}"> {escape(verb):<9}</tspan><tspan fill="{DIM}" xml:space="preserve"> {escape(what)}</tspan></text></g>')


# ── header ──────────────────────────────────────────────────────────────
def header():
    w, h = 1280, 420
    boot = [("started", "identity.service"), ("started", "network.target · online · CPT"),
            ("verified", "mfa.challenge"), ("reached", "target leo-os.profile")]
    lines = "".join(ok_line(56, 64 + i * 24, v, x, 0.25 + i * 0.35) for i, (v, x) in enumerate(boot))

    cx, cy, r = 1040, 214, 150
    wedges = "".join(
        f'<path d="M{cx} {cy} L{cx + r * math.cos(math.radians(-a)):.1f} {cy + r * math.sin(math.radians(-a)):.1f} '
        f'A{r} {r} 0 0 1 {cx + r * math.cos(math.radians(-a + 4)):.1f} {cy + r * math.sin(math.radians(-a + 4)):.1f} Z" '
        f'fill="{SIGNAL}" opacity="{0.32 * (1 - i / 16) ** 2:.3f}"/>'
        for i, a in enumerate(range(0, 64, 4)))
    rings = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r * k:.0f}" fill="none" stroke="{LINEB if k == 1 else LINE}" stroke-width="{1.5 if k == 1 else 1}"/>'
                    for k in (1, .75, .5, .25))
    ticks = "".join(
        f'<line x1="{cx + math.cos(math.radians(d)) * r * (0.9 if d % 30 == 0 else 0.95):.1f}" y1="{cy + math.sin(math.radians(d)) * r * (0.9 if d % 30 == 0 else 0.95):.1f}" '
        f'x2="{cx + math.cos(math.radians(d)) * r:.1f}" y2="{cy + math.sin(math.radians(d)) * r:.1f}" stroke="{FAINT if d % 30 == 0 else LINEB}"/>'
        for d in range(0, 360, 10))
    period = 4.0
    blips = ""
    for ang, dist, col in [(35, .62, SIGNAL), (110, .4, ICE), (200, .75, VIOLET), (260, .5, ICE), (320, .82, AMBER)]:
        x, y = cx + math.cos(math.radians(ang)) * r * dist, cy + math.sin(math.radians(ang)) * r * dist
        begin = (ang / 360) * period  # the beam turns clockwise from 0°: lights up as it passes
        blips += (f'<g opacity="0"><animate attributeName="opacity" values="0;1;0" keyTimes="0;0.04;1" dur="{period}s" begin="{begin:.2f}s" repeatCount="indefinite"/>'
                  f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="{col}" opacity=".18"/><circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{col}"/></g>')
    radar = f"""
<g class="fade" style="animation-delay:.3s">
  {rings}
  <line x1="{cx - r - 14}" y1="{cy}" x2="{cx + r + 14}" y2="{cy}" stroke="{LINE}"/>
  <line x1="{cx}" y1="{cy - r - 14}" x2="{cx}" y2="{cy + r + 14}" stroke="{LINE}"/>
  {ticks}
  <g>{wedges}<line x1="{cx}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="{SIGNAL}" stroke-width="2"/>
    <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{period}s" repeatCount="indefinite"/></g>
  {blips}
  <circle cx="{cx}" cy="{cy}" r="5" fill="{SIGNAL}"/>
  <text x="{cx + r}" y="{cy - r - 22}" font-size="13" text-anchor="end"><tspan fill="{SIGNAL}">cape-town.za</tspan><tspan fill="{SIGNAL}" class="pulse"> ●</tspan><tspan fill="{SIGNAL}"> online</tspan></text>
  <text x="{cx - r}" y="{cy + r + 36}" font-size="12.5" fill="{FAINT}">lat −33.89 · lon 18.56 · tz SAST (UTC+2)</text>
</g>"""

    tagline = "I keep businesses online, secure and moving."
    tw = (len(tagline) + 5) * 11.4  # "~$ " prefix + cursor, generous for fallback monospace fonts
    body = f"""{frame(w, h)}
<defs>
  <linearGradient id="shine" x1="-0.6" y1="0" x2="0" y2="0" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    <animate attributeName="x1" values="-0.6;1.4;1.4" keyTimes="0;.35;1" dur="7s" begin="2.2s" repeatCount="indefinite"/>
    <animate attributeName="x2" values="0;2;2" keyTimes="0;.35;1" dur="7s" begin="2.2s" repeatCount="indefinite"/>
  </linearGradient>
  <filter id="glow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="9"/></filter>
  <clipPath id="type"><rect x="56" y="282" height="30" width="{tw + 40:.0f}">
    <animate attributeName="width" dur="4.4s" begin="0s" fill="freeze" calcMode="discrete" values="{';'.join(['0'] * 30 + [str(int((tw + 40) * i / 35)) for i in range(36)])}"/></rect></clipPath>
</defs>
{lines}
<g class="glitch" style="animation-delay:1.5s">
  <text x="52" y="248" font-size="104" font-weight="800" letter-spacing="-2" filter="url(#glow)" opacity=".45"><tspan fill="{SIGNAL}">LEO</tspan><tspan fill="{VIOLET}">//</tspan><tspan fill="{ICE}">OS</tspan></text>
  <text x="52" y="248" font-size="104" font-weight="800" letter-spacing="-2"><tspan fill="{SIGNAL}">LEO</tspan><tspan fill="{VIOLET}">//</tspan><tspan fill="{ICE}">OS</tspan></text>
  <text x="52" y="248" font-size="104" font-weight="800" letter-spacing="-2" fill="url(#shine)">LEO//OS</text>
</g>
<text x="56" y="302" font-size="18" clip-path="url(#type)" xml:space="preserve"><tspan fill="{FAINT}">~$ </tspan><tspan fill="{DIM}">{escape(tagline)}</tspan><tspan fill="{SIGNAL}" class="blink">▌</tspan></text>
<g class="fade" style="animation-delay:4.4s">
  <circle cx="64" cy="340" r="6" fill="{SIGNAL}" class="ring"/><circle cx="64" cy="340" r="6" fill="{SIGNAL}"/>
  <text x="80" y="346" font-size="16"><tspan fill="{DIM}">STATUS: </tspan><tspan fill="{SIGNAL}" font-weight="700">ONLINE</tspan><tspan fill="{FAINT}">  ·  Leo Lennards  ·  IT Support &amp; Security  ·  Cape Town, ZA</tspan></text>
</g>
{radar}
"""
    css = """
  .glitch { animation: fade .6s ease both, glitch 9s steps(1) 3s infinite; }
  @keyframes glitch { 0%, 95%, 100% { transform: none; filter: none; }
    95.5% { transform: translate(4px,-2px) skewX(-8deg); filter: drop-shadow(-4px 0 #ff5f6d) drop-shadow(4px 0 #6cc7ff); }
    96.5% { transform: translate(-5px,1px); } 97.5% { transform: translate(2px,0) skewX(4deg); } }
"""
    return svg(w, h, body, css, "LEO//OS: Leo Lennards, IT Support & Security, Cape Town")


# ── whoami ──────────────────────────────────────────────────────────────
def whoami():
    w, h = 1280, 372
    rows = [("role", "IT Support Technician @ Leftclick (Cape Town MSP)", INK),
            ("focus", "L1/L2 service desk · M365 & Entra ID · AD · endpoint security", INK),
            ("degree", "BSc IT, Software Engineering · Golden Key (top 15%)", INK),
            ("studying", "Postgrad IT: networks & security, Zero Trust research", VIOLET),
            ("certified", "NinjaOne Certified Technician", ICE),
            ("building", "Wordskiis (live word game) · StudyOS (AI study platform)", SIGNAL),
            ("status", "ONLINE · open to opportunities", SIGNAL)]
    body = frame(w, h)
    body += f'<text x="40" y="52" font-size="16" class="fade"><tspan fill="{FAINT}">leo@leo-os</tspan><tspan fill="{LINEB}">:</tspan><tspan fill="{ICE}">~</tspan><tspan fill="{FAINT}">$ </tspan><tspan fill="{INK}">whoami --json</tspan></text>'
    body += f'<g class="fade" style="animation-delay:.4s"><rect x="40" y="72" width="{w - 80}" height="{h - 108}" rx="10" fill="{PANEL}" fill-opacity=".85" stroke="{LINEB}"/>'
    body += f'<text x="64" y="104" font-size="14" fill="{DIM}">identity.json</text>'
    body += f'<text x="{w - 64}" y="104" font-size="14" text-anchor="end"><tspan fill="{SIGNAL}" class="pulse">●</tspan><tspan fill="{SIGNAL}"> verified</tspan></text>'
    body += f'<line x1="64" y1="118" x2="{w - 64}" y2="118" stroke="{LINE}"/></g>'
    for i, (k, v, col) in enumerate(rows):
        y = 148 + i * 26
        body += (f'<g class="rise" style="animation-delay:{0.8 + i * 0.28:.2f}s"><text x="64" y="{y}" font-size="15" xml:space="preserve">'
                 f'<tspan fill="{FAINT}">"{k}":</tspan><tspan x="210" fill="{col}">"{escape(v)}"</tspan></text></g>')
    body += f'<text x="{w - 64}" y="{h - 52}" font-size="15" fill="{SIGNAL}" text-anchor="end" class="blink">▌</text>'
    return svg(w, h, body, title="whoami: Leo Lennards, IT Support Technician in Cape Town")


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur] if cur else lines


# ── services ────────────────────────────────────────────────────────────
SERVICES = [
    ("m365", "Microsoft 365 & Entra ID", "Users, licensing, mailboxes and MFA across client tenants.", ["M365", "Entra ID", "MFA"]),
    ("ad", "Active Directory", "Accounts, resets, group membership and Group Policy.", ["AD DS", "GPO"]),
    ("desktop", "Desktop Support", "Windows 10/11 and macOS end to end, printers, rebuilds.", ["Windows", "macOS"]),
    ("desk", "Remote Service Desk", "Triage, phone support, remote sessions, clear notes.", ["Triage", "Remote"]),
    ("endpoint", "Endpoints & Security", "ESET, full-disk encryption, NinjaOne RMM.", ["ESET", "NinjaOne"]),
    ("network", "Networking", "From Wi-Fi to VoIP: TCP/IP, DNS, DHCP, LAN/WAN.", ["DNS", "DHCP", "VoIP"]),
    ("email", "Firewall & Email Security", "Windows Firewall, WAF, Mimecast quarantine.", ["WAF", "Mimecast"]),
    ("server", "Server Support", "Windows Server 2019 roles and PowerShell.", ["Server 2019", "PowerShell"]),
]


def services():
    w = 1280
    cols, cw, ch, gap = 4, 287, 150, 16
    rows = (len(SERVICES) + cols - 1) // cols
    h = 76 + rows * (ch + gap) + 14
    body = frame(w, h)
    body += f'<text x="40" y="52" font-size="16" class="fade"><tspan fill="{FAINT}">leo@leo-os</tspan><tspan fill="{LINEB}">:</tspan><tspan fill="{ICE}">~</tspan><tspan fill="{FAINT}">$ </tspan><tspan fill="{INK}">systemctl status --all</tspan>'
    body += f'<tspan fill="{FAINT}">   # 8 services · </tspan><tspan fill="{SIGNAL}">all running</tspan></text>'
    for i, (sid, name, desc, tags) in enumerate(SERVICES):
        x = 40 + (i % cols) * (cw + gap)
        y = 76 + (i // cols) * (ch + gap)
        d = 0.3 + i * 0.12
        chips, cx = "", x + 18
        for t in tags:
            tw = len(t) * 7.6 + 16
            chips += f'<rect x="{cx:.0f}" y="{y + ch - 38}" width="{tw:.0f}" height="22" rx="5" fill="{PANEL2}" stroke="{LINE}"/><text x="{cx + 8:.0f}" y="{y + ch - 23}" font-size="12" fill="{DIM}">{escape(t)}</text>'
            cx += tw + 6
        body += f"""<g class="rise" style="animation-delay:{d:.2f}s">
  <rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="{PANEL}" fill-opacity=".9" stroke="{LINE}"/>
  <rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="none" stroke="{SIGNAL}" stroke-opacity="0">
    <animate attributeName="stroke-opacity" values="0;.55;0" dur="8s" begin="{2 + i:.0f}s" repeatCount="indefinite"/></rect>
  <text x="{x + 18}" y="{y + 30}" font-size="14"><tspan fill="{FAINT}">svc/</tspan><tspan fill="{INK}" font-weight="700">{sid}</tspan></text>
  <circle cx="{x + cw - 82}" cy="{y + 25}" r="4" fill="{SIGNAL}" class="ring" style="animation-delay:{i * .25:.2f}s"/>
  <circle cx="{x + cw - 82}" cy="{y + 25}" r="4" fill="{SIGNAL}"/>
  <text x="{x + cw - 18}" y="{y + 30}" font-size="12.5" fill="{SIGNAL}" text-anchor="end">running</text>
  <text x="{x + 18}" y="{y + 60}" font-size="14" fill="{ICE}">{escape(name)}</text>
  {''.join(f'<text x="{x + 18}" y="{y + 84 + k * 16}" font-size="12" fill="{DIM}">{escape(line)}</text>' for k, line in enumerate(wrap(desc, 33)[:2]))}
  {chips}
</g>"""
    return svg(w, h, body, title="systemctl status: Leo's IT services, all running")


# ── project cards ───────────────────────────────────────────────────────
PROJECTS = [
    ("wordskiis", "Wordskiis", "Five-letter word puzzle: daily challenge,", "Blitz, Duo, Survival, quests and XP.", "TypeScript", "#3178c6", "live", SIGNAL),
    ("studyos", "StudyOS", "AI-powered study platform: notes, docs,", "FSRS flashcards, exams and study plans.", "TypeScript", "#3178c6", "building", AMBER),
    ("portfolio", "Personal-Web-Portfolio", "leolennards.vercel.app: the LEO//OS", "terminal-style portfolio.", "TypeScript", "#3178c6", "live", SIGNAL),
    ("apexfitness", "ApexFitness", "Android fitness tracking app built with", "Kotlin and Jetpack Compose.", "Kotlin", "#a97bff", "shipped", ICE),
    ("ytdownloader", "YTDownloader", "Android app that saves videos, playlists", "and albums as MP3 or MP4.", "Kotlin", "#a97bff", "shipped", ICE),
    ("clicktrade", "ClickTrade", "C2C e-commerce website: listings,", "buyers and sellers.", "PHP", "#4f5d95", "archived", DIM),
]


def project(slug, name, l1, l2, lang, lcol, state, scol, index):
    w, h = 620, 168
    body = frame(w, h, 12)
    body += f"""
<defs><linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="{ICE}" stop-opacity="0"/><stop offset=".5" stop-color="{ICE}" stop-opacity=".09"/><stop offset="1" stop-color="{ICE}" stop-opacity="0"/></linearGradient></defs>
<rect y="0" width="140" height="{h}" fill="url(#scan)"><animate attributeName="x" from="-140" to="{w}" dur="5s" begin="{index * 0.7:.1f}s" repeatCount="indefinite"/></rect>
<g class="rise">
  <text x="28" y="44" font-size="17"><tspan fill="{FAINT}">svc/</tspan><tspan fill="{INK}" font-weight="700">{escape(slug)}</tspan></text>
  <circle cx="{w - 28 - len(state) * 8.4 - 14:.0f}" cy="38" r="4.5" fill="{scol}" class="ring"/>
  <circle cx="{w - 28 - len(state) * 8.4 - 14:.0f}" cy="38" r="4.5" fill="{scol}"/>
  <text x="{w - 28}" y="44" font-size="14" fill="{scol}" text-anchor="end">{escape(state)}</text>
  <text x="28" y="76" font-size="14" fill="{ICE}">{escape(name)}</text>
  <text x="28" y="102" font-size="13.5" fill="{DIM}">{escape(l1)}</text>
  <text x="28" y="122" font-size="13.5" fill="{DIM}">{escape(l2)}</text>
  <circle cx="34" cy="146" r="5" fill="{lcol}"/><text x="46" y="151" font-size="12.5" fill="{FAINT}">{escape(lang)}</text>
  <text x="{w - 28}" y="151" font-size="12.5" fill="{FAINT}" text-anchor="end">open ↗</text>
</g>"""
    return svg(w, h, body, title=f"{name}: {l1} {l2}")


# ── footer ──────────────────────────────────────────────────────────────
def footer():
    w, h = 1280, 120
    body = frame(w, h)
    body += f"""
<defs><clipPath id="cmd"><rect x="0" y="30" height="40" width="360">
  <animate attributeName="width" values="0;0;360;360" keyTimes="0;.15;.3;1" dur="10s" repeatCount="indefinite" calcMode="discrete"/></rect></clipPath></defs>
<text x="40" y="56" font-size="16"><tspan fill="{FAINT}">leo@leo-os</tspan><tspan fill="{LINEB}">:</tspan><tspan fill="{ICE}">~</tspan><tspan fill="{FAINT}">$ </tspan></text>
<text x="168" y="56" font-size="16" fill="{INK}" clip-path="url(#cmd)">exit</text>
<g><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.32;.34;.95;1" dur="10s" repeatCount="indefinite"/>
  <text x="40" y="86" font-size="15" xml:space="preserve"><tspan fill="{SIGNAL}">▸ </tspan><tspan fill="{INK}">agent disconnected</tspan><tspan fill="{FAINT}">  ·  thanks for visiting  ·  </tspan><tspan fill="{VIOLET}">stay secure.</tspan></text></g>
<text x="{w - 40}" y="56" font-size="16" fill="{SIGNAL}" text-anchor="end" class="blink">▌</text>
"""
    return svg(w, h, body, title="exit: thanks for visiting, stay secure")


def main():
    os.makedirs(OUT, exist_ok=True)
    files = {"header.svg": header(), "whoami.svg": whoami(), "services.svg": services(), "footer.svg": footer()}
    for i, p in enumerate(PROJECTS):
        files[f"project-{p[0]}.svg"] = project(*p, index=i)
    for name, content in files.items():
        with open(os.path.join(OUT, name), "w") as f:
            f.write(content)
    print("wrote", len(files), "svgs")


if __name__ == "__main__":
    main()
