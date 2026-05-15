#!/usr/bin/env python3
"""generate.py — build index.html from the bridge / version template.

Run after each new bridge release:
  py -3 C:\\dev\\N6NUBridgeLanding\\generate.py
Output:
  C:\\dev\\N6NUBridgeLanding\\index.html

Single source of truth for the bridge inventory + version history.
Bump LATEST when shipping a new family-aligned release; the older
versions stay listed under "Previous" without manual editing.
"""
from datetime import date
from pathlib import Path

LATEST    = "1.1.7"
PREVIOUS  = ["1.1.6", "1.1.5", "1.1.4", "1.1.3", "1.1.2", "1.1.1", "1.1.0"]

# Per-bridge version overrides — used when a single bridge ships
# ahead of the family-aligned LATEST. Keys are the slug. The version
# string here becomes the Latest link; the family LATEST gets bumped
# into that bridge's Previous list so older versions stay reachable.
PER_BRIDGE_LATEST = {
    "sdrplay-rx-bridge": "1.1.21",
}

# Diagnostic / debug builds. One-off binaries cut to chase a specific
# tester report. None currently shipped — most recent (W3SZ r2 2026-05-15)
# was promoted to the mainline v1.1.21 SDRplay release.
DEBUG_BUILDS = []


def debug_build_block(b):
    return f'''<div class="bridge">
  <h3>{b["title"]}</h3>
  <p class="desc">{b["desc"]}</p>
  <p class="latest">Download:
    <a href="{b["filename"]}">{b["filename"]}</a>
  </p>
</div>
'''


def debug_section():
    """Whole 'Debug builds' section. Caller guards on DEBUG_BUILDS truthiness."""
    blocks = "".join(debug_build_block(b) for b in DEBUG_BUILDS)
    return f'''<h2 id="debug">Debug builds</h2>
<p>
  One-off diagnostic builds cut to chase a specific tester report.
  <b>Don't install these unless I've asked you to.</b> They carry an
  off-stream version number on purpose so they don't get confused
  with regular releases, and they may have extra logging or
  experimental fixes that haven't landed in the mainline yet.
</p>

{blocks}'''

# (display name, github repo path with case, slug for filename, short desc)
BRIDGES = [
    ("HackRF One",                              "HackRF-RX-Bridge",   "hackrf-rx-bridge",
     "8-bit ADC, 1 MHz - 6 GHz. Needs WinUSB via Zadig (bundled in installer)."),
    ("RTL-SDR (R820T2 / V3+)",                  "rtlsdr-rx-bridge",   "rtlsdr-rx-bridge",
     "8-bit ADC, max 2.4 Msps. Needs WinUSB via Zadig (bundled)."),
    ("SDRplay (RSP1A / RSPduo / RSPdx)",        "sdrplay-rx-bridge",  "sdrplay-rx-bridge",
     "14-bit ADC. Requires SDRplay API 3.x service installed first from sdrplay.com."),
    ("AirSpy R2",                               "airspy-rx-bridge",   "airspy-rx-bridge",
     "12-bit ADC, 10 Msps native. Needs WinUSB via Zadig (bundled)."),
    ("ADALM-Pluto / Pluto+ (RX only)",          "pluto-rx-bridge",    "pluto-rx-bridge",
     "12-bit ADC, 70 MHz - 6 GHz. Requires Analog Devices' libiio drivers installed first."),
    ("ADALM-Pluto / Pluto+ (RX+TX)",            "pluto-wsjtx-bridge", "pluto-wsjtx-bridge",
     "Same hardware as pluto-rx but with TX path enabled. Use this if Pluto is your only radio (QO-100, indoor low-power tests)."),
    ("FunCube Pro+ V2 / FlexRadio DAX-IQ / Malachite", "iq-rx-bridge", "iq-rx-bridge",
     "Sound-card IQ source (any USB sound card delivering stereo IQ as audio L=I, R=Q). No special drivers — Windows audio class."),
]

URL = ("https://github.com/n6nu/{repo}/releases/download/"
       "v{ver}/{slug}-{ver}-setup.exe")


