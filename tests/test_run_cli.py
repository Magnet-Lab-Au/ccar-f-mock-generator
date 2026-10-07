"""Tests of the command line of the owner (src/run.py). No test makes a model call."""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import run  # noqa: E402


class TestArguments(unittest.TestCase):
    def test_the_options_can_come_before_the_action_and_the_target(self):
        import argparse
        captured = {}
        real = argparse.ArgumentParser.parse_intermixed_args

        def capture(self, args=None, namespace=None):
            ns = real(self, args, namespace)
            captured["ns"] = ns
            return ns
        with mock.patch.object(argparse.ArgumentParser, "parse_intermixed_args", capture), \
                mock.patch.object(run, "make_control", side_effect=run.Refused("stop")):
            run.main(["decide", "--mock", "1", "more_tries", "M1-S47", "--reason", "Small findings."])
        ns = captured["ns"]
        self.assertEqual((ns.command, ns.action, ns.target, ns.mock, ns.reason),
                         ("decide", "more_tries", "M1-S47", 1, "Small findings."))


if __name__ == "__main__":
    unittest.main()
