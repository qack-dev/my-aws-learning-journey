#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import boto3
from decimal import Decimal
import os

# DynamoDBから取得したDecimal型をJSONで扱えるように変換するヘルパークラス
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # 数値が整数か小数かで変換方法を分ける
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        return super(DecimalEncoder, self).default(obj)

# DynamoDBリソースを取得
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('posts')

def lambda_handler(event, context):
    """
    DynamoDBのpostsテーブルから全項目を取得して返す。
    """
    try:
        # DynamoDBテーブルの全項目をスキャン(全件取得)する (READ)
        response = table.scan()
        
        # 取得した項目をレスポンスとして返す
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' # CORS設定
            },
            # DecimalEncoderを使ってJSONシリアライズする
            'body': json.dumps(response.get('Items', []), cls=DecimalEncoder)
        }
        
    except Exception as e:
        # エラーハンドリング
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Could not retrieve posts'})
        }
