from ultralytics import YOLO

model = YOLO("yolov10s.pt")

model.export(format="onnx")
