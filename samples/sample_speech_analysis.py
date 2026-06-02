"""
Speech Analysis — transcribe speech and identify speakers.

`IntegratedApi` with `speech_analysis=True` returns one segment per
uninterrupted speaker turn. Each segment carries:
  - `speaker`         — diarization label (`SPEAKER_00`, `SPEAKER_01`, …)
  - `speaker_name`    — registered profile name when matched, else null
  - `speaker_score`   — similarity to the matched profile, else null
  - `transcript`      — the recognized text
  - `start_time_sec`, `end_time_sec` — segment boundaries (float)

To attach names to voices, register Speaker Profiles first with
`sample_speaker_profile_api.py`.

Two consumption patterns are shown below:

  1. `get_completed_result(job_id)` — blocking call that returns the
     final result dict. Recommended for most users.

  2. Manual SSE loop — subscribe to the stream and react to each
     `progress` / `partial_result` / `completed` / `error` event as
     it arrives. Use this when you need to render progress in a UI.

Project key: Cochl.Sense Dashboard → your project → Settings tab.
Docs: https://docs.cochl.ai/sense/cochl.sense-cloud-api/speechanalysis/
"""
from cochl.sense import IntegratedApi, IntegratedApiOptions


def main():
    # 1. Authenticate with the project key.
    api = IntegratedApi(
        'YOUR_API_PROJECT_KEY',  # Replace with your project key.
    )

    # 2. Enable only Speech Analysis for this run.
    options = IntegratedApiOptions(
        sound_event_detection=False,
        speech_analysis=True,
        audio_insights=False,
    )

    # 3. Upload the file. The server enqueues a job and returns its id.
    job: dict = api.analyze_file(
        'your_file.wav',  # Replace with your audio file path.
        options,
    )

    if 'job_id' not in job:
        print('ERROR: analyze_file did not return a job_id:', job)
        return

    job_id: str = job['job_id']

    # 4. Block until the job finishes and return the final result dict.
    #    Transcription segments live under result['speech_analysis']['results'].
    result: dict = api.get_completed_result(job_id)
    print(result)

    # Convenient per-segment readout:
    # for seg in result['speech_analysis']['results']:
    #     label = seg['speaker_name'] or seg['speaker']
    #     print(f"[{seg['start_time_sec']:.2f}–{seg['end_time_sec']:.2f}] "
    #           f"{label}: {seg['transcript']}")

    # ---------------------------------------------------------------
    # Alternative: stream progress events yourself.
    # Each SSE line is either:
    #     event: progress | partial_result | completed | error
    #     data:  <JSON payload>
    #
    # request: Request = api.create_event_stream_request(job_id)
    # with urlopen(request) as response:
    #     for line in response:
    #         line = line.decode('utf-8').strip()
    #         if line.startswith('event: ') or line.startswith('data: '):
    #             print(line)
    # ---------------------------------------------------------------


if __name__ == '__main__':
    main()
