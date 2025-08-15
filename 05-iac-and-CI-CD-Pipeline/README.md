# AWSハンズオン：S3静的サイトのIaC & CI/CDパイプライン構築

## 概要

このプロジェクトは、AWSの基本的なサービスであるS3とCloudFrontを利用して構築された静的ウェブサイトを、より実践的な構成へと進化させるハンズオンの成果物です。

Infrastructure as Code (IaC) の概念をCloudFormationを用いて実践し、さらにGitHubへのソースコードpushをトリガーとしてウェブコンテンツが自動的にデプロイされるCI/CD（継続的インテグレーション/継続的デプロイ）パイプラインをAWS CodePipelineで構築しました。

## 構築されるアーキテクチャ

本プロジェクトは、「**インフラを定義・管理するIaCのフロー**」と、「**コンテンツを自動デプロイするCI/CDのフロー**」という2つの主要な流れで構成されています。

### CI/CD フロー (コンテンツ更新)
開発者がローカルでコンテンツ（HTML/CSS）を編集し、GitHubリポジトリにプッシュすると、その変更が自動的にS3バケットに反映されます。

**[ Local PC ] --- `git push` ---> [ GitHub ] --- `Webhook` ---> [ AWS CodePipeline ] --- `Deploy` ---> [ Amazon S3 ]**

### IaC & 配信フロー (インフラ構成)
AWS CloudFormationテンプレート (`template.yaml`) によって、セキュアなコンテンツ配信基盤がコードとして定義・管理されています。S3バケットは非公開に保たれ、CloudFrontからのアクセスのみがOrigin Access Control (OAC) によって許可されます。

**[ User ] <--- `HTTPS` --- [ CloudFront ] <--- `OAC` --- [ Amazon S3 (Private) ]**

## 特徴と学習ポイント

### 1. Infrastructure as Code (IaC) with CloudFormation
手動でのコンソール操作に頼らず、インフラ構成（S3, CloudFront, OAC, IAM Policy等）をすべて`template.yaml`という単一のコードで管理しています。これにより、ヒューマンエラーを削減し、誰でも何度でも全く同じインフラを迅速かつ正確に再現することが可能です。差分更新の仕組みにより、変更箇所のみを安全に適用できる点も学習しました。

### 2. Automated Deployment (CI/CD) with CodePipeline
GitHubの`main`ブランチへのpushをトリガーに、AWS CodePipelineが自動的にソースコードを取得し、ターゲットとなるS3バケットへコンテンツをデプロイするパイプラインを構築しました。これにより、手動でのアップロード作業が不要となります。

### 3. Enhanced Security with OAC (Origin Access Control)
当初はパブリックアクセスを許可していたS3バケットを、AWSのセキュリティベストプラクティスに従って完全にプライベート化しました。CloudFrontからS3へのアクセスにはOACを利用することで、ユーザーがS3バケットに直接アクセスすることを防ぎ、CloudFront経由のセキュアなコンテンツ配信のみを強制する構成を実現しています。これは、Trusted Advisorの警告をIaCで解決する実践的な経験となりました。

## 苦慮した点

このハンズオンは、チュートリアル通りに進めるだけでは完了しない、数多くの実践的なトラブルシューティングの連続でした。以下にその過程で直面し、解決した問題点を記録します。

### 1. CloudFormationのデプロイエラー
*   **文字コード問題:** 当初、Windows環境のCLIから日本語コメントを含む`template.yaml`をデプロイしようとした際、`cp932 codec can't decode`エラーに遭遇しました。ファイルの文字コードを**UTF-8**で保存し直すことで解決しました。
*   **不正なパラメータ:** CloudFrontのオリジンにS3のウェブサイトエンドポイントURL (`!GetAtt S3Bucket.WebsiteURL`) を指定したところ、URLに含まれる`:`（コロン）が原因で`Invalid request`エラーが発生。`!Sub`関数を用いて正しいドメイン名を動的に生成する方法に修正して解決しました。

### 2. CodeCommitの仕様変更とGitHubへの切り替え
当初の計画ではAWS CodeCommitをソースリポジトリとして利用する予定でした。しかし、**CodeCommitが新規AWSユーザーには利用できなくなっている**という重要なポリシー変更に直面。急遽、より汎用性の高い**GitHub**をソースとしてパイプラインを構築する方針に切り替えました。

### 3. CodePipelineとGitHubの複雑な権限エラー
CI/CDパイプラインの構築において、最も多くの時間と思考を要したのが権限設定でした。
*   **`No Branch [main] found` エラー:** パイプライン設定は正しいにも関わらず、ブランチが見つからないエラーに遭遇。原因は、AWSコンソール側で接続を作成しただけでは不十分で、**GitHub側で「AWS Connector for GitHub」アプリを明示的にインストールし、リポジトリへのアクセスを許可**する必要があったためでした。
*   **`The provided role does not have sufficient permissions` エラー:** 上記を解決後、今度はIAMロールの権限不足エラーが発生。調査を進めると、CodePipelineのサービスロールに`codestar-connections:UseConnection`アクションの許可が不足していることが判明。さらに、トラブルシューティングの過程で複数の古いポリシーが自動生成されており、**「正しいアクション」と「正しいリソース（接続ARN）」が別々のポリシーに記述されている**という根本原因を突き止めました。不要なポリシーを削除し、単一の正しいポリシーに統合・修正することで、最終的にこの問題を解決しました。

これらの経験を通じて、AWSのドキュメントやサービス間の連携を理解し、原因を特定する実践的なトラブルシューティングを行うことができました。
