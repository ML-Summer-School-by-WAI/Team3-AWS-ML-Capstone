import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

PROCESSED_DATA_PATH = os.path.join("data", "processed", "titanic_clean.csv")
MODEL_OUTPUT_PATH = "model.joblib"


def train_model():
    print(f"Loading processed data from '{PROCESSED_DATA_PATH}'...")
    try:
        df = pd.read_csv(PROCESSED_DATA_PATH)
    except FileNotFoundError:
        print(f"Error: The file was not found at '{PROCESSED_DATA_PATH}'.")
        print("Please ensure your processed data exists.")
        return

    features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    target = 'Survived'
    
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Data split into {len(X_train)} training and {len(X_test)} testing samples.")

    print("Training the Logistic Regression model...")
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    print("Model training complete.")

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"✅ Model Accuracy on the test set: {accuracy:.4f}")

    print(f"Saving model to '{MODEL_OUTPUT_PATH}'...")
    joblib.dump(model, MODEL_OUTPUT_PATH)
    print("✅ Model saved successfully.")


if __name__ == "__main__":
    train_model()