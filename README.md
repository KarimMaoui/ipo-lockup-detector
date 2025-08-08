# IPO scan


Mon Objectif
Automatiser la collecte, le traitement et la synthèse des informations liées aux IPO récentes.

## ⚙️ Fonctionnalités
- Récupération des IPO récentes via l'API EDGAR de la SEC
- Scraping des articles de presse financiers sur les tickers détectés
- Nettoyage et enrichissement des données
- Génération d'un digest quotidien ou hebdomadaire

## Structure
Le code est structuré pour séparer la collecte des données, leur traitement et la génération du digest final.  
Toutes les étapes sont regroupées dans `src/` et peuvent être exécutées individuellement ou enchaînées automatiquement.


## 🚀 Lancer le projet depuis chez votre terminal
Pour lancer la pipeline complète, il suffit d’exécuter :
```bash
python src/scheduler.py
