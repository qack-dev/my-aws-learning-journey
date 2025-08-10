# AWSハンズオン：サーバーレスAPI (API Gateway + Lambda + DynamoDB)

## 概要

このプロジェクトは、AWSの主要なサーバーレスサービスである **API Gateway**, **Lambda**, **DynamoDB** を連携させ、基本的なCRUD（作成・読み取り）機能を持つサーバーレスなREST APIを構築するハンズオンの成果物です。

サーバーのプロビジョニングや管理を一切行うことなく、APIリクエストに応じてバックエンドの処理（Pythonコード）を実行し、データベースの情報を操作する、モダンなクラウドネイティブアプリケーションの基本アーキテクチャを学びました。

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

### 1. フルサーバーレスアーキテクチャ
このプロジェクトは、EC2のような仮想サーバーを一切使用していません。

- **（従来比較）** 自宅サーバーでApache/Nginxを設定し、特定のURLへのアクセスをバックエンドのPythonスクリプト（CGI/WSGI）に渡していた処理が、**API Gateway**と**Lambda**の連携に置き換わりました。
- **（学習点）** サーバーのOSやミドルウェアの管理から完全に解放され、コードを書くことだけに集中できるサーバーレスの強力なメリットを体感しました。リクエストがあった時にだけ課金されるため、コスト効率も非常に高いです。

### 2. フルマネージドNoSQLデータベース (DynamoDB)
データの永続化層としてDynamoDBを採用しました。

- **（従来比較）** 自宅サーバーで`CREATE TABLE`していたMariaDBのようなリレーショナルデータベースが、**DynamoDB**に相当します。
- **（学習点）** DynamoDBはスキーマレスなNoSQLデータベースであり、柔軟なデータ構造に対応できます。また、Lambdaと同様にサーバー管理が不要で、アプリケーションの要求に応じて自動でスケールするため、サーバーレス構成との親和性が極めて高いことを理解しました。

### 3. Infrastructure as Code (IaC) への繋がり
今回はコンソールから各サービスを設定しましたが、この一連の構成はCloudFormationやTerraformといったIaCツールでコード化することが可能です。手動設定のプロセスを経験したことで、どのリソースをコードで定義する必要があるかを具体的に理解できました。

## APIエンドポイント仕様

### 投稿を作成 (Create)

- **Method:** `POST`
- **Endpoint:** `/posts`
- **Request Body (JSON):**
  ```json
  {
    "message": "これはテスト投稿です。"
  }
  ```
- **Success Response (201 Created):**
  ```json
  {
    "id": "generated-uuid",
    "message": "これはテスト投稿です。",
    "timestamp": 1678886400
  }
  ```

### 投稿を全件取得 (Read)

- **Method:** `GET`
- **Endpoint:** `/posts`
- **Success Response (200 OK):**
  ```json
  [
    {
      "id": "uuid-1",
      "message": "投稿1",
      "timestamp": 1678886400
    },
    {
      "id": "uuid-2",
      "message": "投稿2",
      "timestamp": 1678886500
    }
  ]
  ```

## セットアップとデプロイ

このプロジェクトは、AWSマネジメントコンソールを通じて以下の手順で構築しました。

1.  **DynamoDB テーブルの作成:**
    - テーブル名: `posts`
    - パーティションキー: `id` (文字列)
    - ソートキー: `timestamp` (数値)
2.  **Lambda 関数の作成 (Pythonランタイム):**
    - `create-post-function`: `create-post-function.py` のコードをデプロイ。DynamoDBへの書き込み権限を持つIAMロールをアタッチ。
    - `get-posts-function`: `get-posts-function.py` のコードをデプロイ。DynamoDBからの読み取り権限を持つIAMロールをアタッチ。
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
