import pyaudio

import cochl.sense as sense

# (1) configure Stream behaviour
# PyAudio format and Cochl.Sense format must match
# For example, PyAudio `pa.Float32` means each sample is represented as float(4-bytes) in little endian.
PYAUDIO_FORMAT = pyaudio.paFloat32
SENSE_DATA_TYPE = sense.AudioDataType.F32
SENSE_ENDIAN = sense.AudioEndian.LITTLE

SAMPLE_RATE = 22050


def main():
    # (2) create Stream Client
    api_config = sense.APIConfig()
    audio_type = sense.StreamAudioType(
        data_type=SENSE_DATA_TYPE,
        endian=SENSE_ENDIAN,
        sample_rate=SAMPLE_RATE,
    )
    client = sense.StreamClient(
        "YOUR_API_PROJECT_KEY",
        audio_type=audio_type,
        api_config=api_config,
    )

    # (3) init PyAudio
    buffer = client.get_buffer()

    def pyaudio_callback(audio_data: bytes, _frame_count, _time_info, _status_flags):
        buffer.put(audio_data)
        return None, pyaudio.paContinue

    p = pyaudio.PyAudio()
    _pyaudio_stream = p.open(
        format=PYAUDIO_FORMAT,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=SAMPLE_RATE // 2,  # callback is triggered every half sample rate (0.5 second)
        stream_callback=pyaudio_callback,
    )

    # (4) retrieve one audio window from the buffer and predict
    print("Cochl.Sense Stream starts")
    while True:
        if buffer.is_ready():
            audio_window = buffer.pop()
            result = client.predict(audio_window)
            print(result)


if __name__ == "__main__":
    main()
