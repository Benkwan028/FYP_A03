from flask import Blueprint, request, jsonify
import boto3
import os
from dotenv import load_dotenv
import hmac
import hashlib
import base64
import traceback

# Load environment variables from .env
load_dotenv()

# AWS Configuration
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
AWS_REGION = os.getenv("AWS_REGION")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Initialize AWS Services
cognito_client = boto3.client('cognito-idp', region_name=AWS_REGION)
s3_client = boto3.client('s3', region_name=AWS_REGION)
dynamodb_client = boto3.resource('dynamodb', region_name=AWS_REGION)

# Define a Blueprint for routes
main = Blueprint('main', __name__)

# Helper function to calculate SECRET_HASH
def get_secret_hash(username, client_id, client_secret):
    """
    Calculate the SECRET_HASH required by AWS Cognito when using a client secret.
    """
    message = username + client_id
    dig = hmac.new(
        client_secret.encode('utf-8'),
        message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

@main.route('/')
def home():
    """Homepage route."""
    return "Welcome to the Motorcycle Online Platform Prototype!"

# User Registration Endpoint
@main.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        # Validate input
        if not username or not password or not email:
            return jsonify({'error': 'Missing required fields: username, password, or email'}), 400

        # Calculate SECRET_HASH
        secret_hash = get_secret_hash(email, COGNITO_APP_CLIENT_ID, COGNITO_CLIENT_SECRET)

        # Register user in AWS Cognito
        cognito_client.sign_up(
            ClientId=COGNITO_APP_CLIENT_ID,
            SecretHash=secret_hash,
            Username=email,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'nickname', 'Value': username}
            ]
        )

        return jsonify({'message': 'User registered successfully!'}), 200

    except Exception as e:
        print("Error during registration:", traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@main.route('/confirm', methods=['POST'])
def confirm_user():
    try:
        data = request.json
        email = data.get("email")
        code = data.get("code")
        
        if not email or not code:
            return jsonify({"error": "Email and confirmation code are required"}), 400
        
        # Use proper environment variables
        secret_hash = get_secret_hash(email, COGNITO_APP_CLIENT_ID, COGNITO_CLIENT_SECRET)
        
        # Call AWS Cognito ConfirmSignUp API
        response = cognito_client.confirm_sign_up(
            ClientId=COGNITO_APP_CLIENT_ID,
            SecretHash=secret_hash,
            Username=email,
            ConfirmationCode=code
        )
        return jsonify({"message": "User confirmed successfully!"}), 200
    except Exception as e:
        print("Error during confirmation:", traceback.format_exc())
        return jsonify({"error": str(e)}), 400

# User Login Endpoint
@main.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        # Validate input
        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        # Calculate SECRET_HASH
        secret_hash = get_secret_hash(email, COGNITO_APP_CLIENT_ID, COGNITO_CLIENT_SECRET)

        # Authenticate user in AWS Cognito
        response = cognito_client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
                'SECRET_HASH': secret_hash
            },
            ClientId=COGNITO_APP_CLIENT_ID
        )

        # Return tokens for authenticated session
        return jsonify({
            'message': 'Login successful!',
            'access_token': response['AuthenticationResult']['AccessToken'],
            'id_token': response['AuthenticationResult']['IdToken']
        }), 200

    except Exception as e:
        print("Error during login:", traceback.format_exc())
        return jsonify({'error': str(e)}), 500

# Product Listing Endpoint
@main.route('/list_product', methods=['POST'])
def list_product():
    try:
        # Extract form data
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        price = request.form['price']
        description = request.form['description']
        image = request.files['file']

        # Upload image to S3
        s3_client.upload_fileobj(
            image,
            S3_BUCKET_NAME,
            f"products/{product_id}/{image.filename}"
        )

        # Create the product object
        product_data = {
            'ProductId': product_id,
            'ProductName': product_name,
            'Price': price,
            'Description': description,
            'ImageURL': f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/products/{product_id}/{image.filename}"
        }

        # Save product to DynamoDB
        table = dynamodb_client.Table(DYNAMODB_TABLE_NAME)
        table.put_item(Item=product_data)

        return jsonify({'message': 'Product listed successfully!', 'product_id': product_id}), 200

    except Exception as e:
        print("Error during product listing:", traceback.format_exc())
        return jsonify({'error': str(e)}), 500

# Get All Products Endpoint
@main.route('/products', methods=['GET'])
def get_products():
    try:
        table = dynamodb_client.Table(DYNAMODB_TABLE_NAME)
        response = table.scan()
        return jsonify(response['Items']), 200

    except Exception as e:
        print("Error while fetching products:", traceback.format_exc())
        return jsonify({'error': str(e)}), 500

# Search Products Endpoint
@main.route('/search', methods=['GET'])
def search_products():
    try:
        query = request.args.get('query')
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400

        # Use DynamoDB scan with filter
        table = dynamodb_client.Table(DYNAMODB_TABLE_NAME)
        response = table.scan(
            FilterExpression="contains(ProductName, :query)",
            ExpressionAttributeValues={":query": query}
        )

        return jsonify(response['Items']), 200

    except Exception as e:
        print("Error during product search:", traceback.format_exc())
        return jsonify({'error': str(e)}), 500