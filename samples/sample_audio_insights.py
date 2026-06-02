"""
Audio Insights — a single-paragraph summary of an audio file.

`IntegratedApi` with `audio_insights=True` produces a high-level
scene description (environment, situation, keywords, notable events,
plus a speech-content summary when speech is present). One summary
object per file, no time chunks.

Two consumption patterns are shown below:

  1. `get_completed_result(job_id)` — blocking call that returns the
     final result dict. Recommended for most users.

  2. Manual SSE loop — subscribe to the stream and react to each
     `progress` / `partial_result` / `completed` / `error` event as
     it arrives. Use this when you need to render progress in a UI.

Project key: Cochl.Sense Dashboard → your project → Settings tab.
Docs: https://docs.cochl.ai/sense/cochl.sense-cloud-api/audioinsights/
"""
from cochl.sense import IntegratedApi, IntegratedApiOptions


def main():
    # 1. Authenticate with the project key.
    api = IntegratedApi(
        'YOUR_API_PROJECT_KEY',  # Replace with your project key.
    )

    # 2. To enable Audio Insights, both Sound Event Detection and Speech Analysis are required.
    options = IntegratedApiOptions(
        sound_event_detection=True,
        speech_analysis=True,
        audio_insights=True,
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
    #    For Audio Insights, the payload lives under result['audio_insights']['result'].
    result: dict = api.get_completed_result(job_id)
    print(result)

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
