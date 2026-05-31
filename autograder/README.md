# Gradescope Docker Image

## Overview

## Misc

### Running the autograder locally

To run your autograder image locally, you will currently need to bypass our autograder harness because otherwise it will try to communicate with Gradescope by default.
You can do this by mounting a sample submission into the /autograder/submission directory and then running /autograder/run_autograder directly.

Here's an example command; replace the path to the submission, results directory, and Docker image name with the appropriate values.

```
docker run --rm -v /path/to/submission:/autograder/submission -v /path/to/results:/autograder/results username/image_name:tag /autograder/run_autograder && cat /path/to/results/results.json
```

or to start an interactive session:

```
docker run --rm -it -v /path/to/submission:/autograder/submission -v /path/to/results:/autograder/results username/image_name:tag bash
```

Minor notes:

- `--rm` is added to clean up the container after it exits. You can remove it if you want to inspect container logs or state afterwards.
- The `/autograder/results` directory should be mounted to a path on your host so that you can inspect the `results.json` file that your autograder produces.

## Reference

- <https://gradescope-autograders.readthedocs.io/en/latest/manual_docker/>
- <https://docs.github.com/en/actions/tutorials/use-containerized-services/create-a-docker-container-action>
