from pydub import AudioSegment
import ffmpeg
from pathlib import Path

AudioSegment.converter = r"C:\Dependencies\ffmpeg\bin\ffmpeg.exe"


class AudioUtils:
    @staticmethod
    def __save_audio(sound: AudioSegment, save_as: Path):
        sound.export(save_as.__str__())

    @staticmethod
    def split_audio_file_to_mono_files(file_to_split: Path, destination_folder: Path):
        audio_to_split = AudioSegment.from_file(file_to_split.__str__())
        file_paths = []
        for index, channel in enumerate(audio_to_split.split_to_mono()):
            original_file_name = file_to_split.stem
            file_type = file_to_split.suffix
            save_mono_as_file = (
                destination_folder / f"{original_file_name}_chn{index}{file_type}"
            )
            AudioUtils.__save_audio(channel, save_mono_as_file)
            file_paths.append(save_mono_as_file)
        return file_paths


class AudioSource:
    def __init__(self, filename=None):
        self.audio_channel__service_person = None
        self.audio_channel__business_client = None

        if filename is not None:
            self.filename = Path(filename)
        else:
            self.filename = ""

        self.directory = Path("audio_processed")

        if filename is not None:
            self.separate_speakers_in_stereo_file()

    def separate_speakers_in_stereo_file(self, filename=None):
        if filename is not None:
            self.filename = filename

        audio_files = AudioUtils.split_audio_file_to_mono_files(
            self.filename, self.directory
        )

        print("Audio Files: ", audio_files[0], audio_files[1])

        self.audio_channel__service_person = audio_files[0]
        self.audio_channel__business_client = audio_files[1]
