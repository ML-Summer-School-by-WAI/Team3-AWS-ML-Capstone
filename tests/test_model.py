# tests/test_model.py
import pytest
import pandas as pd
import numpy as np
import joblib



def test_model_prediction():
    """Tests that the model returns a prediction of the correct type and shape."""
    try:
        model = joblib.load("model.joblib")
    except FileNotFoundError:
        pytest.skip("Trained model file 'model.joblib' not found. Run train.py first.")

    sample_data = {
        'Pclass': [3],
        'Sex': [0], # male
        'Age': [25],
        'SibSp': [1],
        'Parch': [0],
        'Fare': [7.5],
        'Embarked': [2] # S
    }
    input_df = pd.DataFrame(sample_data)

   
    prediction = model.predict(input_df)

    assert isinstance(prediction, np.ndarray), "Prediction should be a numpy array"
    assert prediction.shape == (1,), "Prediction shape should be (1,)"
    assert prediction[0] in [0, 1], "Prediction value should be 0 or 1"