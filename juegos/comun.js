/* Utilidades comunes de los juegos nuevos del Angelito Burlón */
window.AB = (() => {
  const guarda = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  let ac = null;
  function nota(f, d = .2, c = 0, tipo = 'triangle', vol = .09) {
    try {
      ac = ac || new (window.AudioContext || window.webkitAudioContext)();
      if (ac.state === 'suspended') ac.resume();
      const t = ac.currentTime + c, o = ac.createOscillator(), g = ac.createGain();
      o.type = tipo; o.frequency.value = f;
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(vol, t + .01); g.gain.exponentialRampToValueAtTime(.0001, t + d);
      o.connect(g).connect(ac.destination); o.start(t); o.stop(t + d + .05);
    } catch (e) {}
  }
  const bien = () => [660, 880, 1100].forEach((f, i) => nota(f, .25, i * .08));
  const mal = () => { nota(220, .25, 0, 'sine'); nota(196, .3, .12, 'sine'); };
  const fanfarria = () => [523, 659, 784, 1047].forEach((f, i) => nota(f, .35, i * .14));
  const baraja = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  // Panel final: necesita #final, #textoFinal y #otraVez en la página
  function fin(texto) {
    fanfarria();
    const p = document.getElementById('final');
    document.getElementById('textoFinal').textContent = texto;
    p.hidden = false; document.getElementById('otraVez').focus();
    lluvia();
  }
  function lluvia() { // estrellitas que caen al ganar
    const c = document.createElement('div'); c.setAttribute('aria-hidden', 'true');
    c.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:30;overflow:hidden';
    for (let i = 0; i < 28; i++) {
      const s = document.createElement('span'); s.textContent = '★';
      s.style.cssText = `position:absolute;left:${Math.random() * 100}%;top:-40px;font-size:${14 + Math.random() * 22}px;color:${['#f5c451', '#ffe7a3', '#fff', '#ff9ec4'][i % 4]};animation:caer ${1.8 + Math.random() * 1.6}s ${Math.random() * .8}s ease-in forwards`;
      c.appendChild(s);
    }
    if (!document.getElementById('estiloCaer')) {
      const st = document.createElement('style'); st.id = 'estiloCaer';
      st.textContent = '@keyframes caer{to{transform:translateY(110vh) rotate(540deg);opacity:.2}}@media (prefers-reduced-motion:reduce){[aria-hidden] span{animation:none!important;display:none}}';
      document.head.appendChild(st);
    }
    document.body.appendChild(c); setTimeout(() => c.remove(), 4200);
  }
  const ESTRELLA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 1.5l2.7 6.8 7.3.5-5.6 4.7 1.8 7.1L12 16.7l-6.2 3.9 1.8-7.1L2 8.8l7.3-.5z"/></svg>';
  // Botones de nivel: [data-nivel] con aria-pressed
  function niveles(clave, porDefecto, alCambiar) {
    let n = guarda.get(clave, porDefecto);
    const bs = document.querySelectorAll('[data-nivel]');
    const marca = () => bs.forEach(b => { const si = b.dataset.nivel === String(n); b.classList.toggle('sec', !si); b.setAttribute('aria-pressed', si); });
    bs.forEach(b => b.addEventListener('click', () => { n = b.dataset.nivel; guarda.set(clave, n); marca(); alCambiar(n); }));
    marca(); return n;
  }
  return { guarda, nota, bien, mal, fanfarria, baraja, fin, lluvia, ESTRELLA, niveles };
})();
