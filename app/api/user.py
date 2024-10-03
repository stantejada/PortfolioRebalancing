from flask import Blueprint, jsonify, request
from app.models import User
from app import db
from flask_login import login_required
from flasgger import swag_from

api = Blueprint('user', __name__)

#GET USER DATA
@api.route('/user/<int:id>', methods=['GET'])
@login_required
@swag_from({
    'tags':['User'],
    'parameters': [
        {
            'name': 'id',
            'type': 'integer',
            'required' : True,
            'in': 'path',
            'description' : 'ID of the user to retriever'
        }    
    ],
    'responses':{
        200 : {
            'description': 'User found',
            'schema': {
                'id': 'User',
                'properties':{
                    'username' : {'type':'string', 'example':'johndoe'},
                    'email' : {'type':'string', 'example':'johndoe@test.com'}
                }
            }
        },
        400 : {
            'description':'User not found'
        }
    }
})
def get_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'error': 'User not found!'}), 404
    return jsonify(user.to_json()), 200


#REGISTER NEW USER
@api.route('user/register', methods=['POST'])
@swag_from({
    'tags': ['User'],
    'parameters': [
        {
            'name': 'user',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'Username of the user to create',
                        'example': 'johndoe'
                    },
                    'email': {
                        'type': 'string',
                        'description': 'Email for the user to create',
                        'example': 'johndoe@test.com'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Password for user to create',
                        'example': 'securepassword'
                    },
                    'repeat_password': {
                        'type': 'string',
                        'description': 'Repeat password to match the original password',
                        'example': 'securepassword'
                    }
                },
                'required': ['username', 'email', 'password', 'repeat_password']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User has been registered successfully'
        },
        400: {
            'description': 'Bad request, invalid input or user already exists'
        },
        404: {
            'description': 'Passwords do not match'
        }
    }
})
def create_user():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            repeat_password = data.get('repeat_password')
            
            if not username or not email or not password or not repeat_password:
                return jsonify({'error':'All fields are required'}),400
            
            if password != repeat_password:
                return jsonify({'error': 'Passwords do not match!'}), 404
            
            user_exist = User.query.filter((User.username == username or (User.email == email))).first()
            
            if user_exist:
                return jsonify({'error': 'Username or Email already exist'}), 400
            
            new_user = User(username= username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            return jsonify({'message': 'User has been registered successfully'}), 201

#DELETE USER BY ID     
@api.route('/user/delete/<int:id>', methods=['DELETE'])
@login_required
@swag_from({
    'tags':['User'],
    'parameters': [
        {
        'name': 'id',
        'type':'integer',
        'required' : True,
        'in':'path',
        'description' : 'ID for the user to delete'
        }
        ],
    'responses': {
        200 : {
            'description' : 'User delete',
            'schema' : {
                'type' : 'object',
                'properties' : {
                    'message' : {
                        'type' : 'string',
                        'example': 'User has been deleted successfully!'
                    }
                }
            }
        },
        404 : {
            'description' : 'User not found',
            'shema': {
                'type' : 'object',
                'properties' : {
                    'error' : {
                        'type' : 'string',
                        'example' : 'User not found!'
                    }
                }
            }
        },
        400 : {
            'description' : 'An error ocurred, user cannot be deleted',
            'shema':{
                'type' : 'object',
                'properties' : {
                    'error' : {
                        'type' : 'string',
                        'example' : 'An error ocurred while trying to delete user'
                    }
                }
            }
        }
        
    }
})
def delete_user(id):
    user = User.query.get(id)
    
    if user is None:
        return jsonify({'error':'User not found!'}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        return jsonify({'error':'An error ocurred while trying to delete the user'}), 500
    
    return jsonify({'message':'User has been deleted successfully'}), 204


#UPDATE ALL USER'S DATA
@api.route('/user/update/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    user = User.query.get(id)
    
    if user is None:
        return jsonify({"error": "User not found!"}), 404
    
    if request.method == 'PUT':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            if not username or not email:
                return jsonify({'error':"Username and Email are required"}), 400
            
            user.username = username
            user.email = email
            
            if password:
                user.set_password(password)
                
            db.session.commit()
        
            return jsonify({'message':'User has been updated'}), 200
        
    return jsonify({"error": "Request must be JSON"}), 400

