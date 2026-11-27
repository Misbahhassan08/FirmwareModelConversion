# Reproducible conversion in VS Code
## 1. Host setup
Use x86_64 Ubuntu (native or WSL2 with VS Code Remote WSL; verify toolkit wheel support). Do not attempt compiler installation on the ARM camera. Clone repository and open vehicle/ in terminal.
```sh
git clone https://github.com/Misbahhassan08/FirmwareModelConversion.git
cd FirmwareModelConversion/vehicle
git clone https://github.com/ultralytics/yolov5.git
git -C yolov5 checkout af08ba156fd58ed5b0fe7e4e58a22c72c3cdd0ce
python3 -m venv .venv-export
source .venv-export/bin/activate
python -m pip install -r yolov5/requirements.txt
python -m pip install onnx
```
Recorded commit is from prior checkpoint analysis; if checkout fails obtain original training source. Use trusted checkpoint only because torch pickle executes code. Place original yolov5s_vehicle_registartionplate.pt as vehicle/best.pt. Verify hash in PROJECT_MEMORY.md. Select export venv in VS Code. Freeze working dependencies after successful run.
## 2. Export
```sh
python export_model.py --yolov5 yolov5
```
Script asserts classes, anchor dimensions and strides, then overrides Detect.forward to return three sigmoid-activated convolution outputs, without grid decode, flattening or NMS. Preserve trained SiLU. Expected input [1,3,640,640]; outputs [1,21,80,80], [1,21,40,40], [1,21,20,20]. ONNX opset 12. Check ONNX graph and compare PyTorch and ONNX outputs on real input before compilation. Output names output0/1/2 differ from original reference names; firmware should use index and verified shape, not fixed names.
## 3. Calibration
Collect representative 100–300 real images with varied distance, plates, exposure, angle and negative scenes. Keep separate labeled validation set. Calibration does not need labels. Match actual camera resize/color/padding, currently letterbox 114 assumed.
```sh
python prepare_calibration.py /absolute/path/to/images --count 200
```
Creates calibration_640/ and dataset.txt with absolute paths. OpenCV writes BGR image files normally; verify RKNN loader and camera RGB channel handling against actual inference. Do not normalize twice.
## 4. Compiler environment
Install official RKNN Toolkit2 1.6.0 wheel and its matching requirements in a separate supported Python venv (e.g. Python 3.8 if wheel tagged cp38). Official repository https://github.com/rockchip-linux/rknn-toolkit2 ; use matching release archive and SDK instructions, not arbitrary latest wheel. Confirm import, version, architecture and wheel tag. Activate compiler venv in same vehicle directory.
```sh
python -c "from rknn.api import RKNN; print('import OK')"
python convert_rknn.py 2>&1 | tee build.log
```
Target rv1106, mean [0,0,0], std [255,255,255], asymmetric_quantized-8, build with calibration dataset. Output yolov5.rknn. Check exit code (use set -o pipefail) and output file exists. Record compiler version/hash and build log.
## 5. Alternative route
If SiLU or 6x6 stem fails or produces wrong outputs, inspect unsupported operators and SDK logs. Try compatible mathematically equivalent export rewrites first. If necessary use Rockchip optimized YOLOv5 (https://github.com/airockchip/yolov5) and transfer/fine-tune weights with original dataset; never swap ReLU blindly. Re-export, recalibrate and compare precision/recall/mAP.
## 6. Deployment contract
Copy generated yolov5.rknn, anchors_yolov5.txt and vehicle_registrationplate_labels.txt (or coco_80_labels_list.txt only if firmware expects that legacy name). Two classes vehicle, registration_plate; 7 values per anchor, 21 logical channels. Existing firmware may need rebuilding. See VALIDATION.md. No model-only swap guarantee.
