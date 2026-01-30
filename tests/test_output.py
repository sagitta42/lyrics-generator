from lyrics_generator.output import OutputManager


def test_identifier():
    identifier = "test"

    output_manager = OutputManager(identifier)
    print(output_manager.output_id)
