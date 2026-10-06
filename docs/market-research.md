# stemdrop: market and money memo

## Verdict

As built, stemdrop will not make meaningful money. It is worth a few weekends as a portfolio piece and a funnel, not a business. Your "broke or cheap" hunch holds up. 77.8% of independent artists earn under $15k a year from music (https://info.xposuremusic.com/article/music-industry-report-2025), and 49% of indie audio-tool companies make under $20k a year (https://moonbase.sh/reports/state-of-audio-plugin-companies-2025/). A bare local demucs wrapper is also already free in several better-featured forms. Only the workflow around the split has a plausible price.

## 1. The market in numbers

Demand is huge. MIDiA counts 148.7M music creators (http://www.midiaresearch.com/blog/the-future-of-the-music-creator-economy). LALAL.AI had 6.79M registered users and 63.8M splits in 2025 (https://www.lalal.ai/blog/lalalai-wrapped-2025/), which is about nine splits per user per year. That is occasional use, which suits one-time pricing better than subscriptions.

| Product | Price | Notes |
|---|---|---|
| LALAL.AI | Free 10 min/mo; Lite $90/yr; Pro $180/yr; 750 min top-up $50 | Fast-queue minutes expire monthly (https://www.lalal.ai/pricing/) |
| LALAL "Lyra" local model | Pro plan only | Offline since 21 May 2026 (https://www.lalal.ai/blog/lyra-local-stem-separation-in-lalalai-desktop-app-and-vst-plugin/) |
| Moises (App Store) | $5.99/mo or $39.99/yr; Pro $29.99/mo | 70M users (https://moises.ai/newsroom/company-milestones/2025-year-in-review) |
| Fadr | Free MP3 stems; Plus $10/mo | WAV is paid (https://fadr.com/plus) |
| StemSplit | $0.10-0.20/min, credits never expire | Same htdemucs_ft model as stemdrop (https://stemsplit.io/pricing) |
| Mac demucs apps | StemWave $9.99, Stemly Split $22.99, StemSplitter Studio €49 | StemWave has no ratings; Stemly has no KVR reviews; StemSplitter got 2 Product Hunt upvotes |
| UVR5, StemDeck, StemRoller | Free | UVR5 has 26.5k stars (https://github.com/Anjok07/ultimatevocalremovergui); StemDeck has about 4k (https://github.com/stemdeckapp/stemdeck) |

"Offline, no credits" is no longer unique. Lyra sells it at Pro prices, and StemDeck gives it away with 6 stems, a mixer and batch queue. Demucs is also aging. On MVSEP's benchmark htdemucs_ft scores about 8.3 dB on vocals against about 12 dB for BS-RoFormer (https://mvsep.com/en/algorithms), and the maintainer says he is no longer actively working on it.

## 2. What the built-in DAW features leave on the table

- **Ableton:** Live 12.3 added local 4-stem separation on 25 Nov 2025, but only in Suite ($749). Standard is $439, Intro $99, and the Live 7-11 Suite upgrade is $229 (https://www.ableton.com/en/release-notes/live-12/, https://www.sweetwater.com/store/detail/Live12SteUpI). You are on Live 11, so you are exactly the gap. No public data says how big that cohort is.
- **Logic:** $199.99, 6 stems, Apple Silicon only (https://apps.apple.com/us/app/logic-pro/id634148309). It beat paid rivals in MusicRadar's January 2026 test.
- **Other DAWs:** FL Studio, Studio One Pro and Cubase Pro have it. Reaper has no built-in option. Every DJ app has live stems too.
- **Mashup workflow:** None of them do two-song key/BPM matching, acapella-to-beat alignment, or a pre-warped hand-off. That is the real gap.
- **Speed:** stemdrop runs CPU-only on Mac because htdemucs crashes on MPS, so it is slower than Ableton 12.3.7+ and Logic.

## 3. Who pays and what for

Nobody pays for the split itself. People pay for:
- **Recurring value felt every session:** Splice charges $12.99-39.99/mo for a library.
- **One-time workflow tools:** Mixed In Key 11 Pro is $99 and Mashup 2.5 is $29 (https://shop.mixedinkey.com/). DJ.Studio Pro+Stems is $169, Serato Sample is $129, and Youka Live is $79 plus $29.99 model upgrades.
- **B2B licensing:** AudioShake raised $14M and Music.ai charges $0.05-0.15/min per stem. A solo dev wrapping open weights can't sell into that.

Forum reaction is anti-subscription. Hobbyists cancel Moises after "10 songs in two years" (https://community.justinguitar.com/t/stemdeck-a-free-moises-alternative/414339), and a user on Hacker News volunteers about €35 perpetual for Nuo Stems (https://news.ycombinator.com/item?id=49486081). Mashup makers are the most free-first group. Rave.dj has 8 paying Patreon members out of 1,891 (https://www.patreon.com/RaveDJ). DJs already have stems in their software.

## 4. Monetization options, ranked

Revenue ranges are my estimates, not sourced figures.

1. **Free and open source plus tip jar.**
   - Price: free, with GitHub Sponsors or Buy Me a Coffee.
   - Channel: GitHub, Bedroom Producers Blog, Product Hunt.
   - Effort: low, a weekend of polish.
   - Revenue: $0-50 a month.
   - Risk: near-zero income. UVR5 runs on tips at 26k stars, and StemDeck takes no money. The payoff is audience and credibility.

2. **Mashup prep kit, one-time $29-39.**
   - What it does: key/BPM detection on two songs, acapella-to-beat time/pitch matching, bar-aligned export of warped WAVs for Ableton, and `beat.wav`.
   - Channel: your own site, with a free tier as the funnel.
   - Effort: 6-10 weekends.
   - Revenue: $50-500 a month with some audience.
   - Risk: Mixed In Key's $29 and $99 products are incumbents. Generating Ableton `.als` files from outside Live is untested.
   - Reality check: the nearest paid precedents have no visible traction. AudioCipher, a solo $15 plugin with a real hook, reached about $96k a year with ads, and 92% of its sales came from its own site (https://www.starterstory.com/how-to-sell-music-software).

3. **Paid "Pro" upgrade, $29-49 one-time.**
   - What it adds: RoFormer-class vocal models, kick/snare/hat drum splits, Traktor `.stem.m4a` export, batch.
   - Template: Go-Splitter Pro at $45 and Youka's paid model upgrades.
   - Effort: 3-5 weekends.
   - Revenue: $30-300 a month.
   - Risk: model licenses. UVR's models allow commercial reuse with credit, but some community models are non-commercial.

4. **Setapp or direct Mac channel.**
   - Terms: Setapp pays 70% of revenue (https://docs.setapp.com/docs/distributing-revenue).
   - Skip the Mac App Store. Rogue Amoeba found direct sales earn more (https://weblog.rogueamoeba.com/2017/02/10/piezos-life-outside-the-app-store/). AudioCipher got zero organic sales there.
   - Effort: low-medium, mostly packaging and notarization.
   - Revenue: $0-200 a month.
   - Risk: a Python bundle may not fit sandboxing, and Setapp acceptance isn't guaranteed.

5. **Hosted "upload a song" service.** Don't. Per-minute pricing is $0.10 and heading to zero. You would also pick up host takedown liability and support load. 51% of indie plugin support load is licensing and installation.

## 5. What to build next, if you go for it

1. Add a model-loading layer, using python-audio-separator or UVR models. Swap in a RoFormer vocal model and credit UVR.
2. Fix Apple Silicon speed through CoreML or another model path.
3. Add key/BPM detection, then acapella-to-beat matching.
4. Add Ableton-ready export, either warped WAVs first or `.als` later.
5. Add a LICENSE file. The repo has none (checked locally).
6. Before charging, post a pay-what-you-want Gumroad listing and see whether anyone pays.

## 6. The legal line

- **Weights.** The demucs code is MIT. The pretrained weights are unresolved. The maintainer said three times in 2022-23 that they are research-only (https://github.com/facebookresearch/demucs/issues/327). They were trained on MUSDB18-HQ, which is non-commercial (https://zenodo.org/records/3338373). The July 2026 Hugging Face card has no license field. Nobody has enforced this, but it is unlicensed commercial use. Ask the maintainer for a one-line license, or ship UVR models. Don't bundle the weights, since stemdrop currently downloads them from Meta's CDN at runtime.
- **Local file in, files out.** This is low risk. Nobody has sued a separation tool, and DMCA 1201 isn't triggered by splitting a file you own.
- **No URL ripping.** YouTube/Spotify import is what brings in DMCA 1201 and ToS exposure, and Apple's guideline 5.2.3 bans it in App Store apps.
- **Never sell or host stems or acapellas of other people's songs.** That is plain infringement. Releasing mashups needs sampling clearance, and Content ID will flag them.
- **Market it as "your songs, your stems."**

## 7. Recommendation

Make stemdrop public and open source, add a LICENSE, and treat it as a portfolio piece and a funnel. Don't charge for the split. If you want to test for money, spend a few weekends on option 2, the mashup prep kit. Put RoFormer models and key/BPM matching behind a free tier. Sell it direct for $29-39 one-time, and test demand with a pay-what-you-want listing before building the whole thing. Skip subscriptions, credits and hosting. Expect pocket money at best: tens to a few hundred dollars a month, and that only if you build an audience first.

---

# Critic notes

1. **No evidence anyone pays for a standalone local splitter, and the memo's revenue figures are guesses.** The dossier's open questions say this in every lens. The $0-50, $50-500, $30-300 and $0-200 a month ranges are labeled "my estimates" and rest on no sales data. No Gumroad, KVR or App Store numbers exist for any paid demucs wrapper. The "no traction" claim comes from absence of ratings and 2 Product Hunt upvotes, which is weak evidence. The recommendation to build the mashup kit rests on this gap.

2. **The mashup kit has no demand test, and the incumbent was never examined.** Mixed In Key Mashup 2.5's feature list could not be fetched, so the memo cannot say whether it already does phrase alignment. Generating Ableton `.als` files from outside Live is untested. The AudioCipher comparison ($96k a year) is a different product with paid ads, so it does not support this one.

3. **The license claims are unverified.** The memo says "UVR's models allow commercial reuse with credit," but the dossier flags RoFormer and UVR community model licensing as unverified and sometimes non-commercial. Whether Meta's CDN terms cover a commercial app pulling weights at install time was never checked. The memo mentions the weights risk but not these two gaps.

4. **Some memo figures conflict with the dossier or lean on low-confidence sources.**
   - The memo gives Ableton Standard as $439. One lens found $439 and another found $349.
   - The memo gives Moises at App Store prices ($5.99 a month, Pro $29.99). The web prices are $3.99 and $9.99, which weakens the "price ceiling" point.
   - The "51% of indie plugin support load is licensing and installation" figure does not appear in the dossier text I could search. The only 51% I found there is an unrelated, low-confidence stat about plugin subscriptions.
   - The Rave.dj Patreon figure (8 paying of 1,891) and the €35 Nuo Stems quote are single data points presented as segment evidence.

5. **The addressable Ableton cohort and the speed gap are unquantified.** The Live 11, Standard and Intro cohort has no public size, and the dossier says so in four lenses, yet the memo still calls it "exactly the gap." The "slower than Ableton and Logic" claim has no benchmark. Whether CoreML or RoFormer closes it is open.

6. **Community sentiment was never directly read, and the legal section is partly untested.** Reddit was blocked, so "just use UVR" is inferred from review sites. LALAL's Lyra quality is unbenchmarked beyond the vendor's own claim. Content ID behavior on transformed mashups rests on vendor blogs only. The "low risk" legal call is a reasonable read, not a legal opinion.

**Overall confidence: medium-high that stemdrop is not a business, low on the specific $29-39 mashup-kit path and every dollar range.**
