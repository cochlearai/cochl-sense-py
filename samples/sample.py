import cochl.sense as sense
from cochl.sense import Result


def main():
    api_config = sense.APIConfig(
        speaker_recognition=True
    )

    client = sense.Client(
        'YOUR_API_PROJECT_KEY',
        api_config=api_config,
    )

    result: Result = client.predict('sample_male_speech.wav')

    print(result.events.to_dict())
    print(result.events.to_summarized_result())

    if api_config.speaker_recognition:
        print(result.speakers)


if __name__ == "__main__":
    main()
