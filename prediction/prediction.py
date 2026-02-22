from flask import Flask, request, jsonify, send_file
import joblib
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "xboost.joblib")

def load_model():
    try:
        model = joblib.load(model_path)
        print(f"✅ Modèle chargé depuis {model_path}")
        return model
    except Exception as e:
        print(f"❌ Erreur chargement modèle : {e}")
        return None

model = load_model()

@app.route('/model', methods=['GET'])
def get_model():
    if not os.path.exists(model_path):
        return jsonify({"error": "Modèle introuvable"}), 404
    return send_file(model_path, as_attachment=True)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_json = request.get_json(force=True)
        if input_json is None:
            return jsonify({"error": "JSON vide"}), 400

        input_df = pd.DataFrame([input_json])
        proba = float(model.predict_proba(input_df)[0, 1])
        prediction = int(proba >= 0.45)

        return jsonify({
            "prediction": prediction,
            "probabilite": proba
        })

    except Exception as e:
        app.logger.exception("Erreur prédiction")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
