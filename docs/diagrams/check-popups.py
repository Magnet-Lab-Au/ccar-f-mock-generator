"""Check the popups of each diagram in a headless browser.

For each HTML file in docs/diagrams/, the script adds check-popups.js to a
copy of the page, opens the copy in Chrome headless, and reads the result from
the page title. The check: each part with data-step opens its popup, the popup
stays in the window, and Escape closes it. The script changes no diagram.

Run from the folder ccar-f-mock-generator:
    python3 docs/diagrams/check-popups.py /path/to/chrome-headless-shell
or set the environment variable CHROME. Any Chrome or Chromium binary that
knows --headless and --dump-dom works. On the computer of the owner it is
~/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell. It
needs system libraries that the computer does not have. They were unpacked
without sudo into ~/.cache/ccar-chrome-libs, from these Ubuntu 22.04 packages
(apt-get download, then dpkg-deb -x): libasound2 libatk-bridge2.0-0
libatk1.0-0 libatspi2.0-0 libdrm2 libgbm1 libnspr4 libnss3 libwayland-server0
libxcb-randr0 libxcomposite1 libxdamage1 libxfixes3 libxi6 libxkbcommon0
libxrandr2 libxrender1 libxshmfence1. So the full command there is:
    LD_LIBRARY_PATH=~/.cache/ccar-chrome-libs python3 docs/diagrams/check-popups.py \
        $(ls ~/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell)
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    chrome = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CHROME")
    if not chrome:
        print(__doc__)
        return 2
    with open(os.path.join(HERE, "check-popups.js"), encoding="utf-8") as f:
        check = f.read()
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        for path in sorted(glob.glob(os.path.join(HERE, "*.html"))):
            name = os.path.basename(path)
            with open(path, encoding="utf-8") as f:
                html = f.read()
            copy = os.path.join(tmp, name)
            with open(copy, "w", encoding="utf-8") as f:
                f.write(html.replace("</body>", '<script>addEventListener("load",()=>{' + check + "})</script></body>"))
            out = subprocess.run([chrome, "--headless", "--no-sandbox", "--dump-dom", "--virtual-time-budget=3000",
                                  "file://" + copy], capture_output=True, text=True, timeout=60).stdout
            m = re.search(r"<title>RESULT ([^<]*)", out)
            if not m:
                print("%s: no result" % name)
                bad += 1
                continue
            items = m.group(1).split()
            faults = [i for i in items if "NOT" in i or "OUTSIDE" in i]
            print("%s: %d parts, %d open, faults: %s" % (name, len([i for i in items if ":open" in i or ":NOT" in i and "CLOSED" not in i]),
                                                          len([i for i in items if ":open" in i]), " ".join(faults) or "none"))
            bad += len(faults)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
