import cochl.sense as sense
from cochl.sense import Result


def main():
    # Load API configuration from JSON file
    api_config = sense.APIConfigFromJson('./config.json')

    # Initialize the Cochl.Sense client with your project key and configuration
    client = sense.Client(
        'YOUR_API_PROJECT_KEY',  # Replace with your actual API project key
        api_config=api_config,
    )

    # Run inference on an example audio file (gunshot sample)
    result: Result = client.predict('sample_gunshot.wav')

    # Print the detailed detection results as a dictionary
    print(result.events.to_dict(api_config))


if __name__ == "__main__":
    # Entry point of the script
    main()

# -----------------------------
# Example only (not executed):
#
# Retrieve a list of official sound tags supported by Cochl.Sense
# tags: list = client.get_official_tags()
# for t in tags:
#     print(t.id)    # Print the tag ID
#     print(t.name)  # Print the tag name
#
# Print the summarized results (simplified format for easier use)
# print(result.events_summarized(api_config))
# -----------------------------
