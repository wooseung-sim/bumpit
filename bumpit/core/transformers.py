from bumpit.core.versions.semver import SemVer


class IncrementingTransformer:
    INCREMENTING_FIELDS = ["major", "minor", "patch"]

    def __call__(self, part, version):
        if part not in IncrementingTransformer.INCREMENTING_FIELDS:
            raise ValueError(f"Cannot increment {part}.")

        transform_delegate = StaticTransformer()
        return transform_delegate(part, version, getattr(version, part) + 1)


class StaticTransformer:
    NUMERICAL_FIELDS = ["major", "minor", "patch"]
    NON_NUMERICAL_FIELDS = ["pre_release", "build_metadata"]

    def __call__(self, part, version, static):
        if part in StaticTransformer.NUMERICAL_FIELDS:
            return self._transform_numerical_part(part, version, static)
        elif part in StaticTransformer.NON_NUMERICAL_FIELDS:
            return self._transform_non_numerical_part(part, version, static)
        else:
            raise ValueError(f"Invalid part {part}")

    @staticmethod
    def _transform_numerical_part(part, version, static):
        try:
            value = int(static)
        except ValueError:
            raise ValueError(f"Expecting {part} to be an integer")

        if getattr(version, part) >= value:
            raise ValueError(f"Can only increase {part} part.")

        new_version = SemVer.parse("0.0.0")

        target_part_index = IncrementingTransformer.INCREMENTING_FIELDS.index(part)
        for current_index, current_part in enumerate(
            StaticTransformer.NUMERICAL_FIELDS
        ):
            version_part = getattr(version, current_part)
            if current_index == target_part_index:
                version_part = static

            if target_part_index < current_index:
                version_part = 0

            setattr(new_version, current_part, version_part)

        return new_version

    @staticmethod
    def _transform_non_numerical_part(part, version, static):
        new_version = SemVer.parse(str(version))
        if getattr(version, part) == static:
            raise ValueError("There is no version change.")

        setattr(new_version, part, static)

        if part == "pre_release":
            new_version.build_metadata = ""

        return new_version
