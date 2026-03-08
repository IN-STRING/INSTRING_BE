import torch
import io
import librosa
import requests
import numpy as np
from scipy.signal import medfilt
from app.core.s3.connect_s3 import s3_client
from app.core.config import settings
from app.services.AI_models.chord_model.chord import CordModel

class ChordPredictor:
    def __init__(self, bucket, key, n_class=61, device=None):
        self.device = torch.device(
            device or ("cuda" if torch.cuda.is_available() else "cpu")
        )
        self.s3 = s3_client

        self.SEQ_LEN = 430
        self.sr = 22050
        self.cqt_move = 512
        self.crom = 84

        self.model = CordModel(n_class=n_class).to(self.device)
        state_dict = self._load_from_s3(bucket, key)
        self.model.load_state_dict(state_dict)
        self.model.eval()

        self.num_to_chord = {0: 'N', 1: 'C:maj', 2: 'C:min', 3: 'C:7', 4: 'C:maj7', 5: 'C:min7', 6: 'C#:maj', 7: 'C#:min', 8: 'C#:7', 9: 'C#:maj7', 10: 'C#:min7', 11: 'D:maj', 12: 'D:min', 13: 'D:7', 14: 'D:maj7', 15: 'D:min7', 16: 'D#:maj', 17: 'D#:min', 18: 'D#:7', 19: 'D#:maj7', 20: 'D#:min7', 21: 'E:maj', 22: 'E:min', 23: 'E:7', 24: 'E:maj7', 25: 'E:min7', 26: 'F:maj', 27: 'F:min', 28: 'F:7', 29: 'F:maj7', 30: 'F:min7', 31: 'F#:maj', 32: 'F#:min', 33: 'F#:7', 34: 'F#:maj7', 35: 'F#:min7', 36: 'G:maj', 37: 'G:min', 38: 'G:7', 39: 'G:maj7', 40: 'G:min7', 41: 'G#:maj', 42: 'G#:min', 43: 'G#:7', 44: 'G#:maj7', 45: 'G#:min7', 46: 'A:maj', 47: 'A:min', 48: 'A:7', 49: 'A:maj7', 50: 'A:min7', 51: 'A#:maj', 52: 'A#:min', 53: 'A#:7', 54: 'A#:maj7', 55: 'A#:min7', 56: 'B:maj', 57: 'B:min', 58: 'B:7', 59: 'B:maj7', 60: 'B:min7'}


    def _load_from_s3(self, bucket, key):
        response = self.s3.get_object(Bucket=bucket, Key=key)
        buffer = io.BytesIO(response["Body"].read())
        return torch.load(buffer, map_location=self.device)


    def _predict_song(self, audio_path):
        response = requests.get(audio_path)
        y, SR = librosa.load(response, sr=self.sr)

        cqt = librosa.cqt(y=y, sr=SR, hop_length=self.cqt_move, n_bins=self.crom)
        chroma = librosa.feature.chroma_cqt(C=cqt, n_chroma=12, n_octaves=7)

        chroma = np.abs(chroma)

        mean = chroma.mean()
        std = chroma.std()
        chroma = (chroma - mean) / (std + 1e-7)

        num_frames = chroma.shape[1]
        input_list = []

        for i in range(0, num_frames, self.SEQ_LEN):
            segment = chroma[:, i : i + self.SEQ_LEN]

            if segment.shape[1] < self.SEQ_LEN:
                pad_width = self.SEQ_LEN - segment.shape[1]
                segment = np.pad(segment, ((0, 0), (0, pad_width)), 'constant')

            segment = segment.reshape(1, 12, self.SEQ_LEN)
            input_list.append(segment)

        all_predictions = []

        with torch.no_grad():
            inputs = torch.tensor(np.array(input_list), dtype=torch.float32).to(self.device)

            outputs = self.model(inputs)

            _, preds = torch.max(outputs, 1)

            preds = preds.cpu().numpy()

            for i in range(preds.shape[0]):
                all_predictions.extend(preds[i])

        final_preds = np.array(all_predictions[:num_frames])

        final_preds = medfilt(final_preds, kernel_size=15)

        return final_preds


    def predict_result(self, audio_path):
        chord = ''
        predicted_indices = self._predict_song(audio_path)
        for i, idx in enumerate(predicted_indices):
            if i % 43 == 0:
                # time_sec = librosa.frames_to_time(i, sr=self.sr, hop_length=self.cqt_move)
                chord_name = self.num_to_chord[idx]
                chord += (chord_name + ' ')
                # m, s = divmod(time_sec, 60)
                # print(f"{int(m):02d}:{int(s):02d} -> {chord_name}")
        return chord


Cpredictor = ChordPredictor(
    bucket=settings.S3_BUCKET_NAME,
    key="model_pts/best_chord_model.pth"
)

# print(Cpredictor.predict_result("버스커 버스커(Busker Busker) - 벚꽃 엔딩 [가사_Lyrics].mp3"))