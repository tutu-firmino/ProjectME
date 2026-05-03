from time import perf_counter

try:
    import pytest
except ImportError:
    raise SystemExit("pytest is not installed. Run: python -m pip install -e .[dev]")


class TestSummary:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_terminal_summary(self, terminalreporter):
        stats = terminalreporter.stats
        self.passed = len(stats.get("passed", []))
        self.failed = (
            len(stats.get("failed", []))
            + len(stats.get("error", []))
            + len(stats.get("xfailed", []))
        )


def main():
    summary = TestSummary()
    started = perf_counter()
    exit_code = pytest.main(["tests", "-q"], plugins=[summary])
    elapsed = perf_counter() - started

    print()
    print("Test summary")
    print(f"  Succeeded: {summary.passed}")
    print(f"  Failed:    {summary.failed}")
    print(f"  Time:      {elapsed:.2f}s")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
