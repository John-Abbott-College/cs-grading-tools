from pathlib import Path
import datetime as dt

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

with Path("config.toml").open(mode="rb") as f:
    CONFIG = tomllib.load(f)

PREFIX = CONFIG["options"]["root_directory"]
SOURCE_PREFIX = f"{PREFIX}/source"
SUBMISSION_PREFIX = f"{PREFIX}/submission"
PYTEST_RESULTS_JSON = f"{PREFIX}/results/pytest_results.json"
RESULTS_JSON = f"{PREFIX}/results/results.json"

RELEASE_DATE: dt.datetime = CONFIG["deadlines"]["release_date"]
DUE_DATE: dt.datetime = CONFIG["deadlines"]["due_date"]
FINAL_DUE_DATE: dt.datetime = CONFIG["deadlines"]["final_due_date"]
CURRENT_DATE: dt.datetime = dt.datetime.now()

SUBMISSION_FILES = CONFIG["options"]["submission_files"]

IS_GRAPHICAL = CONFIG["options"]["graphical"]
