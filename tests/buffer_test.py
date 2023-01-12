import unittest
from dataclasses import dataclass
from typing import List

from pyvpsq.buffer import Buffer


class BufferTest(unittest.TestCase):
    def test_read_c_string(self):
        @dataclass
        class ReadCStringTestCase:
            name: str
            data: bytes
            expected: str
            remaining: bytes

        tests: List[ReadCStringTestCase] = [
            ReadCStringTestCase(
                name='consumes string buffer',
                data=b'some-c-string\x00',
                expected='some-c-string',
                remaining=b'',
            ),
            ReadCStringTestCase(
                name='does not consume past terminating null byte',
                data=b'some-c-string\x00more-data',
                expected='some-c-string',
                remaining=b'more-data',
            ),
            ReadCStringTestCase(
                name='handles empty string',
                data=b'\x00',
                expected='',
                remaining=b'',
            ),
        ]

        for t in tests:
            # GIVEN
            buffer = Buffer(t.data)

            # WHEN
            actual = buffer.read_c_string()

            # THEN
            self.assertEqual(
                t.expected,
                actual,
                f'"{t.name}" failed\nexpected string: {t.expected}\nactual: {actual}'
            )
            self.assertEqual(
                t.remaining,
                buffer.get_buffer(),
                f'"{t.name}" failed\nexpected remaining bytes: {t.remaining}\nactual: {actual}'
            )

    def test_write_c_string(self):
        @dataclass
        class WriteCStringTestCase:
            name: str
            data: bytes
            value: str
            expected: bytes

        tests: List[WriteCStringTestCase] = [
            WriteCStringTestCase(
                name='writes string to empty buffer',
                data=b'',
                value='some-c-string',
                expected=b'some-c-string\x00',
            ),
            WriteCStringTestCase(
                name='appends string to buffer',
                data=b'other-c-string\x00',
                value='some-c-string',
                expected=b'other-c-string\x00some-c-string\x00',
            ),
            WriteCStringTestCase(
                name='writes empty string',
                data=b'',
                value='',
                expected=b'\x00',
            ),
        ]

        for t in tests:
            # GIVEN
            buffer = Buffer(t.data)

            # WHEN
            buffer.write_c_string(t.value)

            # THEN
            self.assertEqual(
                t.expected,
                buffer.get_buffer(),
                f'"{t.name}" failed\nexpected: {t.expected}\nactual: {buffer.get_buffer()}'
            )


if __name__ == '__main__':
    unittest.main()
