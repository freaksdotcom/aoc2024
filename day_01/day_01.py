#!/bin/env python3

from absl import app  # type: ignore
from absl import flags  # type: ignore
from typing import Any

FLAGS = flags.FLAGS

flags.DEFINE_string("input", None, "Input File", short_name="i")


def main(_: Any):
    list_one: list[int] = []
    list_two: list[int] = []
    with open(FLAGS.input) as input:
        for line in input:
            v_one, v_two = line.split()
            list_one.append(int(v_one))
            list_two.append(int(v_two))
    list_one.sort()
    list_two.sort()
    print(f"{list_one=}")
    print(f"{list_two=}")

    answer = 0
    for diffs in zip(list_one, list_two):
        answer += abs(diffs[0] - diffs[1])
        print(f"{abs(diffs[0] - diffs[1])=}")

    print(f"{answer = }")


if __name__ == "__main__":
    app.run(main)
