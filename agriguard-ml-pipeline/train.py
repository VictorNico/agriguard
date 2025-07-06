from ultralytics import YOLO
import os
import yaml

def train_model(cfg):
    model_path = cfg["initial_model"]

    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"[ERREUR OFFLINE] Le modèle local '{model_path}' est introuvable. Aucun téléchargement autorisé. Place-le dans le dossier du projet.")

    print(f"[INFO] Chargement du modèle local depuis : {model_path}")
    model = YOLO(model_path)

    # Sécurité : suppression de tout ancien fichier data.yaml
    if os.path.exists(cfg["data_yaml"]):
        os.remove(cfg["data_yaml"])

    # Génération automatique du fichier data.yaml au format Ultralytics attendu
    # names_dict = {i: name for i, name in enumerate(cfg["class_names"])}
    # data_yaml_dict = {
    #     "names": names_dict,
    #     "nc": cfg["num_classes"],
    #     "path": cfg["dataset_split"],
    #     "train": "./train",
    #     "val": "./val"
    # }
    # with open(cfg["data_yaml"], "w") as f:
    #     yaml.dump(data_yaml_dict, f, sort_keys=False)
    # print(f"[INFO] Fichier data.yaml généré à {cfg['data_yaml']}")

    results = model.train(
        data=cfg["data_yaml"],
        epochs=cfg["epochs"],
        imgsz=cfg["imgsz"],
        batch=cfg["batch"],
        device=cfg["device"],
        project=cfg["project"],
        name=cfg["name"],
        resume=os.path.exists(cfg["resume_model"])
    )

    print(f"[INFO] Entraînement terminé. Meilleur modèle : {results.best}")
    return results.best
