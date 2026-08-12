# Dis-Fosint v5.7 - Discord OSINT suite

A complete, all-English, **Discord OSINT** research suite with a professional
CLI menu (no GUI). Every feature uses only **unauthenticated public endpoints** -
no tokens, no message sending, no server joining, no exploitation. Built clean
for security research, fraud investigation and OSINT education.

Run it:  `python main.py`

## Auto-push to webhook (v5.5+)

Every tool's console result is **automatically sent to your webhook** when one
is configured - fast (background thread, never blocks the tool) and pretty:

- Clean embed: tool name, UTC timestamp, output in a monospace block, gray accent
- ANSI codes and progress junk stripped; long outputs truncated safely (Discord limits)
- Skip list keeps tools that already push their own embeds (Server Intel dossier, Notifier)
- Toggle anytime in `[K] Settings` (option 6) or `config.json` key `auto_push`
- Silent when no webhook is set - nothing breaks without one

## Auto-save results (v5.6+, all versions)

Every tool run is **automatically archived to disk** - no manual saving:

- `results/<key>-<tool>/<timestamp>_<tool>.json` - structured document:
  tool, key, version, UTC timestamp, duration (ms), line count, lines array, raw text
- `results/<key>-<tool>/<timestamp>_<tool>.csv` - tidy data table:
  one row per output line with a type tag (`OK / INFO / WARN / ERR / PLAIN`)
- `results/index.jsonl` - append-only master timeline of every run
- Runs with no output are skipped; the console prints the saved paths
- `results/` is gitignored - archives stay local

## Credits

Developed by **Une-Sys**

- Site: https://une-sys.netlify.app/
- GitHub: https://github.com/Une-Sys
- Telegram: https://t.me/unezelsys

(Licensed under MIT - see LICENSE)

## Menu (professional look)

- Comfortable **black & gray** console theme - no emojis, no noisy colors
- Optional **transparent console**: run `set DIS_FOSINT_ALPHA=210` before launch
  (or edit the value; 60-255). Windows Terminal users can set transparency in
  Settings > Defaults; classic conhost is handled automatically on startup.
- ASCII banner + live version/tool counters + credits footer
- Single framed box with **named sections**:
  `CORE OSINT :: Server & Identity` / `DEEP INTEL :: Analysis & Risk` /
  `WORKFLOW :: Delivery & Case Files`, two columns per row, bright key tags,
  built-in footer `[A] [K] [X]`
- Sub-menus (settings, notifier, sources, cases) keep the boxed style with legends

## Install

```
pip install -r requirements.txt
python main.py
```

Optional: `set DIS_FOSINT_ALPHA=xxx` controls transparency (default 225).

## Architecture (layered, extensible)

```
main.py                      entry point - CLI menu (built from registry)
core/
  discord_api.py           HTTP layer: headers, invite regex, rate-limit-aware fetchers
  snowflake.py             offline snowflake math (decode, age, avatar hint)
  server_intel.py          Server Intel Ultimate (invite + widget chain, risk scan, dossier)
  tools.py                 compact tools: parser, triage, guild-by-ID, status, decoder
  url_forensics.py         CDN URL Forensics - snowflake extraction from any Discord link
  botlookup.py             Bot Directory Lookup - public archives (discord.bots.gg + discordbotlist)
  scam.py                  Scam Domain Radar - cached AntiScam list (36k+ domains); URL/text scan
  monitor.py               Server Monitor - pulse widget+invite counts, threshold alerts, webhook reports
  sources.py               OSINT Sources & Dorks - resource bank (8 sections, 71 references)
  user_tools.py            user ID lookup (lanyard + statusbadges, opt-in sources)
  cordcat.py               user deep lookup (cord.cat: breach check + risk/bot scores)
  notify.py                webhook embed notifications (color-coded, retry-aware)
  webhook_intel.py         Webhook Intel deep - snowflake dates, phish-name scan, guild widget cross-check
  cases.py                 case manager (per-target case files)
  registry.py              TOOL REGISTRY - the single place new tools are added
  ui.py                    boxed display layer (banner, grouped main menu, headers)
  config.py                settings (webhook URL, cordcat cookie)
```

## Menu

| Key | Tool |
|-----|------|
| 1 | Server Intel (Ultimate) - identity, growth bars, boosts, security, invite lifecycle, inviter age, events, feature decode, risk scan, live widget cross-check + invite chain, assets w/ SHA-256, dossier + raw JSON, webhook push |
| 2 | Guild by ID - widget probe without any invite |
| 3 | Invite Link Triage - resolve + risk-score every invite in any text |
| 4 | Invite URL Parser |
| 5 | User ID Lookup - account age, presence (lanyard), badges (statusbadges) |
| D | User Deep Lookup (cord.cat) - decorations/styles, flag decode, breach-source checkmarks, risk + bot scores (needs your browser's cf_clearance cookie via Settings) |
| 6 | ID Snowflake Decoder - offline math |
| 7 | Webhook Intel (deep) - type decode, masked token + charset check, snowflake dates for webhook/channel/guild/app/creator, phishing-name scan, public guild widget cross-check, optional lanyard creator presence |
| 8 | Discord Service Status |
| 9 | Webhook Notifier - embed test + configure |
| S | Scam Domain Radar - 36,748 flagged domains (local cache), base-domain matching, whole-text scan, live refresh |
| U | CDN URL Forensics - labels + decodes every snowflake in a link (avatars, attachments guild/channel, message links, emojis...) and hands invite codes to Triage |
| M | Server Monitor - samples members/online/expiry over time, threshold alerts, optional webhook report |
| B | Bot Directory Lookup - two public archives (no auth): identity, owner account age, tags, library, invites/stats |
| O | OSINT Sources & Dorks - bank: lookup sites, GitHub Discord tools (honest status tags), OSINT suites, communities, extensions, public API recipes, search dorks |
| C | Case Manager |
| A / K / X | About/Legal, Settings, Exit |

## Adding a new tool (extensibility)

1. Write a `def my_tool():` (no args) in any `core/*.py` module.
2. Register one line in `core/registry.py`:
   ```python
   ("7", "My New Tool", my_tool),
   ```
3. To place it in a menu section, add its key to a group in `TOOL_GROUPS`
   in `core/registry.py` (new groups are rendered automatically).
Done - it appears in the grouped menu automatically. Use
`core/discord_api.py` for any HTTP (you get retries/rate-limit handling for free)
and `core/snowflake.py` for ID math.

## Outputs
- `results\<tool>\*.json + *.csv` - every run auto-archived (JSON document + tidy CSV) + `index.jsonl` master log
- `reports\discord_<guild>_dossier.txt` - full dossier incl. raw API JSON + member dump
- `icons\*` - downloaded media with SHA-256 fingerprint printed
- `cases\*.case.txt` - per-target timelines
- `scamdomains.txt` - local cache of the Discord-AntiScam flagged domain list (refreshes weekly or on demand)
- `config.json` - webhook URL / cordcat cookie (secrets - keep private, gitignored)

## Ethics
Public data only. Authorized investigations only. No token theft, no message sending,
no server joining, no exploitation - ever.

## Copyright
(c) 2026 Une-Sys - MIT License. Full credits: https://une-sys.netlify.app/
