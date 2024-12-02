#!/bin/env python3

from absl import app  # type: ignore
from absl import flags  # type: ignore
from typing import Any
from dataclasses import dataclass
from pprint import pp
import logging

logger = logging.getLogger(__name__)

FLAGS = flags.FLAGS

flags.DEFINE_string("input", "sample_01.txt", "Input File", short_name="i")


@dataclass
class Report:
    levels: list[int]

    def is_safe(self):
        increment = self.levels[0] < self.levels[1]
        safe = True
        for x in range(1, len(self.levels)):
            diff = self.levels[x] - self.levels[x - 1]
            if diff == 0:
                safe = False
                return safe
            if abs(diff) > 3:
                safe = False
                return safe
            if increment and diff < 0:
                safe = False
                return safe
            if not increment and diff > 0:
                safe = False
                return safe
        return safe


def main(_: Any):
    logger.setLevel(logging.DEBUG)

    reports: list[Report] = []
    with open(FLAGS.input) as input:
        for line in input:
            reports.append(Report([int(x) for x in line.split()]))

    pp(reports)

    safe_count = 0
    for r in reports:
        if r.is_safe():
            safe_count += 1
    print(f"{safe_count = }")


if __name__ == "__main__":
    app.run(main)
