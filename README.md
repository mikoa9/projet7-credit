# projet7-credit
Vous êtes Data Scientist au sein d'une société financière, nommée "Prêt à dépenser",  qui propose des crédits à la consommation pour des personnes ayant peu ou pas du tout d'historique de prêt.
L’entreprise souhaite mettre en œuvre un outil de “scoring crédit” pour calculer la probabilité qu’un client rembourse son crédit, puis classifie la demande en crédit accordé ou refusé. Elle souhaite donc développer un algorithme de classification en s’appuyant sur des sources de données variées (données comportementales, données provenant d'autres institutions financières, etc.).

De plus, les chargés de relation client ont fait remonter le fait que les clients sont de plus en plus demandeurs de transparence vis-à-vis des décisions d’octroi de crédit. Cette demande de transparence des clients va tout à fait dans le sens des valeurs que l’entreprise veut incarner.

Prêt à dépenser décide donc de développer un dashboard interactif pour que les chargés de relation client puissent à la fois expliquer de façon la plus transparente possible les décisions d’octroi de crédit, mais également permettre à leurs clients de disposer de leurs informations personnelles et de les explorer facilement. 

## Les données
Voici les données dont vous aurez besoin pour réaliser le dashboard : https://www.kaggle.com/c/home-credit-default-risk/data

Pour plus de simplicité, vous pouvez les télécharger à cette adresse : 
https://s3-eu-west-1.amazonaws.com/static.oc-static.com/prod/courses/files/Parcours_data_scientist/Projet+-+Impl%C3%A9menter+un+mod%C3%A8le+de+scoring/Projet+Mise+en+prod+-+home-credit-default-risk.zip

Vous aurez sûrement besoin de joindre les différentes tables entre elles.

## Votre mission
- Construire un modèle de scoring qui donnera une prédiction sur la probabilité de faillite d'un client de façon automatique.
- Construire un dashboard interactif à destination des gestionnaires de la relation client permettant d'interpréter les prédictions faites par le modèle, et d’améliorer la connaissance client des chargés de relation client.

Michaël, votre manager, vous incite à sélectionner un kernel Kaggle pour vous faciliter la préparation des données nécessaires à l’élaboration du modèle de scoring. Vous analyserez ce kernel et l’adapterez pour vous assurer qu’il répond aux besoins de votre mission.

Vous pourrez ainsi vous focaliser sur l’élaboration du modèle, son optimisation et sa compréhension.

## Spécifications du dashboard

Michaël vous a fourni des spécifications pour le dashboard interactif. Celui-ci devra contenir au minimum les fonctionnalités suivantes :

- Permettre de visualiser le score et l’interprétation de ce score pour chaque client de façon intelligible pour une personne non experte en data science.
- Permettre de visualiser des informations descriptives relatives à un client (via un système de filtre).
- Permettre de comparer les informations descriptives relatives à un client à l’ensemble des clients ou à un groupe de clients similaires.

## Livrables 

- Le dashboard interactif répondant aux spécifications ci-dessus et l’API de prédiction du score, déployées chacunes sur le cloud : 
  - Dashboard : https://share.streamlit.io/mikoa9/projet7-credit/main/streamlit/streamlit_app.py
  - API: https://projet7-credit.herokuapp.com/ 
  - ex appel API : https://projet7-credit.herokuapp.com/predict/358806
  - [le sample déployé avec l'api](https://github.com/mikoa9/projet7-credit/blob/main/model/app_sample_normalized.csv)
- Un dossier sur un outil de versioning de code contenant :
  - Le code de la modélisation (du prétraitement à la prédiction)
  - [Le code générant le dashboard](https://github.com/mikoa9/projet7-credit/blob/main/streamlit/streamlit_app.py)
  - [Le code permettant de déployer le modèle sous forme d'API](https://github.com/mikoa9/projet7-credit/blob/main/app.py)
- Une note méthodologique décrivant :
  - La méthodologie d'entraînement du modèle (2 pages maximum)
  - La fonction coût métier, l'algorithme d'optimisation et la métrique d'évaluation (1 page maximum)
  - L’interprétabilité globale et locale du modèle (1 page maximum)
  - Les limites et les améliorations possibles (1 page maximum)
- Un support de présentation pour la soutenance, détaillant le travail réalisé.
