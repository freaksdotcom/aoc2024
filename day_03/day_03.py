#!/bin/env python3

import logging
import re
from dataclasses import InitVar, dataclass, field
from typing import Any, TypeVar

from absl import app  # type: ignore
from absl import flags  # type: ignore

logger: logging.Logger = logging.getLogger(__name__)

FLAGS: flags.FlagValues = flags.FLAGS

flags.DEFINE_string("input", "sample_01.txt", "Input File", short_name="i")
flags.DEFINE_bool("debug", False, "Print debug output", short_name="D")

MUL_RE: re.Pattern[str] = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
DO_RE: re.Pattern[str] = re.compile(r"do\(\)")
DONT_RE: re.Pattern[str] = re.compile(r"don't\(\)")

OP_PATTERNS: dict[str, re.Pattern[str]] = {"MUL": MUL_RE, "DO": DO_RE, "DONT": DONT_RE}

OPCODE_RE: re.Pattern[str] = re.compile(
    "|".join(p.pattern for p in OP_PATTERNS.values())
)

T = TypeVar("T")

from enum import Enum, auto


class Op(Enum):
    MUL = auto()
    DO = auto()
    DONT = auto()


@dataclass
class OpCode:
    x: int | None = field(init=False, default=None)
    y: int | None = field(init=False, default=None)
    op: Op | None = field(init=False, default=None)
    input: InitVar[str]

    def exec(self) -> int | None:
        if self.op is Op.MUL:
            if self.x is None or self.y is None:
                raise ValueError
            return self.x * self.y

    def __post_init__(self, input: str) -> None:
        logger.debug(f"{input = }")
        if (m := MUL_RE.match(input)) is not None:
            logger.debug("Creating ")
            x: str
            y: str
            x, y = m.groups()
            self.x = int(x)
            self.y = int(y)
            self.op = Op.MUL
        elif m := DO_RE.match(input):
            self.op = Op.DO
        elif m := DONT_RE.match(input):
            self.op = Op.DONT
        else:
            raise ValueError


def main(_: Any) -> None:
    if FLAGS.debug:
        logger.setLevel(logging.DEBUG)

    opcodes: list[OpCode] = []
    with open(FLAGS.input) as input:
        for line in input:
            for code in OPCODE_RE.finditer(line):
                logger.debug(f"{code=}")
                logger.debug(f"{code[0]=}")
                opcodes.append(OpCode(code[0]))

    mul_sum = 0
    enabled = True
    for op in opcodes:
        logger.debug(f"{op = }, {enabled = }")
        if op.op is Op.DO:
            enabled = True
            continue
        if op.op is Op.DONT:
            enabled = False
            continue
        if not enabled:
            continue
        if op.op is Op.MUL:
            res = op.exec()
            if res:
                mul_sum += res

    print(f"Result = {mul_sum}")


if __name__ == "__main__":
    app.run(main)
