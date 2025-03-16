# Dressing Virtuel

## Table des Matières
- [Description du Projet](#description-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration des Variables d'Environnement](#configuration-des-variables-denvironnement)
- [Contribution](#contribution)
- [Licence](#licence)
- [Auteurs](#auteurs)

---

## Description du Projet
Dressing Virtuel est une application permettant de stocker et organiser des photos de tous les vêtements d'un utilisateur. Cela permet un accès rapide à sa collection de vêtements sans avoir besoin de se rendre physiquement à son dressing.

En plus de cet accès simplifié, l'application propose des suggestions de tenues en fonction de l'occasion (réunion, sortie, week-end, etc.).

### Pourquoi Dressing Virtuel ?
Contrairement à d'autres applications similaires, Dressing Virtuel ne requiert pas de prendre des photos de chaque vêtement individuellement. Son moteur **I2C1 (Image to Clothes v1)** utilise la vision par ordinateur pour extraire automatiquement les vêtements à partir de photos existantes (ex: Google Photos) et les classifier intelligemment.

### Engagement contre le Fast Fashion
Dressing Virtuel aide à lutter contre la surconsommation vestimentaire en offrant un inventaire digitalisé des vêtements. Cela permet à l'utilisateur de vérifier s'il possède déjà un article avant d'en acheter un nouveau. 
De futures fonctionnalités permettront aussi d'identifier les vêtements peu utilisés pour favoriser la revente ou le don.

---

## Fonctionnalités
- **Ajout automatique de vêtements** à partir de photos existantes
- **Classification intelligente** des vêtements
- **Suggestions de tenues** en fonction de l'occasion
- **Recherche et filtre avancés** pour retrouver un vêtement
- **Prise en charge des métadonnées** pour l'analyse de l'utilisation des vêtements
- **Gestion et synchronisation avec Google Photos** (futur)

---

## Prérequis

Ce dépôt est le front-end du projet Dressing Virtuel Data Collector disponible à l'adresse suivante : [Dressing Virtuel Data Collector](https://github.com/JhonatanCaldeira/dressing_virtuel_data_collector).

L'installation préalable du back-end est nécessaire pour le bon fonctionnement du front-end.

---

## Installation

1. **Installer Python 3.10**
2. **Installer Git ou GitHub Desktop**
3. **Cloner le dépôt** dans un répertoire local :
   ```sh
   git clone https://github.com/JhonatanCaldeira/Dressing_Virtuel.git ./
   ```
4. **Configurer l'environnement virtuel** :
   ```sh
   python -m venv .venv
   ```
5. **Activer l'environnement virtuel** :
   ```sh
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```
6. **Installer les dépendances** :
   ```sh
   pip install -r requirements.txt
   ```
7. **Démarrer Django** :
   ```python
   python manage.py runserver
   ```

---

## Configuration des Variables d'Environnement

Avant de lancer l'application, assurez-vous de configurer les variables d'environnement dans `config/.env` :

Exemple minimal :
```ini
# Dossiers de stockage
IMAGE_TMP_DIR=./tmp
IMAGE_STORAGE_DIR=./storage

# PostgreSQL
PG_DB_HOST=localhost
PG_DB_PORT=5432
PG_DB_NAME=db_dressing_virtuel
PG_DB_USER=admin
PG_DB_PASSWORD=your_password
```

La liste complète des variables est disponible dans [`config/.env.example`](config/.env.example).

---

## Contribution

Les contributions sont les bienvenues !

1. Forkez le repo
2. Créez une branche (`git checkout -b feature-nouvelle-fonction`)
3. Faites vos modifications et commit (`git commit -m "Ajout d'une nouvelle fonctionnalité"`)
4. Poussez votre branche (`git push origin feature-nouvelle-fonction`)
5. Créez une Pull Request

Voir [`contributing.md`](contributing.md) pour plus de détails.

---

## Licence

Ce projet est sous licence [MIT](https://choosealicense.com/licenses/mit/).

---

## Auteurs

- [@Jhonatan Caldeira](https://github.com/JhonatanCaldeira)


