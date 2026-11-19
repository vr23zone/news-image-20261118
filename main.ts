// "The World by Post" — a news-image entry for make.fun's
// "Sum up 18 November's world news in one image" bounty
// (news-image-20261118).
//
// The picture itself is entry.png beside this file: one day of world
// news delivered as a page from a stamp album. Twelve perforated
// postage stamps carry Wednesday 18 November 2026's biggest stories —
// the Xi–Putin meeting in Shenzhen ahead of the first US–China–Russia
// summit, Iran's drone answer to the US strike on Qeshm Island, a
// fallen arch of the Kerch Bridge, Alaska settling the US Senate,
// America losing its measles-free status, Congo's Ebola toll passing
// 11,000, Voyager 1 crossing one light-day from Earth, Nvidia's record
// quarter, the 15-million-file Deutsche Bank leak, COP31's climate
// reality check in Antalya, GTA VI eve in Sydney, and the Nations
// League's final-night drama — each stamp cancelled with a postmark
// dated 18 NOV 2026. A POSTCARD BRIEFS strip adds 26 more of the day's
// stories as numbered one-liners: 38 stories, 8 continents, one day.
//
// The image is drawn and typeset by draw.py (Python + PIL) from the
// flat vector scenes and wording in that file, deterministically.
//
// This program's whole job is to put that image where the grader looks:
// it copies entry.png to /output/entry.png (MAKEFUN_OUTPUT_DIR stands
// in for /output outside the grader's container):
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
