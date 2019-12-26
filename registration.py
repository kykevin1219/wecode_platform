import os
import ssl
import jwt
import json
import smtplib
import requests

import mysql.connector

from mysql.connector        import errorcode
from mysql.connector.errors import Error
from email                  import encoders
from email.mime.text        import MIMEText
from email.mime.multipart   import MIMEMultipart

from letter import html
from my_settings import DATABASE, JWT_SECRET, SENDER

def registration(event, context):
    try :
        body       = json.loads(event['body'])
        users      = body['users']
        batch      = body['batch']
        users_list = [(user['name'], user['gmail'], batch) for user in users]
        connection = mysql.connector.connect(
            user     = DATABASE["user"],
            password = DATABASE["password"],
            host     = DATABASE["host"],
            database = DATABASE["database"],
            use_pure = True)
        cursor           = connection.cursor()
        add_users        = """INSERT INTO users (name, gmail, batch) VALUES (%s, %s, %s) """
        cursor.executemany(add_users, users_list)
        connection.commit()
        registered_users = cursor.rowcount
        
        gmails     = [user["gmail"] for user in users]
        format_string = ','.join(['%s'] * len(gmails))
        query      = ("SELECT id, name, gmail,batch FROM users where gmail IN (%s)" %format_string)
        cursor.execute(query, tuple(gmails))
        recipients = []
        for (id, name, gmail, batch) in cursor: 
            recipients.append({
                "id"    : id,
                "name"  : name,
                "gmail" : gmail,
                "batch" : batch
            })
        for recipient in recipients:
            # Create a secure SSL context
            port        = 465  # For SSL
            smtp_server = "smtp.gmail.com"
            message     = MIMEMultipart("alternative")
            context     = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login(SENDER["email"], SENDER["password"])
                message            = MIMEMultipart("alternative")
                message["Subject"] = "[WECODE]환영합니다!"
                message["From"]    = SENDER["email"]
                payload            = {"user_id": recipient["id"]}
                mail_token           = jwt.encode(payload, JWT_SECRET, algorithm = "HS256").decode("UTF-8")
                message.attach(
                    MIMEText(
                        html.format(
                            name  = recipient["name"],
                            batch = recipient["batch"],
                            token = mail_token,
                        ), "html")
                )
                server.sendmail(
                    SENDER["email"],
                    recipient["gmail"],
                    message.as_string(),
                )
                server.quit()
        
        
        result_message   = f"""{registered_users} USERS CREATED"""
        cursor.close()
        connection.close()
    except mysql.connector.IntegrityError:
        return {
            'statusCode' : 409,
            'headers' : {
                'Access-Control-Allow-Headers' : '*'
            },
            'body'       : json.dumps({'error' : "IntegrityError"})
        }
    except KeyError:
        return {
            'statusCode' : 400,
            'headers' : {
                'Access-Control-Allow-Headers' : '*'
            },
            'body'       : json.dumps({'error' : "KEY_ERROR"})
        }
    return {
        'statusCode' : 200,
        'headers' : {
            'Access-Control-Allow-Origin' : '*'
        },
        'body'       : json.dumps({'message' : result_message})
    } 
