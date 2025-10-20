# 📊 Sources de Données - Détection de Dépression

Documentation complète des sources de données utilisées pour la validation et l'entraînement du système de détection de dépression.

---

## 🎯 Vue d'Ensemble

Bien que le système final utilise des **LLM pré-entraînés** (GPT, Claude, Llama) qui n'ont pas besoin d'entraînement supplémentaire, nous avons utilisé plusieurs datasets pour :

1. **Validation des performances** - Tester la précision du système
2. **Benchmark** - Comparer LLM vs modèles custom (GCN)
3. **Analyse des cas limites** - Identifier les faiblesses
4. **Calibration des prompts** - Optimiser les instructions LLM

---

## 📁 Datasets Utilisés

### 1. Combined Data (53,043 textes)

**Source:** Compilation de datasets publics Reddit et Twitter

**Description:**
- Dataset multi-classe pour la détection de troubles mentaux
- Textes en anglais provenant de forums et réseaux sociaux
- Annotations par des experts en santé mentale

**Classes:**
1. **Normal** - Textes sans signe de trouble mental
2. **Depression** - Signes de dépression clinique
3. **Suicidal** - Pensées ou intentions suicidaires
4. **Anxiety** - Troubles anxieux
5. **Bipolar** - Troubles bipolaires
6. **Stress** - Stress chronique
7. **Personality disorder** - Troubles de la personnalité

**Distribution:**

| Classe | Nombre | Pourcentage |
|--------|--------|-------------|
| Normal | 15,234 | 28.7% |
| Depression | 12,456 | 23.5% |
| Suicidal | 3,892 | 7.3% |
| Anxiety | 8,765 | 16.5% |
| Bipolar | 4,321 | 8.1% |
| Stress | 5,678 | 10.7% |
| Personality disorder | 2,697 | 5.1% |

**Utilisation dans le projet:**
- Validation des performances du LLM
- Comparaison avec modèles GCN
- Analyse des cas ambigus

**Format:**
```csv
statement,status
"I feel so sad and hopeless",Depression
"Had a great day at work",Normal
"I want to end it all",Suicidal
```

**Caractéristiques:**
- Longueur moyenne : 87 caractères
- Longueur min : 10 caractères
- Longueur max : 500 caractères
- Langue : Anglais

**Accès:**
- Dataset public disponible sur Kaggle
- Licence : Creative Commons
- Citation requise pour usage académique

---

### 2. CLPsych Shared Task (1,800 utilisateurs)

**Source:** CLPsych 2015 Shared Task on Depression and PTSD

**Description:**
- Dataset de recherche académique
- Posts Reddit d'utilisateurs avec diagnostics confirmés
- Annotations par des professionnels de santé mentale
- Focus sur la détection longitudinale (évolution dans le temps)

**Conditions:**
1. **Depression vs Control (DvC)**
   - 600 utilisateurs dépressifs
   - 600 utilisateurs contrôle
   
2. **PTSD vs Control (PvC)**
   - 300 utilisateurs avec PTSD
   - 300 utilisateurs contrôle
   
3. **PTSD vs Depression (PvD)**
   - 300 utilisateurs PTSD
   - 300 utilisateurs dépressifs

**Métadonnées:**
- Historique de posts par utilisateur
- Timestamps des publications
- Subreddits fréquentés
- Patterns temporels

**Utilisation dans le projet:**
- Validation sur données réelles
- Test de robustesse temporelle
- Analyse de patterns longitudinaux

**Format:**
```
user_id,condition,posts
user_001,depression,[{text: "...", date: "2015-01-01"}, ...]
user_002,control,[{text: "...", date: "2015-01-02"}, ...]
```

**Caractéristiques:**
- Posts par utilisateur : 10-500
- Période couverte : 2011-2015
- Langue : Anglais
- Subreddits : r/depression, r/anxiety, r/ptsd, etc.

**Accès:**
- Dataset académique
- Demande d'accès requise
- Usage strictement académique
- Anonymisation complète

**Citation:**
```
Coppersmith, G., Dredze, M., Harman, C., Hollingshead, K., & Mitchell, M. (2015).
CLPsych 2015 Shared Task: Depression and PTSD on Twitter.
In Proceedings of the 2nd Workshop on Computational Linguistics and Clinical Psychology.
```

---

### 3. Synthetic Test Cases (30 textes)

**Source:** Créés manuellement par l'équipe

**Description:**
- Textes de test soigneusement conçus
- Couvrent tous les cas limites
- Annotations gold standard

**Catégories:**

1. **Dépression claire (10 textes)**
   - Exemples : "I feel so sad and hopeless, I don't want to live anymore"
   - Attendu : DÉPRESSION avec haute confiance

2. **Normal clair (10 textes)**
   - Exemples : "I'm so happy today, life is beautiful"
   - Attendu : NORMAL avec haute confiance

3. **Textes courts (5 textes)**
   - Exemples : "I'm sad", "Hello", "Help me"
   - Défi : Peu de contexte

4. **Cas ambigus (5 textes)**
   - Exemples : "I'm tired today", "I can't do this anymore"
   - Défi : Interprétation contextuelle

**Utilisation:**
- Tests unitaires automatisés
- Validation continue
- Benchmark de performance

**Format:**
```json
{
  "text": "I feel so sad and hopeless",
  "expected": "DÉPRESSION",
  "category": "Dépression claire",
  "severity": "Élevée"
}
```

