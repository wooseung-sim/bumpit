import pytest

from bumpit.core.versions.calver import (
    CalverIncrementingTransformer,
    CalVer,
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
            part, CalVer.parse(self._version_format, self._raw_version)
        )
        assert expected_version == str(new_calver)

    def test_transform_invalid_part(self):
        with pytest.raises(ValueError):
            self._transform(
                "modifier", CalVer.parse(self._version_format, self._raw_version)
            )


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
            part, CalVer.parse(self._version_format, self._raw_version), value
        )
        assert expected_version == str(new_calver)

    def test_transform_add_modifier(self):
        new_calver = self._transform(
            "modifier", CalVer.parse(self._version_format, "201910.1.10.100."), "ghi"
        )
        assert "201910.1.10.100.ghi" == str(new_calver)

    def test_transform_invalid_part(self):
        with pytest.raises(ValueError):
            self._transform(
                "dummy", CalVer.parse(self._version_format, self._raw_version), 1
            )

    def test_transform_invalid_value_for_numerical_part(self):
        with pytest.raises(ValueError):
            self._transform(
                "major", CalVer.parse(self._version_format, self._raw_version), "a"
            )

    @pytest.mark.parametrize("value", [9, 10])
    def test_transform_non_increasing_numerical_part(self, value):
        with pytest.raises(ValueError):
            self._transform(
                "minor", CalVer.parse(self._version_format, self._raw_version), value
            )

    def test_transform_non_changing_date_part(self):
        version = CalVer.parse(self._version_format, self._raw_version)
        value = version.calendar_date

        with pytest.raises(ValueError):
            self._transform("date", version, value)

    def test_transform_non_changing_non_numerical_part(self):
        part = "modifier"
        version = CalVer.parse(self._version_format, self._raw_version)
        value = getattr(version, part)

        with pytest.raises(ValueError):
            self._transform(part, version, value)
