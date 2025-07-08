import os
import torch
import matplotlib.pyplot as plt
from ultralytics import YOLO

# === Configuration ===
MODEL_PATH = "yolov11s-cls.pt"
DATA_PATH = "dataset_split"
EPOCHS = 20
BATCH_SIZE = 48
IMG_SIZE = 224
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def fine_tune_yolo():
    """Fine-tuning du modèle YOLOv11s-cls avec tracking des performances"""
    if not os.path.exists(MODEL_PATH):
        print(f"Erreur: Le modèle {MODEL_PATH} n'existe pas.")
        print("Téléchargez-le avec: yolo download yolov11s-cls.pt")
        return None

    if not os.path.exists(DATA_PATH):
        print(f"Erreur: Le dataset {DATA_PATH} n'existe pas.")
        return None

    print(f"Device : {DEVICE}")
    print(f"Fine-tuning sur dataset : {DATA_PATH}")
    
    model = YOLO(MODEL_PATH)

    results = model.train(
        data=DATA_PATH,
        epochs=EPOCHS,
        batch=BATCH_SIZE,
        imgsz=IMG_SIZE,
        device=DEVICE,
        project="yolo_classification",
        name="finetune_experiment",
        save=True,
        verbose=True,
        patience=10,
        lr0=0.01,
        warmup_epochs=3,
        seed=42,

        # 🎯 Augmentations avancées
        augment=True,
        mixup=0.2,
        copy_paste=0.2,
        erasing=True
    )

    print("✅ Entraînement terminé.")
    return results

def plot_training_metrics(results):
    """Génère un graphique de loss et accuracy par epoch"""
    try:
        metrics = results.metrics
        epochs = list(range(1, len(metrics["train/loss"]) + 1))

        plt.figure(figsize=(12, 6))

        # === Loss ===
        plt.subplot(1, 2, 1)
        plt.plot(epochs, metrics["train/loss"], label="Train Loss")
        plt.plot(epochs, metrics["val/loss"], label="Val Loss")
        plt.title("Loss par epoch")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.legend()
        plt.grid(True)

        # === Accuracy ===
        plt.subplot(1, 2, 2)
        plt.plot(epochs, metrics["metrics/accuracy_top1"], label="Top-1 Accuracy")
        plt.plot(epochs, metrics["metrics/accuracy_top5"], label="Top-5 Accuracy")
        plt.title("Accuracy par epoch")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.savefig("training_metrics.png")
        print("📊 Graphique sauvegardé sous : training_metrics.png")
        #plt.show()

    except Exception as e:
        print("❌ Erreur lors de la génération du graphique :", e)

def main():
    print("=== Lancement du fine-tuning YOLOv11s-cls ===")
    results = fine_tune_yolo()
    
    if results:
        plot_training_metrics(results)

        best_model = os.path.join(results.save_dir, "weights", "best.pt")
        print(f"✅ Meilleur modèle : {best_model}")

if __name__ == "__main__":
    main()