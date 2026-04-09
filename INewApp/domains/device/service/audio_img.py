import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_audio_img(wav_path: str, output_path: str):
    y, sr = librosa.load(wav_path, sr=None)

    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_axis_off()

    librosa.display.waveshow(y, sr=sr, ax=ax, color="#FF3B30")

    fig.patch.set_facecolor("black")
    fig.savefig(
        output_path,
        bbox_inches="tight",
        pad_inches=0,
        facecolor="black",
        dpi=150,
    )
    plt.close(fig)