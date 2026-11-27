# Golden reference: RV1106G3
User reports original yolov5(1).rknn works perfectly on physical cameras. Never overwrite it.
## Identity
- 7,589,751 bytes; SHA256 7e72c8caa060ea15d69109e4af6c1f80005cbd1be14bbe1f6f2af9175861c44a.
- Embedded version 1.6.0+81f21f4d; compiler 1.6.0 (585b3edcf@2023-12-11T07:37:51).
- Target rv1106, static logical ONNX input images [1,3,640,640], mean 0/std 255, RGB convention to verify.
- INT8 asymmetric quantization; runtime scale and zero point must be queried, never copied from another model.
## Architecture
Prior binary inspection found ConvSP stem, ConvRelu, ConvReluAdd, Concat, MaxPool, Resize and three ConvSigmoid outputs. CSP/C3 backbone repeat pattern 1/2/3/1, FPN/PAN neck and modified spatial pooling are reconstructed; exact intermediate graph/channel widths not fully verified. Six named MaxPool operators need not mean six source-level pools; compiler lowering can split operations. ConvSP may be compiler transformation, not necessarily a custom training module. Likely YOLOv5s but exact variant not conclusively proven.
Logical outputs: output0 [1,255,80,80], 286 [1,255,40,40], 288 [1,255,20,20]. Embedded sigmoid; external anchor decoding and NMS. 3 anchors per cell, stride 8/16/32; 25,200 candidates. Native physical dimensions/layout can differ.
## Anchor contract
P3: (10,13), (16,30), (33,23).
P4: (30,61), (62,45), (59,119).
P5: (116,90), (156,198), (373,326).
Original text format is one decimal number per line, 18 values. Preserve order. Original labels are 80 COCO classes; custom labels differ.
## Decoder
For dequantized sigmoid values p and grid g: center=(2*p-0.5+g)*stride; size=(2*p)^2*anchor. Score=objectness*class probability. Class-aware NMS and inverse letterbox. No additional sigmoid. If native tensor layout is blocked/padded, unpack using actual SDK attributes before indexing.
## Exactness
Compatibility means equivalent output semantics and correct firmware loading, not byte-identical output to the COCO reference. Custom weights/classes require different tensor channels, names may differ. Compiler and runtime exact versions, firmware source, physical layouts, calibration and target hardware results remain to be captured.
