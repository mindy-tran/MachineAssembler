"""Unit tests for assembler phase 1"""

import unittest
from assembler_phase1 import *


class TestResolve(unittest.TestCase):

    def test_sample_resolve(self):
        lines = """
        # comment line at address 0

        # Blank line above is also address 0
        start:   # and start should also be address 0
        next:    ADD/P   r0,r1,r2[15]  # Still address 0
                 SUB     r1,r2,r3      # Address 1
        after:   MUL     r1,r2,r3[15]  # Address 2
        finally:  # Address 3
        fini:    DIV     r1,r2,r3      # Address 3
        """.split("\n")
        labels = resolve(lines)
        self.assertEqual(labels["start"], 0)
        self.assertEqual(labels["next"], 0)
        self.assertEqual(labels["after"], 2)
        self.assertEqual(labels["finally"], 3)
        self.assertEqual(labels["fini"], 3)

class TestParseMemop(unittest.TestCase):

    def test_parse_memop_unlabeled(self):
        line = "  LOAD/P  r3,something"
        fields = parse_line(line)
        self.assertEqual(fields["kind"], AsmSrcKind.MEMOP)
        self.assertEqual(fields["labelref"], "something")
        self.assertEqual(fields["opcode"], "LOAD")
        self.assertEqual(fields["label"], None)

    def test_parse_memop_labeled(self):
        line = "bogon:  STORE/Z r3,something # comments too"
        fields = parse_line(line)
        self.assertEqual(fields["kind"], AsmSrcKind.MEMOP)
        self.assertEqual(fields["labelref"], "something")
        self.assertEqual(fields["opcode"], "STORE")
        self.assertEqual(fields["label"], "bogon")


if __name__ == "__main__":
    unittest.main()