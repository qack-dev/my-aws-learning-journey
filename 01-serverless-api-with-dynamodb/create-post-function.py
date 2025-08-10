#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import boto3
import uuid
import time
import os

# DynamoDBリソースを取得
dynamodb = boto3.resource('dynamodb')
# 操作するテーブル名を指定
table = dynamodb.Table('posts')

def lambda_handler(event, context):
    """
    HTTP POSTリクエストを受け取り、DynamoDBに新しい項目を作成する。
    """
    try:
        # API Gatewayからのリクエスト本文(body)を取得
        # 本文は文字列化されているため、json.loadsで辞書型に変換
        body = json.loads(event.get('body', '{}'))
        
        # 投稿メッセージを取得。もしなければNone
        message = body.get('message')

        # メッセージがない場合はエラーレスポンスを返す
        if not message:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*' # CORS設定
                },
                'body': json.dumps({'error': 'message is required'})
            }

        # DynamoDBに保存する項目を作成
        item = {
            'id': str(uuid.uuid4()),  # ユニークなIDを自動生成
            'message': message,
            'timestamp': int(time.time()) # 現在時刻をUnixタイムスタンプ(数値)で記録
        }
        
        # DynamoDBテーブルに項目を書き込む (CREATE)
        table.put_item(Item=item)
        
        # 成功レスポンスを返す
        return {
            'statusCode': 201, # 201 Created
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(item)
        }

    except Exception as e:
        # エラーが発生した場合のログ出力とエラーレスポンス
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Could not create post'})
        }
