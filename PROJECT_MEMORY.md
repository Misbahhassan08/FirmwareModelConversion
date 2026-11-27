# Persistent project memory — 2026-11-27
Goal: repeatable model conversion to RV1106G3 camera using known working reference. User wants detailed GitHub memory and exact compatible deployment files.
Reference identity and architecture in docs/REFERENCE.md. Original file yolov5(1).rknn; companions anchors_yolov5(2).txt and coco_80_labels_list(1).txt.
Custom checkpoint yolov5s_vehicle_registartionplate.pt: 14,395,055 bytes; SHA256 f0e81d4540d4cb91e7115f36a73eb2bc1a419d25d024d8e64080538319bf63a9. Training details: YOLOv5s, 150 epochs, 640 input, 2 classes vehicle and registration_plate, precision .769, recall .667. Prior checkpoint inspection reported FP16 stored weights, SiLU, depth .33 width .50, C3/SPPF, same anchors, recorded source commit af08ba156fd58ed5b0fe7e4e58a22c72c3cdd0ce. Export script independently asserts contract when executed. Dataset path and link omitted from public repository.
Decision: preserve SiLU first, export three post-sigmoid heads; alternative optimized ReLU requires validation/fine-tuning. Use toolkit 1.6.0 baseline. No fabricated RKNN.
Earlier status: conversion was initially pending; the subsequent hardware milestones below supersede this status.
Next: clone repo, place local checkpoint, get matching toolkit, prepare images, run export and compile, capture logs and tensor dump, adapt firmware if required, test against original PT, record results. Update this file and append run results on each future change. Repository is public; keep model binaries and dataset local unless explicitly authorized for publication.

## WSL continuation - 2026-11-27
Verified checkpoint and exported ONNX with the expected three raw sigmoid heads; ONNX checker and one-image raw PyTorch/ONNX parity passed. Toolkit 1.6.0 produced an ignored local smoke_test.rknn using two supplied images only. This is not a production calibration or validated camera model. Build required a local ONNX Runtime executable-stack flag fix on Ubuntu 26.04; see docs/RUN_LOG.md for hashes, logs and error. Next: collect representative camera calibration images, compare decoded detections and RKNN outputs, inspect firmware/runtime tensor attributes, test on device and measure held-out accuracy before deployment.

Camera startup log: preliminary RKNN initialized with expected 21-channel logical NHWC outputs; video encoder channel creation failed (errno 14) later in startup. Inference correctness, firmware decoder compatibility and cause of encoder failure are not established. See docs/RUN_LOG.md.
User reports encoder startup works after changing video resolution; subsequent resolution and firmware findings are recorded below. Quantitative detection accuracy remains unverified.
## Latest hardware milestone (2026-11-27)
See [hardware test](docs/HARDWARE_TEST_2026-11-27.md). Custom RKNN compiled and initialized successfully on camera; three NHWC INT8 heads with 21 channels verified. VENC fails EFAULT after VI starts. Inference and streaming unverified. Next: clean-boot original/custom comparison, memory/kernel logs, isolated inference, inspect firmware source. This supersedes earlier pending compilation status.

## Firmware source review
See [FIRMWARE_ANPR_REVIEW.md](docs/FIRMWARE_ANPR_REVIEW.md). Actual source already uses two classes and NHWC. Video resolution 2884x1624 differs from sensor 2592x1944; large DMA pools and NPU-first initialization are diagnostic targets. First test 1920x1080 with model input unchanged, log memory/stride and VENC return. Inference logging flag always false; BGR/padding mismatch and cleanup require attention. No root cause confirmed or firmware patch tested.

## Successful hardware milestone — 2026-11-27
User confirmed: changing DISP_WIDTH and DISP_HEIGHT makes the custom model work perfectly on RV1106G3. The recommended diagnostic resolution was 1920x1080, but the user has not explicitly confirmed the final numeric dimensions. Preserve current SiLU INT8 RKNN, two classes, 640x640 model input, three NHWC heads and original anchors. Resolution change resolved observed VENC failure; underlying memory/alignment/encoder mechanism remains unverified. No retraining or activation replacement required for this reported successful run. Quantitative accuracy, FPS, stability and exact final resolution remain to be recorded. This supersedes earlier pending hardware operation status. Do not change the working setup without a controlled test.

## Confirmed resolution baseline
1920x1080 works; 2592x1944 fails. User now targets 3MP streaming with same custom RKNN. Test 2304x1296 and intermediate modes per docs/RUN_LOG.md. Exact root cause still unverified.

## OCR next phase
User wants on-camera plate text recognition alongside working detector. Proposed LPRNet second RKNN model, standalone validation first, local plate alphabet fine-tuning and dual-model memory testing. See [OCR roadmap](docs/OCR_ROADMAP.md). Not implemented yet.

## OCR V1 source package
See [OCR_V1_IMPLEMENTATION.md](docs/OCR_V1_IMPLEMENTATION.md). Full modified firmware source delivered locally; optional standalone and live OCR, training and conversion scripts. Host C++ syntax/CTC test and Python syntax passed; OCR model compilation, ARM build and physical testing pending. Existing detector unchanged; 1080p default. No proprietary source or model uploaded to public repo.
