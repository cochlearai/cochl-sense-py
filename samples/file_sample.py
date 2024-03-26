import cochl.sense as sense


def main():
    api_config = sense.APIConfig()
    client = sense.FileClient(
        "YOUR_API_PROJECT_KEY",
        api_config=api_config,
    )

    results = client.predict("sample_gunshot.wav")
    print(results.to_dict())
    print(results.to_summarized_result())


if __name__ == "__main__":
    main()
