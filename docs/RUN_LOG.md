# Conversion test log
## 2026-11-27 — initial baseline
Reference camera operation: user reported working. Reference binary and custom checkpoint hashes verified from uploaded files. Conversion script syntax previously checked; no actual compiler run, no ONNX parity test, no custom RKNN hardware test. No representative calibration images supplied.
## Template for next test
- Date / operator / repository commit:
- Host OS, Python, torch, ONNX, RKNN toolkit:
- Camera board, firmware, driver/runtime:
- Checkpoint / ONNX / RKNN SHA256:
- Calibration dataset identifier and count:
- Logical and native tensor attributes:
- Export parity, build result, logs:
- PT vs RKNN precision, recall, mAP, plate recall:
- Inference FPS/latency and stability:
- Decision / known issues / rollback:

## 2026-11-27 - WSL setup attempt
- Repository baseline: afc31117d259d258f11b572bcb10ceefe2063919; Ubuntu 26.04.1 LTS WSL2 x86_64, kernel 6.18.58.1, system Python 3.14.4.
- Local Python 3.8.20 compiler and 3.11.18 export environments created; dependency installation and import verification pending. YOLOv5 source checked out at af08ba156fd58ed5b0fe7e4e58a22c72c3cdd0ce.
- Official rknn-toolkit2 v1.6.0 source commit b25dadacc24b88eb7dfcaa47c9c525ecca89b319. cp38 wheel SHA-256 fb79c8fd67fd035997cd10ac4675f1e36bdddf6fb17ef802de7fdf5c864ef70b.
- No checkpoint or calibration images found in vehicle directory. Export, ONNX parity, custom RKNN build, camera inference and accuracy remain untested. Preserve original reference.
- Checkpoint supplied locally and verified: f0e81d4540d4cb91e7115f36a73eb2bc1a419d25d024d8e64080538319bf63a9. Copied to ignored vehicle/best.pt; checkpoint directory added to .gitignore to protect local metadata.
- Two user-provided JPEG samples downloaded into ignored vehicle/images and prepared successfully with prepare_calibration.py --count 2. This is smoke-test data, not representative production calibration or labeled accuracy validation.
- Export dependencies installed (Python 3.11.18, torch 2.15.0+cpu, ONNX 1.23.2, ONNX Runtime 1.32.0); export launched with local export.log. Toolkit dependency install and export still in progress at time of entry; neither compilation nor parity nor hardware results are established.
- Initial export failed with Python 3.11 missing pathlib._local; export_model.py now maps that Python 3.13+ pickle module to pathlib on older Python. Script SHA-256 a9a64be0ec0b9551e0a40906eac99fb7962dc7ac7d3a215be786d808a9671a32. Retry passed checkpoint class/anchor/stride/output assertions and ONNX checker.
- ONNX size 28098005 bytes; SHA-256 7ff656217965882f14219cee55c8ac6cca5ced91a8f6cf73e93d65b80da92c5b. Raw PyTorch vs ONNX output parity on one supplied image passed rtol 1e-4, atol 1e-5; maximum absolute errors by head: 7.53998756e-06, 1.03414059e-05, 6.34789467e-06. Decoded-box parity remains pending.
- RKNN 1.6.0 import passed. Initial build failed on ONNX Runtime executable-stack loader error under Ubuntu 26.04; local patchelf 0.19.3.0 cleared that flag on the environment copy of onnxruntime 1.16.0 shared library (modified SHA-256 707f644b9b68b85eaeca249d2a61dac7cfdec72a05e392cadf22f631286a8e0e). Build retry succeeded, using only two smoke-test images. Toolkit warned about ONNX opset 12; no opset change made without parity testing. Logs are local in vehicle/*.log.
- smoke_test.rknn size 7954824 bytes; SHA-256 80cb777f26b2a2d38791c95e69c973fd4007b590087e9034755dd4185633dd04. Not production calibrated or validated. RKNN output comparison, firmware compatibility, runtime tensor attributes, real-device inference, accuracy, performance and rollback checks remain pending.
- Prepared local mai/ camera test package: yolov5.rknn copied from smoke_test.rknn (SHA-256 80cb777f26b2a2d38791c95e69c973fd4007b590087e9034755dd4185633dd04), anchors_yolov5.txt and vehicle_registrationplate_labels.txt copied from vehicle/. This remains a two-image calibration smoke test; camera compatibility and accuracy are unvalidated. Firmware filenames and two-class decoding must be verified before deployment.

## 2026-11-27 - camera startup log with preliminary model
- User-supplied camera log reports RKNN initialization success. Input: NHWC INT8 [1,640,640,3]; outputs: NHWC INT8 [1,80,80,21], [1,40,40,21], [1,20,20,21]; each reported zp -128 and scale 0.003922. These are reported logical attributes, not proof of native buffer layout or correct postprocessing.
- ISP reports successful init/prepare/start and stream-on. Subsequently MPP encoder VCODEC_CHAN_CREATE and VCODEC_CHAN_START fail with errno 14 (Bad address), followed by hw create failed and init venc failed. Root cause not established; log does not show inference results or accuracy.
- Firmware loads ./model/coco_80_labels_list.txt; verify contents and two-class decoder, buffer indexing, preprocessing and output quantization handling. Compare encoder startup with original model and request firmware source, runtime/driver versions and complete logs. Keep test model separate and retain rollback.
- User subsequently reports that changing the video resolution resolved the encoder startup issue; subsequent resolution and firmware findings are recorded below; quantitative detection accuracy remains unverified.
## Latest hardware milestone (2026-11-27)
See [hardware test](HARDWARE_TEST_2026-11-27.md). Custom RKNN compiled and initialized successfully on camera; three NHWC INT8 heads with 21 channels verified. VENC fails EFAULT after VI starts. Inference and streaming unverified. Next: clean-boot original/custom comparison, memory/kernel logs, isolated inference, inspect firmware source. This supersedes earlier pending compilation status.

## Successful hardware milestone — 2026-11-27
User confirmed: changing DISP_WIDTH and DISP_HEIGHT makes the custom model work perfectly on RV1106G3. The recommended diagnostic resolution was 1920x1080, but the user has not explicitly confirmed the final numeric dimensions. Preserve current SiLU INT8 RKNN, two classes, 640x640 model input, three NHWC heads and original anchors. Resolution change resolved observed VENC failure; underlying memory/alignment/encoder mechanism remains unverified. No retraining or activation replacement required for this reported successful run. Quantitative accuracy, FPS, stability and exact final resolution remain to be recorded. This supersedes earlier pending hardware operation status. Do not change the working setup without a controlled test.

## Resolution confirmation — 2026-11-27
User explicitly confirmed 1920x1080 works perfectly and 2592x1944 fails again. 2884x1624 previously failed at VENC creation. 2592x1944 is 5.04 MP, not 3 MP. Target 2304x1296 (2.99 MP), alternative 2048x1536 (3.15 MP). Controlled test ladder: 2048x1152, 1920x1440, 2304x1296, 2048x1536, 2400x1350, 2560x1440; all untested. Keep RKNN 640x640, encoder settings and model unchanged initially. If failure collect CMA/kernel logs and inspect encoder virtual stride, pixel format and DMA allocations. No guarantee of higher resolution until tested. Luckfox references: https://wiki.luckfox.com/Core1106/Introduction/ and https://wiki.luckfox.com/Luckfox-Pico-Pro-Max/CSI-Camera/ .
