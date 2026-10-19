/* starts the portal form of the tab on its element, as the React page of the portal will */
import { start } from '../src/academy.ts';
const tab = document.body.dataset.tab, root = document.getElementById('ap');
const [body, data] = await Promise.all([fetch('../src/' + tab + '.body.html').then((r) => r.text()), import('../src/' + tab + '.data.ts')]);
root.innerHTML = body;
window.ACADEMY = data.default;   // only for check-pages.js, which reads the popups of Fig. A there
let stop = start(root, data.default);
stop(); stop = start(root, data.default);   // twice, as React StrictMode does
