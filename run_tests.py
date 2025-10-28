import importlib
import inspect
import sys


TEST_MODULES = [
    "tests.test_tail_slip",
    "tests.test_flood_fill",
    "tests.test_food_logic",
    "tests.test_h2h",
    "tests.test_policy_eval",
]


def main() -> int:
    failures = 0
    for module_name in TEST_MODULES:
        module = importlib.import_module(module_name)
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if not name.startswith("test_"):
                continue
            try:
                func()
            except AssertionError as exc:
                failures += 1
                print(f"[FAIL] {module_name}.{name}: {exc}")
            except Exception as exc:
                failures += 1
                print(f"[ERROR] {module_name}.{name}: {exc}")
    if failures:
        print(f"{failures} tests failed.")
        return 1
    print("All tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

