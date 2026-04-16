import sys
import os
from pathlib import Path
from typing import Generator, Any

import pytest


@pytest.fixture
def importable_python_file(tmp_path) -> Generator[Path, Any, None]:
    """Create a temporary python file that can be imported.

    Reference
    - https://pytest-with-eric.com/pytest-best-practices/pytest-tmp-path/
    - https://learn.microsoft.com/en-us/training/modules/python-advanced-pytest/4-fixtures
    """
    sys.path.append(str(tmp_path))
    init_file_path: Path = tmp_path / "__init__.py"
    init_file_path.touch()
    tmp_file_path: Path = tmp_path / "testfile.py"
    yield tmp_file_path
    sys.path.remove(str(tmp_path))
    os.remove(tmp_file_path)
