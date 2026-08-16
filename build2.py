# -*- coding: utf-8 -*-
"""Собирает game.html из src2.html: вшивает three.js, GLTFLoader и лицо."""
import base64, io, sys
from PIL import Image, ImageEnhance

TMP = r"C:\Users\eltom\AppData\Local\Temp\claude"

im = Image.open("Screenshot_300.png").convert("RGB").crop((35,15,470,450)).resize((256,256), Image.LANCZOS)
im = ImageEnhance.Brightness(im).enhance(1.25)
im = ImageEnhance.Contrast(im).enhance(1.12)
buf = io.BytesIO(); im.save(buf, "JPEG", quality=84)
face = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

three  = io.open(TMP + r"\three147.min.js", encoding="utf-8").read()
loader = io.open(TMP + r"\GLTFLoader.js",  encoding="utf-8").read()

h = io.open("src2.html", encoding="utf-8").read()
h = h.replace("__THREE__", three).replace("__LOADER__", loader).replace("__FACE__", face)
io.open("game.html", "w", encoding="utf-8").write(h)
print("built", round(len(h.encode())/1024), "KB")

# тестовая сборка с автопилотом
frames = int(sys.argv[1]) if len(sys.argv) > 1 else 600
bot = """<script>
setTimeout(function(){
  if(document.getElementById('load').style.display!=='none'){ document.title='ASSETS NOT LOADED'; }
  startGame();
  for(var i=0;i<%d;i++){
    var best=null,bd=1e9;
    for(var k=0;k<spots.length;k++){ var s=spots[k]; if(!s.alive) continue;
      var d=Math.hypot(s.x-player.position.x,s.z-player.position.z); if(d<bd){bd=d;best=s;} }
    for(var k=0;k<props.length;k++){ var p=props[k]; if(!p.alive||p.suck>0||p.tier>G.tier) continue;
      var d=Math.hypot(p.x-player.position.x,p.z-player.position.z); if(d<bd){bd=d;best=p;} }
    if(best){ var dx=best.x-player.position.x, dz=best.z-player.position.z, l=Math.hypot(dx,dz)||1;
      stick={bx:0,by:0,dx:dx/l*70,dy:dz/l*70}; }
    step(1/60); if(G.over) break;
  }
  var d=document.createElement('div');
  d.style.cssText='position:fixed;left:6px;bottom:100px;z-index:99;background:#000c;color:#0f0;font:12px monospace;padding:6px';
  d.textContent='eaten='+G.eaten+' kg='+Math.round(G.kg)+' r='+G.r.toFixed(1)+' tier='+G.tier+
    ' houses='+G.houses+' models='+Object.keys(MODELS).length;
  document.body.appendChild(d);
}, 2500);
</script>""" % frames
io.open("_t.html", "w", encoding="utf-8").write(h.replace("</body>", bot + "</body>"))
print("test build ok")
