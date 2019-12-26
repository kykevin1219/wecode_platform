import os
import json

import mysql.connector

from my_settings import DATABASE

def batch_view(event, context):
    data       = event['headers']
    connection = mysql.connector.connect(
        user     = DATABASE["user"],
        password = DATABASE["password"],
        host     = DATABASE["host"],
        database = DATABASE["database"],
        use_pure = True)
    cursor = connection.cursor()
    if 'batch' not in data.keys():
        query = "SELECT id, name, gmail, batch, is_active, github_name FROM users"
    else : 
        batch      = data['batch']
        query  = f"""SELECT id, name, gmail, batch, is_active, github_name FROM users WHERE batch = {batch}"""
    cursor.execute(query)
    result = [{
        'id'          : id,
        'name'        : name,
        'gmail'       : gmail,
        'batch'       : batch,
        'is_active'   : is_active,
        'github_name' : github_name
    } for (id, name, gmail, batch, is_active, github_name) in cursor]
    cursor.close()
    connection.close()
    return {
        'statusCode': 200,
        'headers' : {
            'Access-Control-Allow-Origin' : '*'
        },
        'body'      : json.dumps({'result' : result})
    }
