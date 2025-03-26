import csv
import os
import shutil

CORE_CSV_FILE = "../core-sounds-ja.csv"
GS_CSV_FILE = "../gs-sounds-ja.csv"
ENC_DIR = "enc"
DST_DIR = "dst"


def rename_and_copy(old_filepath, new_filename, destination_dir):
    """ファイル名を変更してコピーする"""
    try:
        # 新しいファイルパスを作成
        new_filepath = os.path.join(destination_dir, new_filename)

        # 新しいファイルパスにサブディレクトリがあれば作成
        os.makedirs(os.path.dirname(new_filepath), exist_ok=True)

        # ファイルをコピー
        shutil.copyfile(old_filepath, new_filepath)
        print(f"ファイルをコピー: {old_filepath} -> {new_filepath}")

    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません: {old_filepath}")
    except Exception as e:
        print(f"エラー: ファイルの移動に失敗しました: {e}")


def main():
    """メイン処理"""

    sound_file_dest = os.path.join(DST_DIR, "ja")

    def _process_csv(csv_file):
        with open(csv_file, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if i == 0:
                    continue  # ヘッダー行をスキップ
                if len(row) >= 2:
                    sound_id = row[0]
                    filepath = row[1]

                    if sound_id and filepath:
                        # 元のファイルパスをencディレクトリに追加
                        old_filepath = os.path.join(ENC_DIR, os.path.basename(sound_id) + ".wav")
                        new_filename = f"{filepath}.wav"
                        rename_and_copy(old_filepath, new_filename, sound_file_dest)
                    else:
                        print(f"スキップ: 不正な行: {row}")
                else:
                    print(f"スキップ: 列が不足: {row}")

    _process_csv(CORE_CSV_FILE)
    _process_csv(GS_CSV_FILE)

    # info.txtを作成 中身は "Japanese"
    with open(os.path.join(DST_DIR, "info.txt"), "w", encoding="utf-8") as f:
        f.write("Japanese")
    print("info.txtを作成しました")

    # tar.gzファイルを作成
    shutil.make_archive(DST_DIR, "gztar", DST_DIR)
    print(f"{DST_DIR}.tar.gzを作成しました")


if __name__ == "__main__":
    main()
