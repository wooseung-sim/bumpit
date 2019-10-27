from difflib import unified_diff


class GoBump:
    def __init__(self, folder, logger, dry_run):
        self._folder = folder
        self._logger = logger
        self._dry_run = dry_run

    def bump(self, current_version, bumped_version, files):
        if self._dry_run:
            self._logger.info("Running in DRY-RUN mode...")

        for file in files:
            with open(file, "rb") as fh:
                before_bump = fh.read().decode("utf-8")

                after_bump = before_bump.replace(current_version, bumped_version)

            if before_bump == after_bump:
                self._logger.warn(
                    f"Could not find version {current_version} in file '{file}'. "
                    f"Skipping..."
                )
            else:
                self._logger.info(
                    "\n".join(
                        list(
                            unified_diff(
                                before_bump.splitlines(),
                                after_bump.splitlines(),
                                lineterm="",
                                fromfile="before: " + file,
                                tofile="after: " + file,
                            )
                        )
                    )
                )

                if self._dry_run:
                    self._logger.info(
                        f"Running DRY-RUN mode. Skipping changes to '{file}'..."
                    )
