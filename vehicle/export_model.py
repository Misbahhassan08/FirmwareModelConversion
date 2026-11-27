"""Export trusted YOLOv5 checkpoint without decoded Detect output."""
import argparse, sys, inspect, pathlib
from pathlib import Path
from types import MethodType
import torch
p=argparse.ArgumentParser()
p.add_argument('--yolov5',required=True)
p.add_argument('--weights',default='best.pt')
p.add_argument('--output',default='vehicle_registrationplate.onnx')
a=p.parse_args()
sys.path.insert(0,str(Path(a.yolov5).resolve()))
# Checkpoints saved on Python 3.13+ can reference pathlib._local, while
# Python 3.11 exposes the same path classes directly from pathlib.
if sys.version_info < (3, 13):
    sys.modules.setdefault('pathlib._local', pathlib)
ckpt=torch.load(a.weights,map_location='cpu',weights_only=False)
model=ckpt.get('ema') or ckpt['model']
model=model.float().eval()
head=model.model[-1]
assert head.nc==2 and head.nl==3 and head.na==3
assert list(map(int,head.stride.tolist()))==[8,16,32]
anchors=(head.anchors.detach().cpu()*head.stride.cpu().view(-1,1,1)).flatten()
expected=torch.tensor([10,13,16,30,33,23,30,61,62,45,59,119,116,90,156,198,373,326],dtype=torch.float32)
assert torch.allclose(anchors,expected), f'Anchor mismatch: {anchors}'
assert [model.names[i] for i in range(2)]==['vehicle','registration_plate']
def raw_forward(self,x):
    return tuple(self.m[i](x[i]).sigmoid() for i in range(self.nl))
head.forward=MethodType(raw_forward,head)
x=torch.zeros(1,3,640,640)
with torch.no_grad():
    out=model(x)
    assert [tuple(y.shape) for y in out]==[(1,21,80,80),(1,21,40,40),(1,21,20,20)]
    kwargs={'dynamo':False} if 'dynamo' in inspect.signature(torch.onnx.export).parameters else {}
    torch.onnx.export(model,x,a.output,opset_version=12,input_names=['images'],output_names=['output0','output1','output2'],do_constant_folding=True,**kwargs)
import onnx
onnx.checker.check_model(onnx.load(a.output))
print('Exported and checked:',a.output)
