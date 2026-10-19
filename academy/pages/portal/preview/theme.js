/* as the portal's theme-init.js: dark from the device setting when nothing is stored */
if (matchMedia('(prefers-color-scheme: dark)').matches) document.documentElement.classList.add('dark');
if (new URLSearchParams(location.search).get('shell') === '0') document.documentElement.classList.add('bare');
