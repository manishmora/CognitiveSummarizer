import pandas as pd
import joblib
import os
import logging
from sklearn.base import ClassifierMixin
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

model_path = os.path.join('trained_models', 'failure_model.pkl')
scaler_path = os.path.join('trained_models', 'scaler.pkl')

# Global model variable
model = None

# Load model
def load_model():
    global model  # Use the global model variable to avoid issues with scope
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please ensure the model is uploaded and generated.")
    
    model = joblib.load(model_path)
    
    # Log the type of the model
    logging.info(f"Loaded model type: {type(model)}")
    
    # Check if the model is a classifier
    if not isinstance(model, ClassifierMixin):
        raise ValueError(f"The loaded model is not a classifier. Please ensure it is a valid sklearn classifier.")
    
    logging.info(f"Model loaded successfully from {model_path}")

# Load scaler
scaler = None
if os.path.exists(scaler_path):
    scaler = joblib.load(scaler_path)
    logging.info(f"Scaler loaded successfully from {scaler_path}")
else:
    logging.warning(f"Scaler not found at {scaler_path}, proceeding without scaling.")

# Preprocess data
def preprocess_data(df):
    feature_columns = [col for col in df.columns if col not in ['timestamp', 'failure']]
    X = df[feature_columns]
    
    # Check that X is not empty and has the correct shape
    if X.empty:
        raise ValueError("Feature data is empty. Please check the input CSV.")
    
    logging.info(f"Features selected: {feature_columns}")
    
    if scaler:
        X = scaler.transform(X)
        logging.info(f"Data scaled using the loaded scaler.")
    else:
        logging.warning("No scaler found. Data will not be scaled.")
        
    logging.info(f"Data shape for prediction: {X.shape}")
    return X

# Predict failures
def predict_failures(csv_path):
    try:
        if model is None:
            load_model()  # Ensure the model is loaded before making predictions
        
        df = pd.read_csv(csv_path)
        
        if df.empty:
            return {"status": "error", "message": "CSV file is empty."}

        X = preprocess_data(df)
        
        # Debug log for model prediction
        logging.info(f"Making predictions for {len(X)} samples.")
        
        predictions = model.predict(X)
        
        # Log prediction result for debugging
        logging.info(f"Predictions: {predictions[:5]}")  # Show first 5 predictions
        
        prob = model.predict_proba(X)[:, 1]
        
        # Log probability for debugging
        logging.info(f"Prediction Probabilities: {prob[:5]}")  # Show first 5 probabilities

        df['Failure_Prediction'] = predictions
        df['Failure_Probability'] = prob

        summary = {
            "total_records": len(df),
            "predicted_failures": int(predictions.sum()),
            "max_probability": round(float(prob.max()), 3),
            "avg_probability": round(float(prob.mean()), 3)
        }

        return {"status": "ok", "summary": summary}

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return {"status": "error", "message": str(e)}
