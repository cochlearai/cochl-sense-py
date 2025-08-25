from typing import Optional

import cochl.sense as sense
from cochl.sense import Result


def main():
    api_config = sense.APIConfig()

    api_config.speaker_recognition = False
    api_config.custom_sound = False

    client = sense.Client(
        'YOUR_API_PROJECT_KEY',
        api_config=api_config,
    )

    tags: list = client.get_official_tags()
    for t in tags:
        print(t.id)
        print(t.name)

    result: Result = client.predict('sample_gunshot.wav')

    print(result.events.to_dict())
    print(result.events.to_summarized_result())

    if api_config.speaker_recognition:
        print(result.speakers)

    if api_config.custom_sound:
        custom_sound = sense.CustomSound(
            'YOUR_ORGANIZATION_KEY',
            api_config=api_config,
        )

        cs_error: Optional[dict] = custom_sound.upload(
            custom_sound_tag='YOUR_CUSTOM_SOUND_TAG',
            zip_file_path='YOUR_ZIP_FILE_PATH'
        )

        if cs_error is None:
            print('successfully uploaded')
        else:
            print(cs_error)


if __name__ == "__main__":
    main()
