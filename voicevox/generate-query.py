import csv
import json
import os
import requests  # requestsライブラリをインポート
import subprocess

CSV_FILE = "../core-sounds-ja.csv"
QUERY_DIR = "query"
VOICEVOX_URL = "127.0.0.1:50021"


def generate_query(text, speaker=2):
    """VOICEVOX APIを呼び出して音声合成クエリを生成する (requestsを使用)"""
    try:
        response = requests.post(f"http://{VOICEVOX_URL}/audio_query", params={"speaker": speaker, "text": text})
        response.raise_for_status()  # HTTPエラーをチェック
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API呼び出しエラー: {e}")
        return None


def save_query(query, filename):
    """クエリをJSONファイルに保存する"""
    filepath = os.path.join(QUERY_DIR, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(query, f, indent=4, ensure_ascii=False)
        print(f"ファイル保存: {filepath}")
    except Exception as e:
        print(f"ファイル保存エラー: {e}")


def modify_pitch(query):
    """音声合成クエリのピッチを変更する"""
    if "pitchScale" in query:
        query["pitchScale"] -= 0.05
    if "intonationScale" in query:
        query["intonationScale"] = 0.8
    return query


def main():
    """メイン処理"""
    if not os.path.exists(QUERY_DIR):
        os.makedirs(QUERY_DIR)

    with open(CSV_FILE, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i == 0:
                continue  # Skip header row
            if len(row) >= 3:
                sound_id = row[0]
                text = row[2]

                if sound_id and text:
                    query = generate_query(text)
                    if query:
                        filename = f"{sound_id}.json"
                        query = modify_pitch(query)
                        save_query(query, filename)
                else:
                    print(f"スキップ: 不正な行: {row}")
            else:
                print(f"スキップ: 列が不足: {row}")


if __name__ == "__main__":
    main()
