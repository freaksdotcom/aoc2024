#!/bin/env python3

from absl import app  # type: ignore
from absl import flags  # type: ignore
from typing import Any
from dataclasses import dataclass

import logging


logger: logging.Logger = logging.getLogger(__name__)

FLAGS: flags.FlagValues = flags.FLAGS

flags.DEFINE_string("input", "sample_01.txt", "Input File", short_name="i")
flags.DEFINE_bool("debug", False, "Print debug output", short_name="D")


@dataclass
class Report:
    levels: list[int]


def safe_delta(levels: list[int]) -> bool:
    idx = 1
    while idx < len(levels):
        delta = abs(levels[idx] - levels[idx - 1])
        if delta > 3 or delta < 1:
            logger.debug(f"Max difference {delta} is out of range")
            return False
        idx += 1
    return True


def correctly_sorted(levels: list[int], can_recurse: bool = True) -> bool:
    if can_recurse:
        logger.debug(f"{levels = }")

    fwd_lvls: list[int] = sorted(levels)
    rev_lvls: list[int] = sorted(levels, reverse=True)
    if fwd_lvls == levels:
        logger.debug(f"{levels} only increments")
        if safe_delta(levels):
            logger.debug(f"Safe: {levels}")
            return True

    elif rev_lvls == levels:
        logger.debug(f"{levels} only decrements")
        if safe_delta(levels):
            return True
    else:
        logger.debug(f"{levels} does not only increment or only decrement")

    for idx in range(len(levels)):
        remove_one = levels[:idx] + levels[idx + 1 :]
        if can_recurse and correctly_sorted(remove_one, can_recurse=False):
            return True

    return False


def main(_: Any) -> None:
    if FLAGS.debug:
        logger.setLevel(logging.DEBUG)

    reports: list[Report] = []
    with open(FLAGS.input) as input:
        for line in input:
            reports.append(Report([int(x) for x in line.split()]))

    safe_count = 0
    for r in reports:
        if correctly_sorted(r.levels):
            logger.debug(f"{r = } is safe\n")
            safe_count += 1
        else:
            logger.debug(f"{r = } is unsafe\n")

    print(f"{safe_count = }")


if __name__ == "__main__":
    app.run(main)
