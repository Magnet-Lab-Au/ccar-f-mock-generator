"""The light and dark button of the sample pages. The owner asked for it on 13 October 2026.

The page follows the device setting until the reader presses the button. Then the
class "light" or "dark" on <html> decides, and the page keeps the choice in
localStorage. A script in <head> sets the class before the page draws, so the
page does not flash in the wrong scheme.
"""

KEY = "academy-theme"

HEAD = ("<script>try{var t=localStorage.getItem('%s');"
        "if(t==='dark'||t==='light')document.documentElement.classList.add(t)}catch(e){}</script>" % KEY)

BUTTON = '<button type="button" class="theme-btn" id="theme-btn">Dark mode</button>'

JS = """<script>
(() => {
  const root = document.documentElement, btn = document.getElementById('theme-btn');
  const device = matchMedia('(prefers-color-scheme: dark)');
  const dark = () => root.classList.contains('dark') || (!root.classList.contains('light') && device.matches);
  const label = () => { btn.textContent = dark() ? 'Light mode' : 'Dark mode'; };
  btn.addEventListener('click', () => {
    const next = dark() ? 'light' : 'dark';
    root.classList.remove('light', 'dark'); root.classList.add(next);
    try { localStorage.setItem('%s', next); } catch (e) {}
    label();
  });
  device.addEventListener('change', label);
  label();
})();
</script>""" % KEY


def scheme_css(dark_vars):
    """The dark variables apply when the device is dark and the reader did not choose light, or when the reader chose dark."""
    return ("@media (prefers-color-scheme: dark) { :root:not(.light) { %s } }\n"
            ":root.dark { %s }\n"
            ":root.light { color-scheme: light; } :root.dark { color-scheme: dark; }\n"
            "@media print { .theme-btn { display: none; } }\n") % (dark_vars, dark_vars)
