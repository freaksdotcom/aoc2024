#!/bin/env python3

from absl import app  # type: ignore
from absl import flags  # type: ignore
from typing import Any

from collections import defaultdict

FLAGS = flags.FLAGS

flags.DEFINE_string("input", None, "Input File", short_name="i")


def main(_: Any):
    list_one: list[int] = []
    list_two: list[int] = []

    l1_counts: defaultdict[int, int] = defaultdict(int)
    l2_counts: dict[int, int] = defaultdict(int)

    with open(FLAGS.input) as input:
        for line in input:
            v_one, v_two = line.split()
            i_one = int(v_one)
            i_two = int(v_two)
            list_one.append(i_one)
            list_two.append(i_two)
            l1_counts[i_one] += 1
            l2_counts[i_two] += 1

    sorted_one = sorted(list_one)
    sorted_two = sorted(list_two)
    print(f"{list_one=}")
    print(f"{list_two=}")

    answer = 0
    for diffs in zip(sorted_one, sorted_two):
        answer += abs(diffs[0] - diffs[1])
        print(f"{abs(diffs[0] - diffs[1])=}")

    print(f"{answer = }")

    pt2_answer = 0
    for k in l1_counts.keys():
        pt2_answer += l2_counts[k] * k

    print(f"{pt2_answer = }")


if __name__ == "__main__":
    app.run(main)
