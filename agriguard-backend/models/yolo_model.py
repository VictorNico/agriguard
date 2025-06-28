from ultralytics import YOLO
import cv2
import numpy as np
import os
class PestDetector:
    def __init__(self, model_path='weights/yolo11s.pt'):
        self.model_path = model_path
        self.model = None
        self.model_loaded = False
        self.load_model()

    def load_model(self):
        try:
            self.model = YOLO(f"{os.getcwd()}/{self.model_path}")
            self.model_loaded = True
            print("✅ Modèle YOLO chargé avec succès")
        except Exception as e:
            print(f"❌ Erreur chargement modèle: {e}")
            self.model_loaded = False

    def detect(self, image):
        if not self.model_loaded:
            return []

        try:
            # Lancer la détection
            results = self.model(image, conf=0.3)

            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Extraction des données
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        bbox = box.xyxy[0].tolist()

                        # Mapping classe → nom ravageur (à adapter)
                        class_names = {
                            0: "legionnaire_automne",
                            1: "bruche_niebe",
                            2: "cochenille_manioc"
                        }
                        print(result.names.get(class_id, f"pest_{class_id}"))
                        detection = {
                            "name": result.names.get(class_id, result.names.get(class_id, f"pest_{class_id}")),
                            "class": class_names.get(class_id, result.names.get(class_id, f"pest_{class_id}")),
                            "confidence": round(confidence, 2),
                            "bbox": [round(x, 2) for x in bbox]
                        }
                        detections.append(detection)

            return detections

        except Exception as e:
            print(f"Erreur détection: {e}")
            return []