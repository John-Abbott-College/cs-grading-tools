from pathlib import Path
import json
from typing import Iterator


def is_word_in_file(word: str, flines: Iterator[str]) -> bool:
    """Checks the lines of a file to see if the provided word is there

    :param word: Word to search for in file
    :param flines: File line iterator
    :return:
    """
    return len([line for line in flines if word.lower() in line.lower()]) > 0


def assert_word_in_file(word: str, file: str) -> None:
    """Assert passes if word is in file, fails otherwise

    :param word: Word to search for in file
    :param file: Filename
    """
    with Path(file).open("r") as f:
        flines = f.readlines()
    assert is_word_in_file(word, flines), f"Missing {word} in {file}"


def assert_any_word_in_file(words: list[str], file: str) -> None:
    """[TODO:description]

    :param words: [TODO:description]
    :param file: [TODO:description]
    """
    with Path(file).open("r") as f:
        flines = f.readlines()
    assert any(is_word_in_file(word, flines) for word in words), (
        f"Need one of {words} in {file}, missing."
    )


def assert_test_passed(test_file: str, test_name: str) -> None:
    """[TODO:description]

    :param test_file: [TODO:description]
    :param test_name: [TODO:description]
    """
    with Path(test_file).open("r") as f:
        test_data = [json.loads(line) for line in f]
    test_result = next(
        result
        for result in test_data
        if result.get("nodeid") == test_name and result.get("when") == "call"
    )
    failure_message = f"unit test '{test_name}' did not pass."
    if test_result.get("longrepr"):
        failure_message += (
            f"\n\n{test_result.get('longrepr').get('reprcrash').get('message')}"
        )
    assert test_result["outcome"] == "passed", failure_message
