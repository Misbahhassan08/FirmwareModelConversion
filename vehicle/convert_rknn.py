import argparse
from pathlib import Path
from rknn.api import RKNN
p=argparse.ArgumentParser(); p.add_argument('--onnx',default='vehicle_registrationplate.onnx'); p.add_argument('--dataset',default='dataset.txt'); p.add_argument('--output',default='yolov5.rknn'); a=p.parse_args()
assert Path(a.onnx).is_file(), 'Missing ONNX export'
lines=[s.strip() for s in Path(a.dataset).read_text().splitlines() if s.strip()]
assert lines and all(Path(s).is_file() for s in lines), 'Calibration images missing'
rknn=RKNN(verbose=True)
def check(ret,step):
    if ret != 0: raise RuntimeError(f'{step} failed: {ret}')
try:
    check(rknn.config(target_platform='rv1106',mean_values=[[0,0,0]],std_values=[[255,255,255]],quantized_dtype='asymmetric_quantized-8'),'config')
    check(rknn.load_onnx(model=a.onnx),'load_onnx')
    check(rknn.build(do_quantization=True,dataset=a.dataset),'build')
    check(rknn.export_rknn(a.output),'export')
    print('Compiled:',a.output)
finally:
    rknn.release()
