from flask import Flask, jsonify, request, render_template
import boto3

app = Flask(__name__)

# Configure AWS S3 and Rekognition
S3_BUCKET_NAME = 'umkc-images'
S3_REGION = 'us-east-2'

s3_client = boto3.client('s3', region_name=S3_REGION)
rekognition_client = boto3.client('rekognition', region_name=S3_REGION)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch-images', methods=['GET'])
def fetch_images():
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
        if 'Contents' not in response:
            return jsonify({'images': []})
        
        images = [
            f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{obj['Key']}"
            for obj in response['Contents']
        ]
        return jsonify({'images': images})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recognize-image', methods=['POST'])
def recognize_image():
    try:
        data = request.json
        image_url = data.get('image_url')

        # Download the image from the URL
        response = s3_client.get_object(
            Bucket=S3_BUCKET_NAME,
            Key=image_url.split(f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/")[-1]
        )
        image_bytes = response['Body'].read()

        # Use AWS Rekognition to detect labels
        rekognition_response = rekognition_client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=5
        )
        labels = [label['Name'] for label in rekognition_response['Labels']]
        return jsonify({'labels': labels})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
