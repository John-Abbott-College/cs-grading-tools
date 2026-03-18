import pytest


@pytest.hookimpl(optionalhook=True)
def pytest_json_modifyreport(json_report):
    total = 0
    for test in json_report.get("tests"):
        test["name"] = test.get("nodeid").split("::")[1]
        test["max_score"] = 1
        test["score"] = 1 if test.get("outcome") == "passed" else 0
        test["status"] = test.get("outcome")
        test["output"] = (
            ""
            if test.get("outcome") == "passed"
            else test.get("call", {}).get("crash", {}).get("message")
        )
        del test["nodeid"]
        del test["lineno"]
        del test["outcome"]
        del test["teardown"]
        del test["setup"]
        total += test["score"]
    json_report["score"] = total
