"""
Sound Event Detection via the legacy `Client` (a.k.a. `EventDetectionApi`).

This is the v1.x client kept for backward compatibility — it returns the
original `events[].tags[].name` / `probability` shape and reads its
behavior knobs from `config.json` next to this file.

For new integrations that need Speech Analysis or Audio Insights as well,
prefer `sample_integrated_api.py`.

Project key: Cochl.Sense Dashboard → your project → Settings tab.
Docs: https://docs.cochl.ai/sense/cochl.sense-cloud-api/gettingstarted/
"""
from cochl.sense import APIConfigFromJson, Client, Result


def main():
    # Sensitivity / result-summary / tag-filter knobs come from this file.
    api_config = APIConfigFromJson('./config.json')

    client = Client(
        'YOUR_API_PROJECT_KEY',  # Replace with your project key from the Dashboard.
        api_config=api_config,
    )

    # Run inference on a local audio file. Supported formats: MP3, WAV, OGG.
    # For other formats, convert first (see README → Convert to supported file formats).
    result: Result = client.predict('your_file.wav')

    # Detailed result as a dict (one entry per inference window).
    print(result.events.to_dict(api_config))

    # Alternative — summarized form, one entry per merged detection event:
    # print(result.to_summarized_result(api_config))

    # Alternative — list of officially supported sound tags:
    # for tag in client.get_official_tags():
    #     print(tag.id, tag.name)


if __name__ == '__main__':
    main()
