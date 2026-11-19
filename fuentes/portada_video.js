// Fotografía fuentes/portada_video.html a 1280×720 y la guarda como video/angelito_burlon.jpg
// Uso (desde la carpeta de la web): node fuentes/portada_video.js   (necesita Playwright y Pillow/python3)
const {chromium}=require('playwright');const path=require('path');const {execFileSync}=require('child_process');
(async()=>{const raiz=path.resolve(__dirname,'..');const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1280,height:720}});
  await p.goto('file://'+path.join(raiz,'fuentes/portada_video.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
  const png=path.join(raiz,'fuentes/portada_video.png');await p.screenshot({path:png});await b.close();
  execFileSync('python3',['-c',`from PIL import Image;Image.open(${JSON.stringify(png)}).convert('RGB').save(${JSON.stringify(path.join(raiz,'video/angelito_burlon.jpg'))},quality=86,optimize=True,progressive=True)`]);
  console.log('video/angelito_burlon.jpg lista')})();
