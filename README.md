# N6NU Bridge Landing

Static landing page hosting download links for the **N6NU SDR Bridges**
(Windows installers for HackRF / RTL-SDR / SDRplay / AirSpy / Pluto /
sound-card-IQ feeders that drive a modified WSJT-X / QMAP for wide-band
Q65 EME).

## Live site

- **GitHub Pages:** https://n6nu.github.io/N6NUBridgeLanding/
- **Vercel:** _(connect via vercel.com → New Project → import this repo)_

Both serve `index.html` from the repo root. Static assets only — no
build step needed.

## Layout

```
index.html                              # the landing page (generated; don't edit by hand)
WSJTX-QMAP-improved-beta-guide.pdf      # latest beta-tester guide, linked from index.html
generate.py                             # template that produces index.html
.nojekyll                               # tells GitHub Pages to skip Jekyll processing
vercel.json                             # (optional) clean-URL routing for Vercel
```

## Updating

When a new bridge release ships (v1.1.6, v1.2.0, etc.):

```bash
# 1. Bump LATEST + push the previous version into PREVIOUS
#    inside generate.py (one-line edit)
py -3 generate.py

# 2. If the user-guide PDF changed, drop the new one in:
cp /path/to/WSJTX-QMAP-improved-beta-guide.pdf .

# 3. Commit + push
git add index.html WSJTX-QMAP-improved-beta-guide.pdf
git commit -m "v1.1.6 release"
git push
```

GitHub Pages picks up the change in ~1 minute. Vercel auto-deploys on
every push.

## Source

The bridge sources live at <https://github.com/n6nu> (per-app repos):
HackRF-RX-Bridge, rtlsdr-rx-bridge, sdrplay-rx-bridge, airspy-rx-bridge,
pluto-rx-bridge, pluto-wsjtx-bridge, iq-rx-bridge. The common monorepo
+ build / packaging / harness work is private to N6NU.

The beta-tester guide PDF is regenerated from
`C:\dev\wsjtx-improved\generate-beta-guide.py` (ReportLab). Bundled
inside each v1.1.5+ bridge installer; also served here.

## License

Page content + generator script: MIT (see `LICENSE`).
The PDF and the bridges themselves are GPL-3.0 — see each bridge's
own repo for the actual source license.
