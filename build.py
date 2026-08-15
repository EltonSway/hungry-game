from PIL import Image, ImageEnhance
import base64, io, sys
im=Image.open('Screenshot_300.png').convert('RGB').crop((35,15,470,450)).resize((256,256), Image.LANCZOS)
im=ImageEnhance.Brightness(im).enhance(1.25); im=ImageEnhance.Contrast(im).enhance(1.12)
buf=io.BytesIO(); im.save(buf,'JPEG',quality=84)
face='data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()
three=open(r'C:\Users\eltom\AppData\Local\Temp\claude\three.min.js',encoding='utf-8').read()
h=open('src.html',encoding='utf-8').read().replace('__THREE__',three).replace('__FACE__',face)
open('game.html','w',encoding='utf-8').write(h)
frames=int(sys.argv[1]) if len(sys.argv)>1 else 600
bot=r'''<script>
setTimeout(()=>{
  startGame();
  for(let i=0;i<%d;i++){
    const o=spots.filter(s=>s.alive).sort((a,b)=>
      Math.hypot(a.x-player.position.x,a.z-player.position.z)-Math.hypot(b.x-player.position.x,b.z-player.position.z))[0];
    if(o){ const dx=o.x-player.position.x, dz=o.z-player.position.z, l=Math.hypot(dx,dz)||1;
      stick={bx:0,by:0,dx:dx/l*70,dy:dz/l*70}; }
    step(1/60); if(G.over) break;
  }
  const d=document.createElement('div');
  d.style.cssText='position:fixed;left:6px;bottom:100px;z-index:99;background:#000c;color:#0f0;font:12px monospace;padding:6px';
  d.textContent='eaten='+G.eaten+' kg='+Math.round(G.kg)+' r='+G.r.toFixed(1)+' bc='+G.bestCombo.toFixed(1)+' over='+G.over;
  document.body.appendChild(d);
}, 900);
</script>''' % frames
open('_t.html','w',encoding='utf-8').write(h.replace('</body>',bot+'</body>'))
print('built', round(len(h.encode())/1024),'KB')
