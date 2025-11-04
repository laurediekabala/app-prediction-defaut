from flask import Flask,request,jsonify,send_file
import joblib as job
import pandas as pd
import os
app =Flask(__name__) 
# charger le model déjà sauvagarder pour faire de prédiction.
model_path=os.path.join(os.getcwd(),"xboost.joblib")
def models() :
    try : 
        model =job.load(model_path)
        print(f"le model est chargé avec succès depuis {model_path}")
        return model
    except Exception as e :
        print(f"erreur lors de chargement du model :{e}")  
        model =None 
        return model
@app.route('/model',methods=['GET'])
def model() :
    try : 
        return send_file(model_path,as_attachment=True)
    except  FileNotFoundError :
       return jsonify({"fichier":"fichier non trouvé"}),404 
@app.route('/predict',methods=['POST'])
def predit() :
    input_df=request.get_json(force=True)
    print("donnees recues ")
    try :
      if input_df is None :
         print("les donnees ne sont ps chargées")
      else :
          print("les donnees sont chargées") 
          model =models()
      input_data=pd.DataFrame([input_df],index=[0])
      for col in input_data :
          print(col)
      proba=float(model.predict_proba(input_data)[0,1])
      prediction= int(proba>=0.45)
      return jsonify({"prediction":prediction,"probabilite":proba})
    except Exception as e :
            print(f"erreur inattendue :{e}") 
            app.logger.exception("Erreur lors de la prédiction")
            return jsonify({"error": str(e)}), 500 
if __name__ =="__main__" :
       app.run(host="0.0.0.0", debug=True, port=5000)


    
     

  