#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from reia.crew import Reia
import usaddress


def parse_address(address: str):
    parsed, _ = usaddress.tag(address)

    return {
        "street": " ".join(
            filter(
                None,
                [
                    parsed.get("AddressNumber"),
                    parsed.get("StreetNamePreDirectional"),
                    parsed.get("StreetName"),
                    parsed.get("StreetNamePostType"),
                ],
            )
        ),
        "city": parsed.get("PlaceName"),
        "state": parsed.get("StateName"),
        "zip": parsed.get("ZipCode"),
    }

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """

    address = '10133 LOUETTA RD, HOUSTON, TX 77070'

    inputs = parse_address(address)

    # inputs = {
    #     'street': '10133 LOUETTA RD',
    #     'city': 'HOUSTON',
    #     'state': 'TX',
    #     'zip': '77070',
    # }

    try:
        result = Reia().crew().kickoff(inputs=inputs)

        structured = result.pydantic
        print(structured.model_dump_json(indent=2))

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        Reia().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Reia().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        Reia().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = Reia().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
