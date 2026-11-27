import argparse, random
from pathlib import Path
import cv2
p=argparse.ArgumentParser(); p.add_argument('images'); p.add_argument('--count',type=int,default=200); a=p.parse_args()
files=sorted(x for x in Path(a.images).rglob('*') if x.suffix.lower() in {'.jpg','.jpeg','.png','.bmp'})
random.Random(42).shuffle(files)
out=Path('calibration_640'); out.mkdir(exist_ok=True); paths=[]
for f in files:
    if len(paths)>=a.count: break
    im=cv2.imread(str(f))
    if im is None: continue
    h,w=im.shape[:2]; r=min(640/w,640/h); nw,nh=round(w*r),round(h*r)
    im=cv2.resize(im,(nw,nh)); dw,dh=640-nw,640-nh
    im=cv2.copyMakeBorder(im,dh//2,dh-dh//2,dw//2,dw-dw//2,cv2.BORDER_CONSTANT,value=(114,114,114))
    dest=out/f'{len(paths):04d}.png'
    if cv2.imwrite(str(dest),im): paths.append(str(dest.resolve()))
if not paths: raise SystemExit('No readable images')
Path('dataset.txt').write_text('\n'.join(paths)+'\n'); print(f'{len(paths)} calibration images')
