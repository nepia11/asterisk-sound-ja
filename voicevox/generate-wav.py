import os
import requests
import json  # jsonをインポート
import argparse

QUERY_DIR = "query"
WAV_DIR = "wav"
VOICEVOX_URL = "127.0.0.1:50021"


def generate_wav(query_json, speaker=10006):
    """VOICEVOX APIを呼び出してWAVファイルを生成する"""
    try:
        response = requests.post(
            f"http://{VOICEVOX_URL}/synthesis",
            headers={"Content-Type": "application/json"},
            params={"speaker": speaker},
            json=query_json,
        )
        response.raise_for_status()  # HTTPエラーをチェック
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"API呼び出しエラー: {e}")
        return None


def load_query(filepath):
    """JSONファイルを読み込む"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"JSONファイル読み込みエラー: {e}")
        return None


def save_wav(wav_data, filename):
    """WAVファイルを保存する"""
    filepath = os.path.join(WAV_DIR, filename)
    try:
        with open(filepath, "wb") as f:
            f.write(wav_data)
        print(f"ファイル保存: {filepath}")
    except Exception as e:
        print(f"ファイル保存エラー: {e}")


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description="VOICEVOX音声合成WAV生成スクリプト")
    parser.add_argument("--sound_id", help="特定のsound_idを指定して処理する")
    args = parser.parse_args()

    if not os.path.exists(WAV_DIR):
        os.makedirs(WAV_DIR)

    query_dir = QUERY_DIR  # queryディレクトリを指定

    filenames = os.listdir(query_dir)
    filenames.sort()
    total = len(filenames)

    for i, filename in enumerate(filenames):
        if filename.endswith(".json"):
            sound_id = filename[:-5]  # 拡張子を取り除く

            if args.sound_id and sound_id != args.sound_id:
                continue  # 特定のsound_idが指定された場合、それ以外のファイルはスキップ

            filepath = os.path.join(query_dir, filename)
            query_json = load_query(filepath)
            if query_json:
                wav_data = generate_wav(query_json)
                if wav_data:
                    wav_filename = f"{sound_id}.wav"
                    save_wav(wav_data, wav_filename)
            else:
                print(f"スキップ: 不正なJSONファイル: {filename}")
            # 進捗表示
            print(f"Progress {i+1}/{total} {filename}")


if __name__ == "__main__":
    main()
