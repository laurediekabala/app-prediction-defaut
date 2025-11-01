 # cette application  est orientée finance elle permet aux entreprises de comprendre les caracteristiques de clients qui sont suscseptibles de faire defaut de paiement ou pas et d'anticiper.
 # pour anticiper nous avons utilisé le model de machine learning  puissant xgboost pour permettre l'entreprise de connaitre par avance les clients qui vont faire defaut de paiement ou pas
 # fonctionnement de l'application :
       * Pour acceder à cette application  il faut d'abord s'authentifier en saisissant votre nom et votre mot de passe si vous  n'avez pas de compte il y a un bouton  permettant de créer votre compte pour créer votre compte vous devez saisir votre nom,votre mot de passe et choisir votre rôle soit admin ,soit analyste,le compte admin est celui qui  administre le systeme et le compte analyste est celui qui ne fait que l'analyse de données.

       * Si vous êtes admin ,après avoir vous connecté vous aller parcourir toutes les pages à savoir :
          a) page d'accueil
          b) page d'analyse  :
                 cette page permet d'analyser les données, les utilisateurs ont droit de choisir  les colonnes pour faire l'analyser ,il sied de signaler qu'à travers cette page vous pouvez filtrer et faire l'analyse descriptive.
          c) page pour la prediction ou machine learning :
              ici nous avons appelé  l'api flask qui retourne le model déjà préentrainé, à paritr de celui-ci vous pouvez faire la prediction en remplissant tous les champs.       

        * par contre si vous êtes analyste vous allez vous connecter sur les deux pages à savoir :
            page analyse et page machine learning
# Pour arriver en mettre oeuvre cette petite application nous avaons utilisé le framework  de pytthon streamlit et du css pour tous contact :laurediekabala@gmail.com            
      
      
 
 

