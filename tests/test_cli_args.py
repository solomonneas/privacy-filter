import argparse
import io
import sys
import unittest
from unittest import mock

from opf.__main__ import build_redaction_parser
from opf._cli.args import iter_inputs


def _make_args(**overrides: object) -> argparse.Namespace:
    defaults: dict[str, object] = {
        "text": None,
        "text_file": None,
        "stdin_mode": "line",
        "interactive_banner": "",
        "interactive_prompt": "",
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


class IterInputsStdinTest(unittest.TestCase):
    def test_line_mode_yields_one_input_per_non_empty_line(self) -> None:
        stdin = io.StringIO("alpha\n\nbeta\n  \ngamma\n")
        args = _make_args(stdin_mode="line")
        with (
            mock.patch.object(sys, "stdin", stdin),
            mock.patch.object(sys.stdin, "isatty", return_value=False, create=True),
        ):
            self.assertEqual(list(iter_inputs(args)), ["alpha", "beta", "gamma"])

    def test_whole_mode_yields_full_stdin_as_one_input(self) -> None:
        payload = "first line\nsecond line\n\nthird line\n"
        stdin = io.StringIO(payload)
        args = _make_args(stdin_mode="whole")
        with (
            mock.patch.object(sys, "stdin", stdin),
            mock.patch.object(sys.stdin, "isatty", return_value=False, create=True),
        ):
            self.assertEqual(list(iter_inputs(args)), [payload])

    def test_whole_mode_yields_nothing_when_stdin_is_blank(self) -> None:
        stdin = io.StringIO("   \n\n")
        args = _make_args(stdin_mode="whole")
        with (
            mock.patch.object(sys, "stdin", stdin),
            mock.patch.object(sys.stdin, "isatty", return_value=False, create=True),
        ):
            self.assertEqual(list(iter_inputs(args)), [])

    def test_missing_stdin_mode_attr_defaults_to_line(self) -> None:
        stdin = io.StringIO("one\ntwo\n")
        args = argparse.Namespace(
            text=None,
            text_file=None,
            interactive_banner="",
            interactive_prompt="",
        )
        with (
            mock.patch.object(sys, "stdin", stdin),
            mock.patch.object(sys.stdin, "isatty", return_value=False, create=True),
        ):
            self.assertEqual(list(iter_inputs(args)), ["one", "two"])


class RedactionParserStdinModeTest(unittest.TestCase):
    def test_stdin_mode_defaults_to_line(self) -> None:
        args = build_redaction_parser().parse_args([])
        self.assertEqual(args.stdin_mode, "line")

    def test_stdin_mode_accepts_whole(self) -> None:
        args = build_redaction_parser().parse_args(["--stdin-mode", "whole"])
        self.assertEqual(args.stdin_mode, "whole")

    def test_stdin_mode_rejects_unknown_value(self) -> None:
        with self.assertRaises(SystemExit):
            build_redaction_parser().parse_args(["--stdin-mode", "jsonl"])


if __name__ == "__main__":
    unittest.main()
