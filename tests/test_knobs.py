from unittest.mock import patch

from bomshell.knobs import get_bool
from bomshell.knobs import get_int
from bomshell.knobs import get_knob_defaults
from bomshell.knobs import get_string
from bomshell.knobs import register


class TestGetString:
    def test_returns_default(self):
        result = get_string("TEST_STRING_KNOB", "hello")
        assert result == "hello"

    def test_returns_env_value(self):
        with patch.dict("os.environ", {"TEST_STRING_ENV": "from_env"}):
            result = get_string("TEST_STRING_ENV", "default")
            assert result == "from_env"

    def test_registers_default(self):
        get_string("TEST_REG_STR", "mydefault")
        assert register["TEST_REG_STR"] == "mydefault"


class TestGetInt:
    def test_returns_default(self):
        result = get_int("TEST_INT_KNOB", 42)
        assert result == 42

    def test_returns_env_value(self):
        with patch.dict("os.environ", {"TEST_INT_ENV": "99"}):
            result = get_int("TEST_INT_ENV", 1)
            assert result == 99

    def test_registers_default(self):
        get_int("TEST_REG_INT", 7)
        assert register["TEST_REG_INT"] == 7


class TestGetBool:
    def test_returns_default(self):
        result = get_bool("TEST_BOOL_KNOB", False)
        assert result is False

    def test_returns_env_value(self):
        with patch.dict("os.environ", {"TEST_BOOL_ENV": "True"}):
            result = get_bool("TEST_BOOL_ENV", False)
            assert result

    def test_registers_default(self):
        get_bool("TEST_REG_BOOL", True)
        assert register["TEST_REG_BOOL"] is True


class TestGetKnobDefaults:
    def test_output_format(self):
        get_string("AAA_TEST", "val1")
        get_int("AAA_TEST_INT", 10)
        output = get_knob_defaults()
        assert "#AAA_TEST=val1" in output
        assert "#AAA_TEST_INT=10" in output

    def test_sorted_output(self):
        get_string("ZZZ_KNOB", "z")
        get_string("AAA_KNOB", "a")
        output = get_knob_defaults()
        lines = output.splitlines()
        knob_lines = [line for line in lines if "AAA_KNOB" in line or "ZZZ_KNOB" in line]
        assert knob_lines == sorted(knob_lines)