def bridge_block(name: str, repo: str, slug: str, desc: str) -> str:
    # A per-bridge override means this bridge shipped a release ahead
    # of the family-aligned LATEST. The previous family LATEST then
    # leads the Previous list so it's still one click away.
    bridge_latest = PER_BRIDGE_LATEST.get(slug, LATEST)
    bridge_prev = ([LATEST] + PREVIOUS) if slug in PER_BRIDGE_LATEST else PREVIOUS
    latest_url = URL.format(repo=repo, ver=bridge_latest, slug=slug)
    latest_file = f"{slug}-{bridge_latest}-setup.exe"
    prev_links = " · ".join(
        f'<a href="{URL.format(repo=repo, ver=v, slug=slug)}">v{v}</a>'
        for v in bridge_prev
    )
    return f'''<div class="bridge">
  <h3>{name}</h3>
  <p class="desc">{desc}</p>
  <p class="latest">Latest:
    <a href="{latest_url}">{latest_file}</a>
  </p>
  <p class="history">Previous:
    {prev_links}
  </p>
</div>
'''


HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>N6NU SDR Bridges — Downloads</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
         max-width: 880px; margin: 2em auto; padding: 0 1em; color: #222; line-height: 1.5; }}
  h1   {{ color: #1a3d6b; border-bottom: 2px solid #1a3d6b; padding-bottom: 6px; }}
  h2   {{ color: #1a3d6b; margin-top: 2em; }}
  h3   {{ color: #444; margin-top: 1.4em; }}
  .bridge {{ border: 1px solid #ddd; border-radius: 6px; padding: 0.6em 1em;
            margin: 0.6em 0; background: #fafafa; }}
  .bridge h3 {{ margin: 0.2em 0 0.3em 0; }}
  .latest {{ font-weight: bold; color: #1a7f3a; margin: 0.3em 0; }}
  .history {{ color: #666; font-size: 0.9em; margin: 0.2em 0 0.4em 1.2em; }}
  .history a {{ color: #888; }}
  a {{ color: #1a3d6b; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .desc {{ font-size: 0.92em; color: #555; margin: 0; }}
  .meta {{ color: #888; font-size: 0.85em; margin-top: 0.2em; }}
  footer {{ margin-top: 3em; padding-top: 1em; border-top: 1px solid #ddd;
           font-size: 0.88em; color: #666; }}
  code {{ background: #eee; padding: 1px 5px; border-radius: 3px; font-size: 0.92em; }}
</style>
</head>
<body>
<h1>N6NU SDR Bridges</h1>
<p>
  Windows installers for the <b>SDR bridges</b> that feed wideband I/Q
  into a modified WSJT-X / QMAP for wide-band Q65 EME and other
  digital modes. Pick the bridge for your hardware.
</p>
<p>
  Each release is a drop-in upgrade from the previous one. Latest
  family release: <b>v{LATEST}</b>.
  See the <a href="#beta">beta-tester guide PDF</a> for setup,
  troubleshooting, and the technical reference.
</p>

<h2>Bridges</h2>

{"".join(bridge_block(*b) for b in BRIDGES)}

<h2 id="beta">Beta-tester guide</h2>
<p>
  PDF covers what's new in this build of WSJT-X / QMAP-improved, why
  the bridges exist, per-bridge setup (drivers, gains, quirks), a
  troubleshooting table, and a technical reference at the end.
</p>
<p>
  <a href="WSJTX-QMAP-improved-beta-guide.pdf"><b>WSJTX-QMAP-improved-beta-guide.pdf</b></a>
  (latest build, served from this site)
</p>
<p class="meta">
  The same PDF also ships inside each bridge installer at
  <code>{{install dir}}\\WSJTX-QMAP-improved-beta-guide.pdf</code>,
  accessible from the bridge GUI via <code>Help → User Guide</code>
  (F1) since v1.1.5.
</p>

{debug_section() if DEBUG_BUILDS else ""}

<footer>
  <p>
    Author: <b>Andreas Junge, N6NU</b>
    &lt;<a href="mailto:n6nu@n6nu.org">n6nu@n6nu.org</a>&gt;.
    Page generated {date.today().isoformat()}.
    Source: <a href="https://github.com/n6nu/N6NUBridgeLanding">github.com/n6nu/N6NUBridgeLanding</a>.
  </p>
</footer>

</body>
</html>
'''

OUT = Path(__file__).with_name("index.html")
OUT.write_text(HTML, encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes, {len(BRIDGES)} bridges, "
      f"latest=v{LATEST})")
