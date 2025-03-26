# VOICEVOX 音声プロンプト生成スクリプト

このディレクトリには、VOICEVOXを使用してAsteriskの音声プロンプトを生成するためのスクリプトが含まれています。

## 必要なソフトウェア

- Python 3.7以上
- requests
- ffmpeg
- VOICEVOXエンジン

## 実行手順

1.  VOICEVOXエンジンを起動します。
    1.  voicevoxディレクトリに移動したあと、以下のコマンドを実行します:

        ```bash
        docker-compose up -d
        ```
    2.  VOICEVOXエンジンが起動したことを確認します:

        ```bash
        curl http://localhost:50021/speakers | jq
        ```
2.  必要なPythonライブラリをインストールします:

    ```bash
    pip install requests
    ```
3.  `generate-query.py` を実行して、音声合成クエリを生成します:

    ```bash
    python3 generate-query.py
    ```

4.  `generate-wav.py` を実行して、WAVファイルを生成します:

    ```bash
    python3 generate-wav.py
    ```

5.  `encode-files.py` を実行して、WAVファイルをAsteriskで利用できる形式にエンコードします:

    ```bash
    python3 encode-files.py
    ```

6.  `rename-files.py` を実行して、ファイルをリネームして適切なディレクトリに移動し、パッケージを作成します:

    ```bash
    python3 rename-files.py
    ```

## 生成されるファイル

- `query/`: 音声合成クエリのJSONファイルが保存されます。
- `wav/`: 生成されたWAVファイルが保存されます。
- `enc/`: エンコードされたWAVファイルが保存されます。
- `dst/`: リネームおよび移動されたファイルが保存されます。
- `gs-sounds-ja.tar.gz`: Asteriskで使用できる音声プロンプトパッケージ。

## 注意事項

- このスクリプトは、VOICEVOXのAPIを利用して音声合成を行います。VOICEVOXのライセンスおよび利用規約を遵守してください。
- 生成された音声プロンプトの品質は、VOICEVOXエンジンの設定に依存します。
- スクリプトの実行には、適切な権限が必要です。
