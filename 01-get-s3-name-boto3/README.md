# AWSハンズオン：Python(Boto3)によるS3バケットの自動一覧取得

## 概要

AWSの無料利用枠のみを利用し、PythonとAWS SDK (Boto3) を使って、AWSアカウント内のAmazon S3バケットをプログラムから一覧取得するための基本的な自動化スクリプトです。

AWS認定Cloud Practitioner取得後のスキルアップとして、手動のコンソール操作から一歩進んだ、プログラマティックなAWSリソース操作（クラウド自動化の第一歩）を実践するために作成しました。

## 利用するツールとサービス

このスクリプトを実行するために、以下のツールとAWSサービスが関連します。

- **Amazon S3:** 操作対象のAWSリソース。
- **Python:** 自動化スクリプトを記述するためのプログラミング言語。
- **Boto3 (AWS SDK for Python):** PythonコードからAWSのサービスを操作するための公式ライブラリ。
- **AWS CLI:** ローカルマシンにAWSの認証情報（アクセスキー）を安全に設定するために利用。
- **IAM (Identity and Access Management):** プログラムからのアクセスを許可するためのIAMユーザーとアクセスキー。

## 特徴と学習ポイント

### 1. プログラマティックなAWS操作 (Programmatic Access)
AWSマネジメントコンソールを使った手動操作ではなく、PythonスクリプトによってAWSリソース（S3）の情報を取得します。これは、繰り返し行う作業を自動化するための基本的なスキルであり、Infrastructure as Code (IaC) の考え方に繋がります。

### 2. 安全な認証情報管理 (Secure Credential Management)
スクリプトコード内にアクセスキーを直接書き込む（ハードコーディングする）のではなく、AWS CLIの `aws configure` コマンドで設定した認証情報をBoto3が自動的に利用する構成にしています。これにより、認証情報を安全に扱うベストプラクティスを学びます。

### 3. 独立した開発環境 (Isolated Development Environment)
Pythonの仮想環境 (`venv`) を利用して、プロジェクトに必要なライブラリ (Boto3) をシステム全体から隔離してインストールします。これにより、他のPythonプロジェクトとの依存関係の衝突を防ぎ、クリーンな開発環境を維持する手法を実践します。

## 実行方法

### 前提条件
1.  有効なAWSアカウントを持っていること。
2.  プログラムからのアクセス用に、適切な権限（例: `AmazonS3ReadOnlyAccess`）を持つIAMユーザーを作成し、その**アクセスキーID**と**シークレットアクセスキー**を払い出しておくこと。

### セットアップと実行手順
1.  **AWS CLIのセットアップ**
    ローカルPCに[AWS CLIをインストール](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html)し、以下のコマンドで払い出したアクセスキー情報を設定します。

    ```bash
    aws configure
    ```

2.  **Python環境の準備**
    このリポジトリをローカルにクローンまたはダウンロードし、そのディレクトリ内で以下のコマンドを実行してPython仮想環境の準備とBoto3のインストールを行います。

    ```bash
    # 仮想環境を作成 (初回のみ)
    python -m venv venv

    # 仮想環境を有効化 (Windowsの場合は `venv\Scripts\activate`)
    source venv/bin/activate

    # Boto3ライブラリをインストール
    pip install boto3
    ```

3.  **スクリプトの実行**
    以下のコマンドでPythonスクリプトを実行します。AWSアカウント内に存在するS3バケットの一覧が、作成日時と共に出力されます。

    ```bash
    python list_s3_buckets.py
    ```

## クリーンアップ

このスクリプトはAWSリソースを読み取るだけで、新たなリソースの作成や変更は行わないため、特別なクリーンアップ作業は不要です。

テスト用にS3バケットを作成した場合は、AWSマネジメントコンソールなどから手動で削除してください。
