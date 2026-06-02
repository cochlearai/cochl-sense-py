# cochl

`cochl` is the official Python client library for the **Cochl.Sense Cloud API**. Use it to detect sound events, transcribe and identify speakers, and summarize what's happening in an audio file, all from Python.

For end-user product documentation see [docs.cochl.ai](https://docs.cochl.ai/sense/cochl.sense-cloud-api/gettingstarted/).

## Installation

Supported on **Python 3.10+**.

```bash
pip install --upgrade cochl
```

## What's in the library

The library exposes three API classes; pick the one that matches your task.

| Class | Use for | Auth key |
|---|---|---|
| `IntegratedApi` | All-in-one analysis: Sound Event Detection + Speech Analysis + Audio Insights in one request. Recommended for new integrations. | Project key (`X-Api-Key`) |
| `Client` *(also exported as `EventDetectionApi`)* | Legacy single-feature client — Sound Event Detection only, with `tags[]` / `probability` shape. Kept for v1.x compatibility. | Project key (`X-Api-Key`) |
| `SpeakerProfileApi` | Register / list / recognize / delete voice profiles used by Speech Analysis. | Organization key (`X-Org-Key`) |

**Project keys** are per-project (Dashboard → Projects → *your project* → **Settings**). **Organization keys** apply across the whole organization (Dashboard → **Organization**).

Project keys do not expire — rotate them by regenerating from the project's **Settings** tab.

## Samples

Working scripts for each API class live under `samples/`. Replace the placeholder key and audio file path, then run with `python samples/<file>.py`.

```
samples/
├── sample_audio_insights.py        # IntegratedApi — audio_insights=True
├── sample_sound_event_detection.py # IntegratedApi — sound_event_detection=True
├── sample_speech_analysis.py       # IntegratedApi — speech_analysis=True
├── sample_speaker_profile_api.py   # SpeakerProfileApi — register / list / recognize / delete
└── legacy/
    ├── sample.py                   # Legacy Client (v1.x response shape)
    └── config.json                 # Sensitivity / result_summary / tag_filter knobs for Client
```

## Quick start — `IntegratedApi`

```python
from cochl.sense import IntegratedApi, IntegratedApiOptions

api = IntegratedApi('YOUR_API_PROJECT_KEY')

job = api.analyze_file(
    'your_file.wav',
    IntegratedApiOptions(
        sound_event_detection=True,
        speech_analysis=True,
        audio_insights=True,
    ),
)

# Block until the job finishes, then return the final result dict.
result = api.get_completed_result(job['job_id'])
print(result)
```

`result` is a dict with up to four top-level keys (one per enabled analysis):

- `sense.results[]` — Sound Event Detection chunks (~1 s windows) with `classes[]` (each `{class, confidence}`) and time fields.
- `speech_analysis.results[]` — speaker-turn segments with `speaker`, `speaker_name` (when matched against a registered Speaker Profile), `transcript`, and time fields.
- `audio_insights.result` — single object with `contains_speech`, `detected_language`, `primary_sound_environment`, `situation_summary`, `notable_events[]`, `speech_content_summary`, `keywords[]`.
- `usage` — `audio_duration_sec`, `services_used[]`, `processing_time_ms`.

A single upload is capped at 1 hour of audio.

For schema details and per-feature documentation, see:
- [Audio Insights](https://docs.cochl.ai/sense/cochl.sense-cloud-api/audioinsights/)
- [Speech Analysis](https://docs.cochl.ai/sense/cochl.sense-cloud-api/speechanalysis/)
- [Sound Event Detection](https://docs.cochl.ai/sense/cochl.sense-cloud-api/soundeventdetection/)

`IntegratedApi` accepts **MP3, WAV, FLAC, OGG**. Convert other formats first — see [Convert to supported file formats](#convert-to-supported-file-formats) below.

### Valid service combinations

`audio_insights` is a summary built on top of the other two analyses, so it can't run on its own — enable it only together with both `sound_event_detection` and `speech_analysis`. At least one service must be enabled. Invalid combinations come back as `400`.

| `sound_event_detection` | `speech_analysis` | `audio_insights` | Result |
|:---:|:---:|:---:|:---|
| ✅ | ❌ | ❌ | OK — SED only |
| ❌ | ✅ | ❌ | OK — Speech Analysis only |
| ✅ | ✅ | ❌ | OK — SED + Speech Analysis |
| ✅ | ✅ | ✅ | OK — full stack (Dashboard default) |
| ❌ | ❌ | ❌ | `400` — no services selected |
| ❌ | ❌ | ✅ | `400` — `audio_insights` requires both SED and Speech Analysis |
| ✅ | ❌ | ✅ | `400` — `audio_insights` requires `speech_analysis` |
| ❌ | ✅ | ✅ | `400` — `audio_insights` requires `sound_event_detection` |

## Speaker Profiles

Register voices ahead of time so `IntegratedApi`'s Speech Analysis can name them (instead of generic `SPEAKER_00` / `SPEAKER_01`).

```python
from cochl.sense import SpeakerProfileApi

api = SpeakerProfileApi('YOUR_ORGANIZATION_KEY')

# Register a profile from an audio sample.
api.add_new_voice('Anna_Kim', 'anna_sample.wav')

# List every profile registered under this organization.
print(api.list_all_speakers())

# Match speakers in a separate file (uses the registered profiles).
print(api.recognize('meeting.wav'))

# Delete a profile.
api.remove('Anna_Kim')
```

Notes:
- Each `add_new_voice` / `recognize` upload is capped at **10 MB** per file.
- `SpeakerProfileApi` uses the **organization key** (`X-Org-Key`), not a project key.

See [Custom Sound: Speaker Profile](https://docs.cochl.ai/sense/cochl.sense-cloud-api/speechanalysis/customspeakerprofile/) for the full registration flow.

## Other notes

### Convert to supported file formats

`Pydub` is one easy way to convert audio into a supported format. Install it per the [Pydub installation guide](https://github.com/jiaaro/pydub?tab=readme-ov-file#installation), then:

```python
from pydub import AudioSegment

audio = AudioSegment.from_file('sample.mp4', 'mp4')
audio.export('sample.mp3', format='mp3')
```

For more on Pydub, see the [Pydub repo](https://github.com/jiaaro/pydub).

### Repo layout

This package is published to PyPI from a private development repository (`cochl-sense-py-private`) and mirrored to the public [`cochlearai/cochl-sense-py`](https://github.com/cochlearai/cochl-sense-py) repo for end-user access. Issues and pull requests should be filed against the public mirror.

### Links

- Product documentation: [docs.cochl.ai](https://docs.cochl.ai)
- Public source mirror: [github.com/cochlearai/cochl-sense-py](https://github.com/cochlearai/cochl-sense-py)
- Issues: [github.com/cochlearai/cochl-sense-py/issues](https://github.com/cochlearai/cochl-sense-py/issues)
