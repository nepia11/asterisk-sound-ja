import csv
import os
import requests

CSV_FILE = "../core-sounds-ja.csv"
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


def load_query(filename):
    """JSONファイルを読み込む"""
    filepath = os.path.join("query", filename)
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

    with open(CSV_FILE, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i == 0:
                continue  # Skip header row
            if len(row) >= 1:
                sound_id = row[0]

                if sound_id:
                    query_filename = f"{sound_id}.json"
                    query_json = load_query(query_filename)
                    if query_json:
                        wav_data = generate_wav(query_json)
                        if wav_data:
                            filename = f"{sound_id}.wav"
                            save_wav(wav_data, filename)
                else:
                    print(f"スキップ: 不正な行: {row}")
            else:
                print(f"スキップ: 列が不足: {row}")


if __name__ == "__main__":
    import json  # import文をここに移動

    main()
