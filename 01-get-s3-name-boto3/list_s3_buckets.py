#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3

def main():
    """
    AWSアカウント内のすべてのS3バケットを一覧表示し、
    それぞれの名前と作成日時を出力します。
    """
    try:
        # S3サービスクライアントを作成
        s3_client = boto3.client('s3')

        # バケットの一覧を取得
        response = s3_client.list_buckets()

        print("S3バケット一覧:")
        
        # バケット情報が'Buckets'キーに含まれているか確認
        if 'Buckets' in response and response['Buckets']:
            # 取得したバケットの数だけループ処理
            for bucket in response['Buckets']:
                bucket_name = bucket['Name']
                creation_date = bucket['CreationDate']
                # F-stringを使って分かりやすく整形して出力
                print(f"- {bucket_name} (作成日: {creation_date.strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            print("S3バケットは見つかりませんでした。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
