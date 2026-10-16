"""Run every diffkit test module in one pass."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main() -> int:
    failed = []
    for t in sorted(HERE.glob("test_*.py")):
        print(f"== {t.name} ==")
        rc = subprocess.call([sys.executable, "-u", str(t)])
        if rc != 0:
            failed.append(t.name)
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        return 1
    print(f"all {len(list(HERE.glob('test_*.py')))} test modules passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
