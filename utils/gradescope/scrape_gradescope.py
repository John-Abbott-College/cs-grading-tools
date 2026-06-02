#!/usr/bin/env python

import argparse
import json
import sys
import zipfile
from datetime import datetime as dt
from pathlib import Path
from urllib.parse import urljoin

from fzf import fzf_input
from gradescope import *  # noqa: F403


def version_to_tuple():
    """Converts sys.version to form (major, minor, patch)"""
    return tuple(int(s) for s in sys.version.split(" ")[0].split("."))


def main():
    kwargs = {"suggest_on_error": True} if version_to_tuple() >= (3, 14, 0) else {}
    parser = argparse.ArgumentParser(
        description=("Download student submissions from Gradescope."), **kwargs
    )

    parser.add_argument(
        "-t",
        "--target",
        choices=["submissions", "grades"],
        required=True,
        help=("Choose what type of data to scrape."),
    )
    parser.add_argument(
        "-d",
        "--deadline",
        action="store_true",
        help=(
            "Optional: get last submission submitted before deadline (default: last submission regardless of deadline)"
        ),
    )
    parser.add_argument(
        "-c",
        "--course_name",
        type=str,
        help=(
            "Optional course name to select. If omitted or there is no match, fzf will prompt."
        ),
    )
    parser.add_argument(
        "-a",
        "--assignment_name",
        type=str,
        help=(
            "Optional assignment name to select. If omitted or there is no match, fzf will prompt."
        ),
    )

    args = parser.parse_args()

    with open("./login.key", "r") as f:
        login_info = json.load(f)

    gs = Gradescope(  # noqa: F405
        login_info["username"],
        login_info["password"],
        url="https://www.gradescope.ca",
        verbose=True,
    )

    courses = gs.get_courses(role=Role.INSTRUCTOR)  # noqa: F405
    course = next((c for c in courses if c.short_name == args.course_name), None)
    if course is None:
        args.course_name = fzf_input(
            'fzf --no-multi --header="select course name"',
            print,
            *(c.short_name for c in courses),
            **{"sep": "\n"},
        )[0]
        course = next((c for c in courses if c.short_name == args.course_name), None)
    print(f"{course.short_name=}")

    assignments = gs.get_assignments(course)
    assignment = next((a for a in assignments if a.title == args.assignment_name), None)
    if assignment is None:
        args.assignment_name = fzf_input(
            'fzf --no-multi --header="select assignment name"',
            print,
            *(a.title for a in assignments),
            **{"sep": "\n"},
        )[0]
        assignment = next(
            (a for a in assignments if a.title == args.assignment_name), None
        )
    print(f"{assignment.title=}")

    assignment_dir = Path(assignment.title.replace(" ", "_"))
    assignment_dir.mkdir(exist_ok=True)
    members = gs.get_members(course)

    if args.target == "submissions":
        for member in members:
            submission_history = gs.get_past_submissions(course, assignment, member)
            submission_history = (
                submission_history if submission_history is not None else []
            )

            if args.deadline:
                submission_history = [
                    s
                    for s in submission_history
                    if dt.fromisoformat(s.created_at).timestamp()
                    <= dt.fromisoformat(assignment.due_date).timestamp()
                ]

            if submission_history:
                s = max(
                    submission_history, key=lambda x: dt.fromisoformat(x.created_at)
                )
                filename = Path(
                    f"{assignment_dir}/{member.full_name}_{member.sid}_{s.created_at}.zip".replace(
                        " ", "_"
                    )
                )

                print(f"Downloading: {member.full_name}, {s.created_at}")
                gs.download_file(str(filename), urljoin(gs.url, s.url + ".zip"))
                with zipfile.ZipFile(filename, "r") as zip_ref:
                    Path(filename.with_suffix("")).mkdir(exist_ok=True)
                    zip_ref.extractall(filename.with_suffix(""))
            else:
                print(f"No submissions to download for {member.full_name}.")

    elif args.target == "grades":
        df = gs.get_assignment_grades(assignment)[["SID", "Total Score"]]
        df["SID"] = df["SID"].astype("Int64")
        df["Comment"] = ["Feedback given on Gradescope"] * df.shape[0]
        filepath = Path(
            f"{assignment_dir}/{assignment.title.replace(' ', '_')}_grades.csv"
        )
        print(f"Downloading grades for {assignment.title} to {filepath}.")
        save_csv(str(filepath), df, sep="\t")  # noqa: F405


if __name__ == "__main__":
    main()
