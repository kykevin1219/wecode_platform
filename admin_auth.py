import os
import jwt
import json

import mysql.connector

from my_settings import DATABASE, JWT_SECRET

def admin_auth(event, context):
    try : 
        token = event["authorizationToken"]
        user_info     = jwt.decode(token, JWT_SECRET, algorithm = "HS256")
        user_id       = user_info["user_id"]
        connection    = mysql.connector.connect(
            user     = DATABASE["user"],
            password = DATABASE["password"],
            host     = DATABASE["host"],
            database = DATABASE["database"],
            use_pure = True)
        cursor = connection.cursor()
        query  = f"""SELECT position FROM users_positions RIGHT JOIN positions ON users_positions.position_id = positions.id WHERE user_id = {user_id}"""
        cursor.execute(query)
        user_positions = [position[0] for position in cursor]
        if "admin" not in user_positions:
            return {
                'policyDocument' : {
                    "Version"    : "2012-10-17",
                    "Statement"  : [
                        {
                            "Action"  : "execute-api:Invoke",
                            "Effect"  : "Deny",
                            "Resource": [
                                "arn:aws:execute-api:ap-northeast-2:194148625732:aq9yrbcbg5/*/GET/users/batch-view",
                                "arn:aws:execute-api:ap-northeast-2:194148625732:aq9yrbcbg5/*/POST/users/registration"
                            ]
                        }
                    ]
                }   
            }
    except jwt.DecodeError: 
        return {
            'policyDocument' : {
                "Version"    : "2012-10-17",
                "Statement"  : [
                    {
                        "Action"  : "execute-api:Invoke",
                        "Effect"  : "Deny",
                        "Resource": [
                            "arn:aws:execute-api:ap-northeast-2:194148625732:aq9yrbcbg5/*/GET/users/batch-view",
                            "arn:aws:execute-api:ap-northeast-2:194148625732:aq9yrbcbg5/*/POST/users/registration"
                        ]
                    }
                ]
            }   
        }
    
    return {
        'policyDocument' : {
            "Version"    : "2012-10-17",
            "Statement"  : [
                {
                    "Action"  : "execute-api:Invoke",
                    "Effect"  : "Allow",
                    "Resource": [
                        "arn:aws:execute-api:ap-northeast-2:194148625732:aq9yrbcbg5/*/GET/users/batch-view",
                        "arn:aws:execute-api:ap-northeast-2:194148625732:aq9yrbcbg5/*/POST/users/registration"
                    ]    
                }
            ]
        }
    }
