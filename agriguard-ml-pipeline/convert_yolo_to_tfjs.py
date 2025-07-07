from ultralytics import YOLO
model = YOLO('yolo_classification/finetune_experiment/weights/best.pt')
model.export(format='tfjs',)
