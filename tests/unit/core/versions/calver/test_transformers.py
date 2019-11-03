from datetime import date

import pytest
from freezegun import freeze_time

from bumpit.core.versions.calver.parsers import parse
from bumpit.core.versions.calver.transformers import (
    CalverIncrementingTransformer,
    CalverStaticTransformer,
)


class TestIncrementingTransformer:
    def setup(self):
        self._version_format = "YYYY0M.MAJOR.MINOR.MICRO.MODIFIER"
        self._raw_version = "201910.1.10.100.abc"
        self._transform = CalverIncrementingTransformer()

    @pytest.mark.parametrize(
        "part, expected_version",
        [
            pytest.param("major", "201910.2.0.0."),
            pytest.param("minor", "201910.1.11.0."),
            pytest.param("micro", "201910.1.10.101."),
        ],
    )
    def test_transform(self, part, expected_version):
        new_calver = self._transform(
            part, parse(self._version_format, self._raw_version)
        )
        assert expected_version == str(new_calver)

    def test_transform_auto_same_date_tokens_bumps_next_numerical_token(self):
        with freeze_time(date(2019, 10, 15)):
            new_calver = self._transform(
                "auto", parse(self._version_format, "201910.1.10.100.abc")
            )
            assert "201910.2.0.0." == str(new_calver)

    def test_transform_auto_new_date_tokens_clears_numerical_tokens(self):
        with freeze_time(date(2019, 12, 15)):
            new_calver = self._transform(
                "auto", parse(self._version_format, "201910.1.10.100.abc")
            )
            assert "201912.0.0.0." == str(new_calver)

    def test_transform_auto_no_changes(self):
        with freeze_time(date(2019, 12, 15)):
            with pytest.raises(ValueError):
                self._transform("auto", parse("YYYYMM", "201912"))

    def test_transform_auto_current_version_is_ahead_of_today(self):
        with freeze_time(date(2019, 12, 15)):
            with pytest.raises(ValueError):
                self._transform(
                    "auto", parse(self._version_format, "202010.1.10.100.abc")
                )

    def test_transform_invalid_part(self):
        with pytest.raises(ValueError):
            self._transform("modifier", parse(self._version_format, self._raw_version))


class TestStaticTransformer:
    def setup(self):
        self._version_format = "YYYY0M.MAJOR.MINOR.MICRO.MODIFIER"
        self._raw_version = "201910.1.10.100.abc"
        self._transform = CalverStaticTransformer()

    @pytest.mark.parametrize(
        "part, value, expected_version",
        [
            # pytest.param("date", date(2019, 12, 10), "201912.0.0.0."),
            # pytest.param("major", "9", "201910.9.0.0."),
            # pytest.param("minor", "19", "201910.1.19.0."),
            pytest.param("micro", "109", "201910.1.10.109."),
            # pytest.param("modifier", "def", "201910.1.10.100.def"),
        ],
    )
    def test_transform(self, part, value, expected_version):
        new_calver = self._transform(
            part, parse(self._version_format, self._raw_version), value
        )
        assert expected_version == str(new_calver)

    def test_transform_add_modifier(self):
        new_calver = self._transform(
            "modifier", parse(self._version_format, "201910.1.10.100."), "ghi"
        )
        assert "201910.1.10.100.ghi" == str(new_calver)

    def test_transform_invalid_part(self):
        with pytest.raises(ValueError):
            self._transform("dummy", parse(self._version_format, self._raw_version), 1)

    def test_transform_invalid_value_for_numerical_part(self):
        with pytest.raises(ValueError):
            self._transform(
                "major", parse(self._version_format, self._raw_version), "a"
            )

    @pytest.mark.parametrize("value", [9, 10])
    def test_transform_non_increasing_numerical_part(self, value):
        with pytest.raises(ValueError):
            self._transform(
                "minor", parse(self._version_format, self._raw_version), value
            )

    def test_transform_non_changing_date_part(self):
        version = parse(self._version_format, self._raw_version)
        value = version.calendar_date

        with pytest.raises(ValueError):
            self._transform("date", version, value)

    def test_transform_non_changing_non_numerical_part(self):
        part = "modifier"
        version = parse(self._version_format, self._raw_version)
        value = getattr(version, part)

        with pytest.raises(ValueError):
            self._transform(part, version, value)