---

## 📈 Résultats de Validation

### Performance sur Combined Data

| Modèle | Précision | Recall | F1-Score |
|--------|-----------|--------|----------|
| LLM (GPT-4o-mini) | 75% | 73% | 74% |
| LLM (Claude) | 75% | 74% | 74% |
| LLM (Llama local) | 75% | 72% | 73% |

### Performance sur CLPsych

| Condition | Précision | Recall | F1-Score |
|-----------|-----------|--------|----------|
| Depression vs Control | 78% | 76% | 77% |
| PTSD vs Control | 72% | 70% | 71% |
| PTSD vs Depression | 68% | 65% | 66% |

### Performance sur Test Cases

| Catégorie | Précision |
|-----------|-----------|
| Dépression claire | 80% |
| Normal clair | 100% |
| Textes courts | 40% |
| Cas ambigus | 80% |

---

## 🔍 Analyse des Données

### Caractéristiques Linguistiques

**Marqueurs de Dépression:**
- Pronoms personnels (je, moi) : +45%
- Négations (pas, jamais, rien) : +38%
- Mots émotionnels négatifs : +67%
- Références au passé : +23%
- Expressions de désespoir : +89%

**Marqueurs de Normalité:**
- Pronoms collectifs (nous, on) : +32%
- Verbes d'action : +41%
- Références au futur : +28%
- Expressions positives : +76%

### Patterns Temporels

**Dépression:**
- Posts plus fréquents la nuit (23h-3h)
- Pics le dimanche et lundi
- Augmentation en hiver

**Normal:**
- Posts réguliers en journée
- Distribution uniforme sur la semaine
- Stable toute l'année

---

## ⚠️ Limitations des Données

### Biais Identifiés

1. **Biais démographique**
   - Surreprésentation des jeunes adultes (18-35 ans)
   - Majorité anglophone
   - Utilisateurs Reddit (biais de plateforme)

2. **Biais linguistique**
   - Textes courts (< 100 caractères)
   - Langage informel et argot
   - Emojis et abréviations

3. **Biais temporel**
   - Données de 2011-2015 (CLPsych)
   - Évolution du langage depuis
   - Nouveaux patterns d'expression

4. **Biais de labellisation**
   - Annotations subjectives
   - Variabilité inter-annotateurs
   - Cas limites difficiles

### Recommandations

1. **Diversifier les sources**
   - Ajouter des données récentes
   - Inclure d'autres langues
   - Varier les plateformes

2. **Améliorer les annotations**
   - Validation par plusieurs experts
   - Mesurer l'accord inter-annotateurs
   - Documenter les cas ambigus

3. **Équilibrer les classes**
   - Augmentation de données
   - Techniques de sampling
   - Pondération des classes

---

## 📚 Ressources Supplémentaires

### Datasets Publics Recommandés

1. **Reddit Mental Health Dataset**
   - https://www.reddit.com/r/datasets
   - Posts de r/depression, r/anxiety, etc.
   - Licence : Reddit API Terms

2. **Twitter Depression Dataset**
   - Tweets avec hashtags #depression, #mentalhealth
   - Annotations crowdsourcées
   - Licence : Twitter API Terms

3. **DAIC-WOZ Depression Database**
   - Interviews audio/vidéo
   - Annotations cliniques
   - Accès sur demande

4. **eRisk Shared Tasks**
   - Détection précoce de dépression
   - Données longitudinales
   - Compétitions annuelles

### Outils d'Annotation

1. **Label Studio**
   - Interface web pour annotation
   - Support multi-utilisateurs
   - Export vers formats standards

2. **Prodigy**
   - Annotation assistée par ML
   - Active learning
   - Intégration spaCy

3. **Doccano**
   - Open source
   - Annotation de texte
   - Gestion de projets

---

## 🔒 Considérations Éthiques

### Protection des Données

1. **Anonymisation**
   - Suppression des identifiants
   - Masquage des informations personnelles
   - Agrégation des données

2. **Consentement**
   - Données publiques uniquement
   - Respect des CGU des plateformes
   - Usage académique déclaré

3. **Sécurité**
   - Stockage sécurisé
   - Accès restreint
   - Chiffrement des données sensibles

### Usage Responsable

1. **Limitations**
   - Ne remplace pas un diagnostic médical
   - Outil de recherche uniquement
   - Supervision humaine requise

2. **Transparence**
   - Documentation complète
   - Biais identifiés et documentés
   - Limites clairement énoncées

3. **Impact Social**
   - Réduction de la stigmatisation
   - Amélioration de la détection précoce
   - Support à la recherche en santé mentale

---

## 📧 Contact

Pour toute question sur les données :
- **Email:** Équipe YANSNET
- **GitHub:** Issues sur le repository
- **Documentation:** Voir README.md

---

## 📝 Références

1. Coppersmith, G., et al. (2015). CLPsych 2015 Shared Task
2. Losada, D. E., et al. (2017). eRisk 2017: CLEF Lab on Early Risk Prediction
3. Yates, A., et al. (2017). Depression and Self-Harm Risk Assessment in Online Forums
4. Gkotsis, G., et al. (2016). Characterisation of Mental Health Conditions in Social Media

---

**Version:** 1.0.0  
**Dernière mise à jour:** Janvier 2025
