# FirmwareModelConversion — MexemAi
Persistent engineering knowledge base for converting trained YOLOv5 detectors to camera-ready Rockchip RV1106G3 RKNN models.

## Start here
- [Reference architecture](docs/REFERENCE.md): immutable known-working model contract.
- [Conversion guide](docs/CONVERSION.md): Ubuntu/VS Code workflow and exact output requirements.
- [Validation and troubleshooting](docs/VALIDATION.md): numerical checks, native tensor layout, deployment and rollback.
- [Project memory](PROJECT_MEMORY.md): decisions, status and handoff for future chats.
- [Vehicle model scripts](vehicle/): two-class conversion implementation.

Status: reference RKNN works on user's cameras (user reported); custom checkpoint inspected; conversion scripts prepared, actual ONNX/RKNN compilation and hardware test pending. No generated RKNN is claimed to exist.

This repository is public. Original trained weights, compiled reference binary, private dataset images and local paths are not committed. Keep them locally; verify SHA-256 against reference documentation. Do not upload proprietary assets without checking rights and visibility.

Future work: read PROJECT_MEMORY.md and reference documents before changing conversion or firmware; record every test, version, failure and decision, preserving working reference.
