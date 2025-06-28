# AgriGuard AI - Setup MVP Flask + Nuxt3

## 🚀 ARCHITECTURE TECHNIQUE

```
Frontend (Nuxt3) ←→ API (Flask) ←→ AI Model (YOLOv11s)
     ↓
  Database ([SQLite, mongodb])
```

---

## 🔧 BACKEND FLASK

### Structure du projet
```
agriguard-backend/
├── app.py                  # entry
├── .gitignore              # ignore src
├── environment.yml         # conda user
├── models/                 # models manipulation
│   ├── __init__.py
│   ├── yolo_model_cls.py
│   └── yolo_model.py
├── utils/                  # Backend utils
│   ├── __init__.py
│   └── image_processing.py
├── data/                   # post actions data
│   └── pest_database.json
├── uploads/                # upload file directory
├── weights/                # model's weights
│   └── yolo{11s, 11m, 11s-cls, 11m-cls}.pt
└── requirements.txt        # py-env user
```

## 🔧 FRONTEND FLASK

### Structure du projet
```
agriguard-frontend/
├── app.vue
├── components
│  ├── CookieConsent.vue
│  ├── InternationalisationButtons.vue
│  ├── OfflineIndicator.vue
│  └── PwaInstallPrompt.vue
├── dist -> .output/public
├── i18n
│  └── locales
│      ├── en.json
│      └── fr.json
├── i18n.config.ts
├── layouts1
│  ├── admin.vue
│  └── default.vue
├── nuxt.config.ts
├── package-lock.json
├── package.json
├── pages
│  └── index.vue
├── plugins1
│  └── pwa.client.ts
├── public
│  ├── favicon.ico
│  ├── logo.png
│  └── robots.txt
├── README.md
├── server
│  └── tsconfig.json
├── stores
│  ├── auth
│  │  └── index.js
│  ├── locale
│  │  └── index.js
│  └── settings
│      └── index.js
├── tsconfig.json
└── types
    └── pwa.d.ts
```

## ⚡ DÉPLOIEMENT RAPIDE
### 1. Frontend Generation
```bash
# Se position dans le repertoire frontend
cd agriguard-frontend

# installer les dependances
# etre sur node 24
npm i

# generer les minifies du projet
npm run generate

# revenir à la racine
cd ..
```

### 2. Lancer le projet via le BACKEND

* py-env
```bash
# se position dans le repertoire backend
cd agriguard-backend
# Créer environnement virtuel
python -m venv conia2025
source conia2025/bin/activate  # Linux/Mac
# ou
conia2025\Scripts\activate     # Windows

# Installer dépendances
pip install -r requirements.txt

# Lancer serveur
python app.py
```

*  conda
```bash
# se position dans le repertoire backend
cd agriguard-backend
# Créer environnement virtuel
conda env create -f environment.yml

# Activer l'environnement
conda activate conia2025 

# Lancer serveur
python app.py
```


### 3. Test complet
```bash
# Frontend: http://localhost:3000
open http://localhost:3000
# API: http://localhost:3000/api
# Test API: http://localhost:3000/api/health
open http://localhost:3000/api/health
```

---

## 🎯 CHECKLIST MVP PRÉ-HACKATHON

### ✅ Fonctionnalités de base
- [x] Interface upload/caméra
- [x] Affichage résultats
- [x] Design responsive
- [ ] Données de test
- [x] API endpoints fonctionnels

### ✅ Optimisations
- [x] Chargement rapide
- [x] Gestion erreurs
- [ ] Feedback utilisateur
- [x] Mobile-friendly
- [x] Offline fallback

### ✅ Demo Ready
- [ ] Images de test préparées
- [ ] Scénarios de demo
- [ ] Données réalistes
- [ ] Performance fluide


### Note

- If you do not have node 24.x or npm installed to your machine, download and install the runtime from [node](https://nodejs.org/en/download/package-manager)
---
# Contribuer

## 🚀 Flux Git

- **Nom des branches**
    - Utilisez le format : `<numéro_issue>-<issue>`

- **Changements local**
    - `git status`
      - en rouge, les changement non ajoutés
      - en vert, ceux déjà ajoutés en attente d'acceptation
  
- **Commits**
    - ajouter vos changements locaux dans le git files, 
      - `git add filename_name1 filename_name2` ou
      - `git add .` pour dire tout
    - accepter les changements ajouter à monter vers le repo
      - `git commit -m $message`
    - Les messages (`$message`) de commit doivent suivre le format :  
      `" | <nom_auteur> |#<numéro_issue>| <description_du_travail>|"`
    - **Exemple** :  
      `"|@VictorNico|#1| configuration du projet |"`
    - Le numéro fait référence à l’**issue** (ticket) sur lequel vous travaillez.

- **Push**
    - Verifier s'il existe un changement sur la branche main :  
      `git pull`
      - S'il en existe des changement de la branch main parmi la liste des branches changées,
        - faire l'etappe **Commits**
        - entrer les changements upcomming avec `git merge origin/main` etant sur votre branche issue
        - dans le cas normal
          - il peut vous etre demandé un message de confirmation (message commit), de preference dans la partie description insister sur l'horodatage
            - example: `|@VictorNico| accepter les changements de main le 28/06/2025 20:02|`
          - enregistrer et fermer
        - sinon, il peux avoir des conflits 
          - il va falloir traiter les conflits efficacement, si on n'est pas sur d'un changement ne pas acter. attendre de l'aide
      - puis, `git push ` ou `git push -u origin <numéro_issue>-<issue>`
      

- **Pull Requests (PR)**
    - Si la PR concerne une **issue existante**, assurez-vous de la **mentionner dans la description** afin qu'elle soit fermée automatiquement à l’approbation de la PR.
    - Utilisez l’une des commandes suivantes :
        - `Resolves #<numéro_issue>`
        - `Fixes #<numéro_issue>`
        - `Closes #<numéro_issue>`
    - Assignez toujours la PR à **vous-même** et à **votre coéquipier**.

---
**Happy Coding Everyone 🚀**
