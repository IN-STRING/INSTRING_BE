import torch
import io
import librosa
import requests
import numpy as np
from app.core.s3.connect_s3 import s3_client
from app.core.config import settings
from app.services.AI_models.SAT_model.SAT import CNNLSTM


class FingerstylePredictor:
    CLASS_NAMES = ["arpeggio", "fingerstyle", "stroke"]
    TEMPO_NAMES = ["slow", "mid", "fast"]

    def __init__(self, bucket, key, device=None):
        self.device = torch.device(
            device or ("cuda" if torch.cuda.is_available() else "cpu")
        )
        self.s3 = s3_client

        self.sr = 22050
        self.duration = 4
        self.n_mels = 128

        self.model = CNNLSTM().to(self.device)
        state_dict = self._load_from_s3(bucket, key)
        self.model.load_state_dict(state_dict)
        self.model.eval()

    def _load_from_s3(self, bucket, key):
        response = self.s3.get_object(Bucket=bucket, Key=key)
        buffer = io.BytesIO(response["Body"].read())
        return torch.load(buffer, map_location=self.device)

    def _preprocess(self, file_path):
        response = requests.get(file_path)
        y, _ = librosa.load(response, sr=self.sr, mono=True)

        target_len = self.sr * self.duration
        if len(y) > target_len:
            y = y[:target_len]
        else:
            y = np.pad(y, (0, target_len - len(y)))

        mel = librosa.feature.melspectrogram(
            y=y,
            sr=self.sr,
            n_mels=self.n_mels
        )
        mel = librosa.power_to_db(mel, ref=np.max)

        tensor = torch.tensor(mel, dtype=torch.float32)
        tensor = tensor.unsqueeze(0).unsqueeze(0).to(self.device)
        return tensor


    @staticmethod
    def _estimate_temp(file_path, sr=22050):
        response = requests.get(file_path)
        y, sr = librosa.load(response, sr=sr)

        duration = librosa.get_duration(y=y, sr=sr)

        if duration >= 6:
            n_chunks = 5
        elif duration >= 3:
            n_chunks = 3
        else:
            n_chunks = 1

        chunk_length = len(y) // n_chunks
        tempos = []

        for i in range(n_chunks):
            start = i * chunk_length
            end = (i + 1) * chunk_length
            y_chunk = y[start:end]

            if len(y_chunk) < sr:
                continue

            onset_env = librosa.onset.onset_strength(y=y_chunk, sr=sr)
            tempo, _ = librosa.beat.beat_track(
                onset_envelope=onset_env,
                sr=sr
            )

            # t_val = float(tempo)
            t_val = float(np.atleast_1d(tempo)[0])
            tempos.append(t_val)

        if len(tempos) == 0:
            return 0

        final_tempo = np.median(tempos)

        if final_tempo < 60:
            final_tempo *= 2
        elif final_tempo > 180:
            final_tempo /= 2

        return final_tempo

    @staticmethod
    def _tempo_label(tempo):
        if tempo < 100:
            return 0  # slow
        elif tempo <= 140:
            return 1  # mid
        else:
            return 2  # fast


    def analyze_guitar_performance(self, file_path):
        input_data = self._preprocess(file_path)

        with torch.no_grad():
            output = self.model(input_data)
            style_idx = torch.argmax(output, dim=1).item()
            style_name = self.CLASS_NAMES[style_idx]

        bpm = self._estimate_temp(file_path)
        t_label_idx = self._tempo_label(bpm)
        t_label_name = self.TEMPO_NAMES[t_label_idx]

        return {
            "style": style_name,
            "bpm": round(bpm),
            "tempo": t_label_name,
        }

FSpredictor = FingerstylePredictor(
    bucket=settings.S3_BUCKET_NAME,
    key="model_pts/fingerstyle_best_model.pt"
)


# result = FSpredictor.analyze_guitar_performance("Kotaro Oshio - 「Fight!」 _ Guitar Cover.mp3")
# print(result)