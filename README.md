# PDF Compressor (Flask)

Petit projet : site simple pour compresser un PDF en ligne.

## Fichiers
- app.py : l'application Flask
- templates/index.html : front simple
- requirements.txt : dépendances

## Installation (local)

1. Crée un venv :
   ```bash
   python -m venv venv
   source venv/bin/activate   # mac/linux
   venv\Scripts\activate    # windows
   ```
2. Installe les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Lance l'application :
   ```bash
   python app.py
   ```
4. Ouvre `http://localhost:5000` dans ton navigateur.

## Déploiement
- Render / Railway / Heroku supportent Flask. Attention à la taille des fichiers et au timeout.
- Pour production, configure une suppression asynchrone des fichiers et active HTTPS.

## Notes techniques
- Ce template utilise `pikepdf`. Si pikepdf n'est pas adapté, tu peux utiliser `qpdf` via la ligne de commande ou `ghostscript` pour une recompression d'images.
- Respecte la confidentialité : supprime les fichiers après traitement.
