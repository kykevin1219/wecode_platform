import os
import jwt
import json
import requests

import mysql.connector

from my_settings import DATABASE, SENDER, JWT_SECRET, GITHUB

def github_login(event, context):
    data       = json.loads(event["body"])
    connection = mysql.connector.connect(
        user     = DATABASE["user"],
        password = DATABASE["password"],
        host     = DATABASE["host"],
        database = DATABASE["database"],
        use_pure = True)
    cursor           = connection.cursor()
    headers          = {"Accept" : "application/json"}
    code             = data["code"]
    state            = data["state"]
    access_token_url = "https://github.com/login/oauth/access_token"
    payloads = {
        "client_id"     : GITHUB["id"],
        "client_secret" : GITHUB["secret"],
        "code" : code,
        "state" : state
    }
    if len(code) == 0:
        return {
            'statusCode' : 400,
            'headers' : {
                'Access-Control-Allow-Headers' : '*'
            },
            'body'       : json.dumps({'error' : 'NO_CODE'})
        }
    if len(state) == 0:
        return {
            'statusCode' : 400,
            'headers' : {
                'Access-Control-Allow-Headers' : '*'
            },
            'body'       : json.dumps({'error' : 'NO_STATE'})
        }
    try : 
        response      = requests.post(access_token_url, headers = headers, params = payloads).json()
        access_token  = response["access_token"]
        user_data_url = f"""https://api.github.com/user?access_token={access_token}"""
        user_data     = requests.get(user_data_url, headers = headers).json()
        github_name   = user_data["login"]
        cursor.execute(f"""SELECT * FROM users WHERE github_name = '{github_name}'""")
        results       = [result for result in cursor]
        if len(results) == 0 and ('mail' in data.keys()) : ##회원가입이 안되어있는데 수강생인경우
            mail_jwt = data['mail']
            print(mail_jwt)
            std_info    = jwt.decode(mail_jwt, JWT_SECRET, algorithm = "HS256")
            std_id      = std_info["user_id"]
            print(std_id)
            cursor.execute(f"""UPDATE users SET is_active = True, github_name = '{github_name}' WHERE id = {std_id}""")
            connection.commit()
            cursor.close()
            connection.close()
            payload     = {"user_id" : std_id}
            login_token = jwt.encode(payload, JWT_SECRET, algorithm = "HS256").decode("UTF-8")
            
            return {
                'statusCode'  : 200,
                'headers' : {
                    'Access-Control-Allow-Headers' : '*'
                },
                'body'        : json.dumps({
                    'jwt'     : login_token,
                    'message' : "NEW_USER"
                })
            } 
            
        if len(results) == 0 and ('mail' not in data.keys()) : ## 받으면 안되는 경우
            print(data)
            return {
                'statusCode' : 401,
                'headers' : {
                    'Access-Control-Allow-Headers' : '*'
                },
                'body'       : json.dumps({'error' : 'WRONG_ACCESS'}) 
            }
        cursor.close()
        connection.close()
        std_id      = results[0][0]
        payload     = {"user_id" : std_id}
        login_token = jwt.encode(payload, JWT_SECRET, algorithm = "HS256").decode("UTF-8")
    except KeyError: 
        return {
            'statusCode' : 400,
            'headers' : {
                'Access-Control-Allow-Headers' : '*'
            },
            'body'       : json.dumps({'error' : 'KEY_ERROR'})
        }
    return {
        'statusCode': 200,
        'headers' : {
            'Access-Control-Allow-Headers' : '*'
        },
        'body'      : json.dumps({'jwt' : login_token})
    }
