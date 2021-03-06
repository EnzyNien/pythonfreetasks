import wave
import struct


class ChipAndDale():

    @property
    def process_data(self):
        if self.file_name is None:
            raise FileExistsError('file name error')
        if self.file_name.split('.')[-1] != 'wav':
            raise FileExistsError(
                'file extension error. extension must be "wav"')
        try:
            self.speed = int(self.speed)
            if self.speed not in range(1, 6):
                raise ValueError('speed must be in 1..5 range')
        except ValueError:
            raise ValueError('speed must be int type')
        else:
            source = wave.open(self.file_name, mode="rb")
            result = wave.open(f"result_{self.speed}.wav", mode="wb")
            try:
                result.setparams(source.getparams())

                frames_count = source.getnframes()
                frames = struct.unpack(
                    "<" + str(frames_count) + "h",
                    source.readframes(frames_count))
                frames = frames[::self.speed]
                newframes = struct.pack("<" + str(len(frames)) + "h", *frames)

                result.writeframes(newframes)
            except BaseException:
                raise TypeError('change file error')
            else:
                print('file is changed\ncompleted...')
            finally:
                source.close()
                result.close()

    def __init__(self, file_name=None, speed=1):
        self.file_name = file_name
        self.speed = speed
        self.process_data


file_name = input('file name (*.wav): ')
speed = input('file speed (1..5): ')
ChipAndDale(file_name=file_name, speed=speed)
