import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from orso.tools import random_int
from orso.tools import random_string


def test_random():
    collected = [random_int() for i in range(1000000)]
    # allow some collisions - they're statistically likely here
    assert len(set(collected)) > (len(collected) * 0.999), len(set(collected))

    collected = [random_string() for i in range(1000000)]
    # allow one collisions, they're not impossible, but are unlikely
    assert len(set(collected)) == len(collected) - 1
    assert all(len(c) == 16 for c in collected)


if __name__ == "__main__":  # pragma: no cover
    test_random()

    print("✅ okay")
