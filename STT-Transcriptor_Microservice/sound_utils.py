from pydub import AudioSegment
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
