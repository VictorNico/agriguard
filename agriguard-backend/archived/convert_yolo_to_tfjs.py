from ultralytics import YOLO
model = YOLO('weights/best.pt')
model.export(format='tfjs',)
