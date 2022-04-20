from ytrss.configuration.configuration import Configuration


def rss_generate(configuration: Configuration) -> None:
    """
    Generate podcast file.
    """
    for destination in configuration.conf.destination_manager.destinations:
        print(f"Generate output: {destination.identity}")
        destination.generate_output()
