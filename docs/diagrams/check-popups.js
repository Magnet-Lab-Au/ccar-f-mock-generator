// Checks that each hot element opens its popup, the popup stays in the window, and Escape closes it.
const els=[...document.querySelectorAll('[data-step]')]; const out=[];
for (const el of els){ el.dispatchEvent(new MouseEvent('click',{bubbles:true}));
  const p=document.getElementById('pop'); const r=p.getBoundingClientRect();
  const ok=!p.hidden && document.getElementById('poptitle').textContent.length>0;
  out.push(el.dataset.step+':'+(ok?'open':'NOT')+(r.right<=innerWidth+1&&r.left>=-1?'':' OUTSIDE'));
  document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));
  if(!p.hidden) out.push(el.dataset.step+':NOT-CLOSED'); }
document.title='RESULT '+out.join(' ');
