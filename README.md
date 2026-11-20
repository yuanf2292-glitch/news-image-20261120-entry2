# The Twentieth — World front page, Friday 20 November 2026

A one-page broadsheet front page that sums up the world news of
Friday 20 November 2026 in a single image. Eight stories, ranked by
consequence: the lead at the top, one in the black box, three more in
the middle row, three briefs under "Also Today".

Every story on the page happened, or was first reported, on
20 November 2026. Stories that belong to 19 November (the Shenzhen
trilateral, the ICJ ruling, the Kyiv embassy strikes, the Han
retrial, the Fiji disaster declaration) are deliberately not
repeated here — this page is the 20th alone.

## The eight stories

- **Akvan comes ashore at noon.** Cyclone Akvan crosses the coast
  close to Gopalpur around noon IST, weaker than feared: IMD
  Bulletin 35 (02:15 IST) has it down to a cyclonic storm, winds
  70–80 km/h gusting to 90. A 0.5–1.0 m surge is warned for six
  districts; 105,000 people moved to shelters.
- **A peace statement that says nothing about Ukraine.** Trump and
  Putin approve a joint statement with no mention of Ukraine. The
  Senate minority leader attacks Trump for calling Putin a "friend".
  Japan's Takaichi holds first talks with Putin on the APEC
  sidelines; Merz sets terms for peace talks after a Berlin summit.
- **Xi presses open trade as APEC leaders meet.** Leaders in
  Shenzhen discuss trade, investment and technology; India presses
  climate finance at COP31 in Türkiye.
- **Nicholls century steadies New Zealand.** Henry Nicholls finishes
  day one of the first Test against India unbeaten on 113 at the
  Basin Reserve; New Zealand close on 243 for five.
- **Brussels charges Spaniard over rail fraud.** EU prosecutors
  charge a Spanish national over €213.7m of Bulgaria railway
  funding fraud; three detained in Poland in a VAT-evasion inquiry.
- **Justice Dept subpoenas pile up.** The US Justice Department
  issues more than 200 subpoena requests in an Alaska election
  inquiry.
- **Gulf Railway to link six states.** The project aims to join six
  Gulf nations by rail and cut reliance on the Strait of Hormuz.
- **EU urges AI skills for all.** The EU encourages member states to
  equip teachers, students and workers with AI skills.

Sources: IMD, Reuters, AP, AFP, Euronews, Times of India.
Compiled 20 Nov 2026.

## Files

- `entry.png` — the finished page, 1024x1024 PNG, under 1 MiB.
- `main.py` — Python 3, standard library only, no network. It gates
  the artwork (real PNG/JPEG header, at most 1 MiB, sides at most
  1024 px), copies it to `$MAKEFUN_OUTPUT_DIR` (or `/output`) in
  32 KiB pieces, then re-reads the copy and checks size and SHA-256
  against the source. A failed gate writes nothing and exits
  non-zero. An output directory equal to the artwork's own directory
  is verified in place instead of copied onto itself.
- `build_frontpage.py` — the Pillow script that draws the page
  (kept for reference; the submitted artwork is the rendered PNG).

## Try it

```sh
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 python3 main.py
MAKEFUN_OUTPUT_DIR=out2 python3 main.py
cmp out1/entry.png out2/entry.png   # same bytes on both runs
```
