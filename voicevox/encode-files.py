import os
import subprocess

WAV_DIR = "wav"
ENC_DIR = "enc"


def encode_wav(input_file, output_file):
    """ffmpegを使用してWAVファイルをエンコードする"""
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",  # 上書きを許可
                "-i",
                input_file,
                "-acodec",
                "pcm_s16le",  # 16-bit PCM
                "-ac",
                "1",  # モノラル
                "-ar",
                "8000",  # 8kHz
                output_file,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"エンコード成功: {input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"エンコードエラー: {input_file} - {e.stderr}")


def main():
    """メイン処理"""
    if not os.path.exists(ENC_DIR):
        os.makedirs(ENC_DIR)

    for filename in os.listdir(WAV_DIR):
        if filename.endswith(".wav"):
            input_file = os.path.join(WAV_DIR, filename)
            sound_id = filename[:-4]  # 拡張子を取り除く
            output_file = os.path.join(ENC_DIR, f"{sound_id}.wav")
            encode_wav(input_file, output_file)


if __name__ == "__main__":
    main()
