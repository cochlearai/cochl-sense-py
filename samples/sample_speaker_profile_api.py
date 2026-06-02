"""
Manage Speaker Profiles via `SpeakerProfileApi`.

Speaker Profiles are voice fingerprints. Once registered, the matching
profile name appears in `speech_analysis.results[].speaker_name` when
you run Speech Analysis through `IntegratedApi` — without one, voices
fall back to generic diarization labels (`SPEAKER_00`, `SPEAKER_01`, …).

This script demonstrates four operations on the API. They are wrapped in
separate helpers so you can call only the ones you need from `main`.

Auth note: `SpeakerProfileApi` takes the **organization key**
(`X-Org-Key`), not a project key. Find it on the Dashboard's
**Organization** tab.

Upload size limit: 10 MB per file for `add_new_voice` and `recognize`.

Docs: https://docs.cochl.ai/sense/cochl.sense-cloud-api/speechanalysis/customspeakerprofile/
"""
from cochl.sense import SpeakerProfileApi


def register(api: SpeakerProfileApi, speaker_name: str, audio_file_path: str) -> None:
    """Register a new voice profile from an audio sample."""
    result: dict = api.add_new_voice(speaker_name, audio_file_path)
    print('add_new_voice:', result)


def list_speakers(api: SpeakerProfileApi) -> None:
    """List every profile registered under this organization."""
    result: dict = api.list_all_speakers()
    print('list_all_speakers:', result)


def recognize(api: SpeakerProfileApi, audio_file_path: str) -> None:
    """Match registered profiles against an audio file."""
    result: dict = api.recognize(audio_file_path)
    print('recognize:', result)


def delete(api: SpeakerProfileApi, speaker_name: str) -> None:
    """Delete a registered profile."""
    result: dict = api.remove(speaker_name)
    print('remove:', result)


def main():
    api = SpeakerProfileApi(
        'YOUR_ORGANIZATION_KEY',  # Dashboard → Organization tab.
    )

    # Typical flow: register a speaker, list profiles to confirm, recognize
    # speakers in a different audio file, optionally delete the profile
    # later. Uncomment whichever steps you want to run.

    # register(api, 'Anna_Kim', 'anna_sample.wav')
    list_speakers(api)
    # recognize(api, 'meeting.wav')
    # delete(api, 'Anna_Kim')


if __name__ == '__main__':
    main()
