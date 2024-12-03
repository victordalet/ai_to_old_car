from ultralytics import YOLO

model = YOLO("yolov10s")

model.export(format="onnx")
