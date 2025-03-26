import os
import requests
import json  # jsonをインポート

QUERY_DIR = "query"
WAV_DIR = "wav"
VOICEVOX_URL = "127.0.0.1:50021"


def generate_wav(query_json, speaker=2):
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
    if not os.path.exists(WAV_DIR):
        os.makedirs(WAV_DIR)

    query_dir = QUERY_DIR  # queryディレクトリを指定

    for filename in os.listdir(query_dir):
        if filename.endswith(".json"):
            sound_id = filename[:-5]  # 拡張子を取り除く
            filepath = os.path.join(query_dir, filename)
            query_json = load_query(filepath)
            if query_json:
                wav_data = generate_wav(query_json)
                if wav_data:
                    wav_filename = f"{sound_id}.wav"
                    save_wav(wav_data, wav_filename)
            else:
                print(f"スキップ: 不正なJSONファイル: {filename}")


if __name__ == "__main__":
    main()
