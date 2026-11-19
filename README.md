# The World by Post — Wednesday 18 November 2026 in one image

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/vr23zone/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/vr23zone/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One day of world news, delivered as a page from a stamp album. **Wednesday 18 November 2026** is
named in the masthead and cancelled, stamp by stamp, with a round postmark dated **18 NOV 2026**.

**Twelve perforated postage stamps** carry the day's biggest stories — each with a place line, a
flat vector scene drawn in code, a headline and a short caption:

1. 🤝 **Shenzhen, China** — Xi Jinping hosts Vladimir Putin on the APEC sidelines; on Thursday
   Donald Trump joins them for the first-ever US–China–Russia trilateral summit.
2. 💥 **Qeshm Strait, Iran** — US jets strike a Revolutionary Guards missile site on Qeshm Island;
   Iran answers with combat drones against bases in Kuwait and Bahrain.
3. 🌉 **Kerch Strait, Crimea** — a seven-stage Ukrainian drone-and-missile attack drops one arch
   of the Kerch Bridge into the strait; Zelensky calls it "unprecedented".
4. 🗳️ **Alaska, USA** — Mary Peltola beats Dan Sullivan in the last midterm Senate race called;
   Democrats take the Senate 56–44, their largest majority since 2009.
5. 🦠 **United States** — after 26 years, America loses its measles-elimination status:
   5,412 cases and 10 deaths in 2026.
6. 🏥 **DR Congo** — the Ebola outbreak passes 11,000 cases, the second-largest on record; around
   Bunia and Beni, nearly three in four infected children under five die.
7. 🛰️ **Deep space** — NASA's Voyager 1 crosses one light-day from Earth, about 16 billion miles
   out; its signals now take a full 24 hours to reach home.
8. 💹 **Santa Clara, USA** — Nvidia posts a record quarter and a $130bn revenue forecast, while
   its board rules out reinstalling founder Jensen Huang as CEO.
9. 🏦 **Frankfurt, Germany** — 15 million internal Deutsche Bank documents leak to Der Spiegel and
   about 50 media outlets, alleging blind eyes to fraud and financing for arms dealers.
10. 🌍 **Antalya, Türkiye** — COP31 opens the second Global Stocktake under the Paris Agreement
    with 21 negotiating issues still deadlocked and Friday's deadline looming.
11. 🎮 **Sydney, Australia** — Grand Theft Auto VI billboards go up from Tokyo to Sydney on the eve
    of the 19 November launch; New Zealand braces for some 35 petabytes of downloads.
12. ⚽ **Nations League, Europe** — England beat Spain 3–2 to end Spain's 43-match unbeaten run;
    Germany hit five past the Netherlands; Norway and Portugal win 3–2 thrillers.

Below the stamps, a **POSTCARD BRIEFS** strip adds **26 more of Wednesday's stories** as numbered
one-liners, each with its own emoji: Houthi drones on Saudi pipeline stations and their advance on
Aden; the Knesset electing Kahana; Trump's peace board faulting both Israel and Hamas; Gaza's
fourth winter; UK sanctions over West Bank settlements; Trump's "very big" Philippines trade deal;
Waymo pulled from US freeways; the outage wave reaching the NSA; the Siberian An-12 crash that
killed 19; a Ukrainian drone strike on a Russian warship in the Gulf of Finland; 8,000 bomb threats
across Europe; UK inflation at 3.6%; the day's market slide (DAX –2.1%, CAC –1.6%, S&P –1.0%,
gold –2.3%); antibiotic-proof Klebsiella in Europe's hospitals; Seoul's $75,000 AI-exam-cheat
bounties; arsenic-poisoned villages in Thailand; a murdered Costa Rican journalist; Pope Leo XIV's
plea against hate; Haiti's "Thank you, Bukele" marches; the World Court's Thursday ruling on
Myanmar; Fiji's El Niño disaster declaration; Sulawesi's new gel-nesting flying frog; termite-
fishing chimps in Tanzania; Antarctica's fragile footprints; and New Zealand's seventh-state debate.

**38 stories in total.** Continent check: Asia (Shenzhen, Qeshm, Manila, Seoul, Thailand, Sulawesi) ·
Europe (Kerch, Frankfurt, Antalya, the Nations League, the West Bank sanctions, the Gulf of Finland,
the bomb threats, British inflation, the hospital superbug) · North America (Alaska, measles, Santa
Clara, Waymo, the outages, Costa Rica, Haiti) · Africa (DR Congo, Tanzania) · South America (Peru) ·
Oceania (Sydney, Fiji) · Antarctica (the footprint study) · Zealandia (New Zealand) — eight
continents — plus deep space (Voyager 1) and the global markets. Every story was first reported on
**Wednesday 18 November 2026** (wire and press reports dated that day; the Nations League matches
were played on the night of Tuesday 17–Wednesday 18 November European time and reported on the
18th). Sources: Reuters, BBC, AP, AFP, UN News, NASA/JPL, The Hindu, the Straits Times, MercoPress,
People and Phys.org, as credited on the image.

## How it is made

`entry.png` (1024 × 1024) is drawn and typeset by **`draw.py`** (Python 3 + Pillow): the airmail
border, the perforated stamps, the flat vector scenes, the postmarks and all of the text are
computed in code from the Noto Sans / Noto Serif / Noto Color Emoji faces — no photographs, no
hand-placed text — and the script refuses to draw if any caption would overflow its stamp or any
brief its column. The output is deterministic: the same bytes on every run.

`main.ts` is the entry the grader runs. It copies the committed `entry.png` to the output
directory:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

To redraw the picture itself: `python3 draw.py`.

---
Entered on [make.fun](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · MIT licensed
