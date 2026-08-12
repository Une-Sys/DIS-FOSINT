"""Dis-Fosint - Discord OSINT suite, main entry point.

The menu is generated from core.registry.TOOLS, so new tools appear
automatically once registered there. Every tool's console output is
auto-pushed to your webhook (if configured) as a pretty embed, and
auto-saved locally as JSON + CSV under results/.
"""

import os
import sys
import time

from core import config, notify, results, ui
from core.registry import TOOL_MAP, tool_groups

NAME = ui.NAME
VERSION = ui.VERSION

# tools that push their own embeds - the auto-push skips them
PUSH_SKIP = {"1", "9"}


class _Tee:
    """Captures printed output while still showing it live."""

    def __init__(self, real):
        self.real = real
        self._buf = []

    def write(self, s):
        self._buf.append(s)
        self.real.write(s)

    def flush(self):
        self.real.flush()

    def text(self):
        return "".join(self._buf)


def run_tool(label, fn, key):
    real = sys.stdout
    tee = _Tee(real)
    sys.stdout = tee
    started = time.time()
    try:
        fn()
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout = real
        dur_ms = int((time.time() - started) * 1000)
        saved = results.save_result(key, label, tee.text(), duration_ms=dur_ms)
        if key not in PUSH_SKIP:
            notify.push_output(label, tee.text())
        if saved:
            ui.info(f"Saved: {os.path.relpath(saved[0])} + {os.path.relpath(saved[1])}")


def about():
    ui.header("ABOUT / LEGAL")
    ui.info(f"{NAME} {VERSION}")
    ui.info("A professional OSINT suite for Discord - built for security research,")
    ui.info("fraud investigation and account forensics education.")
    ui.info("")
    ui.warn("ETHICS: This tool NEVER sends messages, grabs tokens, joins servers")
    ui.warn("or touches non-public data. Use only against targets you are")
    ui.warn("authorized to investigate. Files carry SHA-256 fingerprints.")
    ui.separator()
    ui.result("Data sources (100% unauthenticated public endpoints):")
    ui.info("  - discord.com API v9: invites, widget, widget image")
    ui.info("  - Snowflake decoding (offline math, no requests)")
    ui.info("  - discordstatus.com status API")
    ui.info("  - api.lanyard.rest + api.statusbadges.me (user OPT-IN sources)")
    ui.info("  - Webhook notifications to YOUR OWN channel")
    ui.info("  - Auto-push: every tool result is sent to your webhook (toggle in [K])")
    ui.info("  - Auto-save: every run is archived as JSON + CSV under results/")
    ui.separator()
    ui.result(ui.CREDITS)


def main():
    ui.enable_transparency()
    while True:
        try:
            ui.clear()
            ui.banner(tools=len(TOOL_MAP))
            ui.main_menu(tool_groups(),
                         footer="[A] About / Legal    [K] Settings    [X] Exit")
            choice = ui.prompt()
            low = choice.lower()
            if low in TOOL_MAP:
                label, fn = TOOL_MAP[low]
                run_tool(label, fn, low)
            elif low == "a":
                about()
            elif low == "k":
                config.config_menu()
            elif low == "x" or choice == "99":
                ui.ok("Exiting. Stay clean.")
                sys.exit(0)
            else:
                ui.err("Invalid choice")
            ui.pause()
        except KeyboardInterrupt:
            print()
            ui.ok("Exiting. Stay clean.")
            sys.exit(0)


if __name__ == "__main__":
    main()