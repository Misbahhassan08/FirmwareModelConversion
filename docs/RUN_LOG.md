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

## Latest hardware milestone (2026-11-27)
See [hardware test](HARDWARE_TEST_2026-11-27.md). Custom RKNN compiled and initialized successfully on camera; three NHWC INT8 heads with 21 channels verified. VENC fails EFAULT after VI starts. Inference and streaming unverified. Next: clean-boot original/custom comparison, memory/kernel logs, isolated inference, inspect firmware source. This supersedes earlier pending compilation status.

## Successful hardware milestone — 2026-11-27
User confirmed: changing DISP_WIDTH and DISP_HEIGHT makes the custom model work perfectly on RV1106G3. The recommended diagnostic resolution was 1920x1080, but the user has not explicitly confirmed the final numeric dimensions. Preserve current SiLU INT8 RKNN, two classes, 640x640 model input, three NHWC heads and original anchors. Resolution change resolved observed VENC failure; underlying memory/alignment/encoder mechanism remains unverified. No retraining or activation replacement required for this reported successful run. Quantitative accuracy, FPS, stability and exact final resolution remain to be recorded. This supersedes earlier pending hardware operation status. Do not change the working setup without a controlled test.
