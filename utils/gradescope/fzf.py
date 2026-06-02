# https://junegunn.github.io/fzf/tips/using-fzf-in-your-program/#python

import subprocess
import sys
import shutil


# fuzzy-select 1 or more results from output of work parameter
def fzf_input(command, work, *args, **kwargs):
    # Double check that the command is on the path before executing.
    command_bin = command.split(" ")[0]
    command_purpose = command.split('"')[1]
    print(f"Using {command_bin} to: {command_purpose}")
    if not shutil.which(command_bin):
        raise SystemExit(
            f"...{command_bin} not detected on system. Either install fzf, or {command_purpose} in advance. Exiting."
        )

    process = subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, shell=True
    )
    original_stdout = sys.stdout
    sys.stdout = process.stdin
    try:
        work(*args, **kwargs)
        process.stdin.close()
    except:  # noqa: E722
        pass
    finally:
        sys.stdout = original_stdout

    output = process.stdout.read().splitlines()
    process.stdout.close()
    return output
