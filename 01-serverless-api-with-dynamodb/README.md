# AWSハンズオン：サーバレスAPI (API Gateway + Lambda + DynamoDB)

## 概要

このプロジェクトは、AWSの主要なサーバレスサービスである **API Gateway**, **Lambda**, **DynamoDB** を連携させ、基本的なCRUD（作成・読み取り）機能を持つサーバレスなREST APIを構築するハンズオンの成果物です。

サーバのプロビジョニングや管理を一切行うことなく、APIリクエストに応じてバックエンドの処理（Pythonコード）を実行し、データベースの情報を操作する、モダンなクラウドネイティブアプリケーションの基本アーキテクチャを学びました。

## アーキテクチャ

このAPIは以下のシンプルな流れで動作します。

```
[クライアント] <=> [API Gateway] <=> [Lambda関数] <=> [DynamoDBテーブル]
```

1.  クライアント（Webブラウザやcurlなど）がAPI Gatewayにリクエストを送信します。
2.  API GatewayはリクエストのパスやHTTPメソッドに応じて、適切なLambda関数をトリガーします。
3.  Lambda関数内のPythonコードが実行され、必要に応じてDynamoDBテーブルのデータを操作します。
4.  実行結果がAPI Gatewayを経由してクライアントに返却されます。

## 使用したAWSサービスと技術

- **Amazon API Gateway:** Lambda関数を外部に公開するためのAPIエンドポイントを作成・管理。
- **AWS Lambda:** リクエストを処理するバックエンドロジックをPythonで実装。
- **Amazon DynamoDB:** 投稿データを保存するフルマネージドNoSQLデータベース。
- **Python (Boto3):** Lambda関数からDynamoDBを操作するために使用したAWS SDK。
- **IAM (Identity and Access Management):** 各サービス間の連携を安全に許可するためのロールとポリシー。

## 特徴と学習ポイント

### 1. フルサーバレスアーキテクチャ
このプロジェクトは、EC2のような仮想サーバを一切使用していません。

- **（従来比較）** 自宅サーバでApacheを設定し、特定のURLへのアクセスをバックエンドのPythonスクリプトに渡していた処理が、**API Gateway**と**Lambda**の連携に置き換わりました。
- **（学習点）** サーバのOSやミドルウェアの管理から解放され、コードを書くことだけに集中できるサーバレスを体感しました。

### 2. フルマネージドNoSQLデータベース (DynamoDB)
DynamoDBを採用しました。

- **（従来比較）** 自宅サーバで`CREATE TABLE`していたMariaDBが、**DynamoDB**に相当します。
- **（学習点）** DynamoDBはNoSQLデータベースであり、柔軟なデータ構造に対応できます。また、Lambdaと同様にサーバ管理が不要で、アプリケーションの要求に応じて自動でスケールするため、サーバレス構成との親和性が高いことを理解しました。

## API仕様

### 作成 (Create)

  ```bash
    curl -X POST -H "Content-Type: application/json" -d "{\"message\": \"初めてのサーバレス投稿です！\"}" "https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/v1/posts"
  ```

### 全件取得 (Read)

  ```bash
    curl -X GET "https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/v1/posts"
  ```

## セットアップとデプロイ

このプロジェクトは、AWSマネジメントコンソールを通じて以下の手順で構築しました。

1.  **DynamoDB テーブルの作成:**
    - テーブル名: `posts`
    - パーティションキー: `id` (文字列)
    - ソートキー: `timestamp` (数値)
2.  **Lambda 関数の作成 (Pythonランタイム):**
    - `create-post-function`: `create-post-function.py` のコード。DynamoDBへの書き込み権限を持つIAMロールをアタッチ。
    - `get-posts-function`: `get-posts-function.py` のコード。DynamoDBからの読み取り権限を持つIAMロールをアタッチ。
3.  **API Gateway の設定:**
    - 新しいREST APIを作成。
    - `/posts` リソースを作成。
    - `GET` メソッドを作成し、`get-posts-function` と統合。
    - `POST` メソッドを作成し、`create-post-function` と統合。
    - APIをデプロイしてエンドポイントURLを取得。

## クリーンアップ

意図しない課金を防ぐため、ハンズオン終了後は以下のリソースを削除してください。

1.  API Gatewayで作成したAPI。
2.  作成した2つのLambda関数。
3.  関数の実行に伴いCloudWatch Logsに作成されたロググループ。
4.  Lambda関数にアタッチしたIAMロール。
5.  DynamoDBの`posts`テーブル。
