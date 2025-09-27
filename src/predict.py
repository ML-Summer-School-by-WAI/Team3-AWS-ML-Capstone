import boto3
import pandas as pd
import joblib
import json
import os
from io import StringIO

s3_client = boto3.client('s3')

MODEL_BUCKET = os.environ.get('MODEL_BUCKET') 
MODEL_KEY = os.environ.get('MODEL_KEY')


LOCAL_MODEL_PATH = f"/tmp/{os.path.basename(MODEL_KEY)}"

if not os.path.exists(LOCAL_MODEL_PATH):
    print(f"Model not found locally. Downloading from s3://{MODEL_BUCKET}/{MODEL_KEY}")
    s3_client.download_file(MODEL_BUCKET, MODEL_KEY, LOCAL_MODEL_PATH)
    print("Model downloaded successfully.")

try:
    model = joblib.load(LOCAL_MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None


def lambda_handler(event, context):
    """
    This function is the entry point for the Lambda function.
    It receives an event from API Gateway, preprocesses the data,
    makes a prediction, and returns the result.
    """
    if model is None:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Model could not be loaded.'})
        }

    try:

        print(f"Received event: {event}")

        body = json.loads(event.get('body', '{}'))

        input_df = pd.DataFrame([body])
        
        training_medians = {'Age': 29.0, 'Fare': 14.45}
        input_df['Age'].fillna(training_medians['Age'], inplace=True)
        input_df['Fare'].fillna(training_medians['Fare'], inplace=True)
        
        # 3. Encode categorical variables
        input_df['Sex'] = input_df['Sex'].map({'male': 0, 'female': 1})
    
        model_features = ['Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Parch']
        for col in model_features:
            if col not in input_df.columns:

                input_df[col] = 0
        
        processed_input = input_df[model_features]

        # 5. Make a prediction
        prediction = model.predict(processed_input)
  
        prediction_result = int(prediction[0])
        
        print(f"Prediction result: {prediction_result}")

        return {
            'statusCode': 200,
            'headers': {
                # Required for CORS
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({
                'prediction': prediction_result,
                'interpretation': 'Survived' if prediction_result == 1 else 'Did Not Survive'
            })
        }

    except Exception as e:
        print(f"Error during prediction: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'An error occurred during processing: {str(e)}'})
        }