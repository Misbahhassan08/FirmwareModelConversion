# Verification gates and troubleshooting
1. Baseline: record working camera firmware/SDK, librknnrt version, model SHA256, test images, output shapes/types/scales/zero points, latency and detections. Back up original binary and labels.
2. Source: verify checkpoint hash, class order, anchors, strides, image preprocessing. Original reported precision .769, recall .667; not independently measured. Establish labeled held-out baseline including small plates and negatives.
3. ONNX: verify checker, inspect inputs/outputs and compare three raw sigmoid maps to PyTorch using same normalized image. Compare decoded boxes to original Detect output, before NMS and after NMS. Use tolerance justified by numeric precision; do not silently accept wrong scores.
4. RKNN: verify actual successful build, file size/hash, runtime API and driver versions. Query RKNN_QUERY_IN_OUT_NUM, RKNN_QUERY_INPUT_ATTR, RKNN_QUERY_OUTPUT_ATTR and native attributes if supported. Capture name, dims, fmt, type, n_elems, size, size_with_stride, w_stride, zp, scale, qnt_type. Three logical outputs expected, each 21 channels. Native layout may be NHWC or blocked NC1HWC2; use correct unpacking and alignment rather than assuming contiguous NCHW. Query scale and zero point separately for each head. Dequantize (q-zp)*scale.
5. Firmware: OBJ_CLASS_NUM=2, PROP_BOX_SIZE=7, replace hardcoded 80/85/255, check label allocation and file paths, output indexing and buffer sizes. For contiguous NCHW index=(anchor*7+attribute)*H*W+y*W+x. Native layouts require different indexing. Preserve anchors and sigmoid semantics. Score threshold and class-aware NMS; overlapping vehicle and plate should not suppress each other. Undo exact letterbox.
6. Hardware: use a separate test model path first, verify init and return codes, same images against original PT and ONNX, record detection confidence/box coordinates and actual FPS, latency, memory, temperature and stability. Compare held-out precision/recall/mAP, especially plate recall; agree acceptable regression before production. Roll back if init fails or detections degrade.
## Symptoms
- Init error: target/compiler/runtime incompatibility, wrong binary or corrupt transfer.
- All-zero outputs: unsupported operators, quantization, tensor layout, preprocessing or driver mismatch.
- Boxes misplaced: anchors/stride/order, duplicate sigmoid, letterbox inversion or indexing.
- No plate detections: class count/labels, NMS crossing classes, threshold, calibration distribution or original training limitations.
- Crash: 80-class assumptions or native padded buffer mishandling.
## Record every run
Date; device/firmware; git commit; Python/Torch/ONNX/toolkit versions; weights/ONNX/RKNN hashes; calibration dataset ID; tensor dump; thresholds; accuracy metrics; FPS; failure logs; decision and rollback status. Mark untested values pending, never invent metrics.
