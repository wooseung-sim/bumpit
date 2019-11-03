# bumpit
A small command line tool to bump tracked versions in your repository.

It is designed to integrate well with your CI/CD pipeline. Simply install and run `bumpit` as part of your pipeline. Let the robots do the boring work!

# Installation
You can download and install `bumpit` from PyPI by running:

```
pip install bumpit
```

# Usages

There are two ways to use `bumpit`
1. through the command line, or
2. through your python code

## Through CLI
At a high level, you need to
1. setup the configuration file `.bumpconfig.yaml` in your target folder.
2. run `bumpit` or use in the code

### Usage
```shell
Usage: bumpit [OPTIONS]

Options:
  -c, --config PATH  (optional) configuration settings. Defaults to
                     `.bumpit.yaml`
  -p, --part TEXT    (optional) strategy part override. Defaults to
                     `strategy.part` from the config file.
  -v, --value TEXT   (optional) part value override. Any part can be overrode
                     by this value as long as the value is valid.
  -d, --dry-run      (optional) run the tool in dry run mode. Defaults to
                     false.
  --help             Show this message and exit.
```

## Inside your program
Just do `from bumpit.core.bumpit import run` in your code.

Check out the [bumpit cli code](https://github.com/mobiusbyte/bumpit/blob/master/bumpit/console/cli.py#L29-L32) for concrete example.

## Configuration
`bumpit` relies heavily on a configuration file to capture runtime context of `bumpit`. This config file is named `.bumpconfig.yaml` by default. You can override this using the `--config` option in the command line.

The config file looks like:

```yaml
current_version: "201910.1.0"
strategy:
  name: "calver"
  part: "minor"
  version_format: "YYYYMM.MINOR.MICRO"
tag:
  apply: True
  format: "{version}"
auto_remote_push: True  # or False
tracked_files:
- setup.py
```

where:
* `current_version` - the current version of your files. It needs to be wrapped in quotes to force parsing to be string (e.g. avoid calver current_version to be parsed as float)
* `strategy` - strategy section
   * `name` - supported values: `semver`, `calver`
   * `part` - the target part to update when `bumpit` runs. Please refer to the description below for strategy specific values.
   * `version_format` - the format of the version. This only applies for `calver`
* `tag` - tag section
   * `apply` - bool value to instruct the tool to tag the repository after the version update
   * `format` - format of the tag. Some people prefer to add prefix to their tag versions (e.g. `release/1.0.1`). As long as the `{version}` is present, then it is a valid `tag_format`
* `auto_remote_push` - bool flag that guards whether to push commit and/or tag changes to remote repository. It should never be wrapped in quotes so that it will be properly parsed as a bool
* `tracked_files` - a list of relative filenames to update version to. If the current_version is not found, the tool simply skips this file

## Important Notes
* Collision of versions is handled outside of `bumpit`. Other tools such as a good version control system fits better in solving this problem.

# Examples
Check out the following repositories for examples:
* [CalVer](https://github.com/mobiusbyte/bumpit-calver-fixtures) example
* [SemVer](https://github.com/mobiusbyte/bumpit-semver-fixtures) example
* [bumpit](https://github.com/mobiusbyte/bumpit/blob/master/.bumpit.yaml) - yep! `bumpit` uses `bumpit`.

# Version Strategies
The tool currently supports the following versioning strategies
* [Semantic Version](https://semver.org/)
* [Calendar Version](https://calver.org/)

## Semantic Version
`bumpit` fully supports strict semver specification defined in [semver.org](https://semver.org/). It validates the right format using the [semver.org proposed format](https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string).

### Configuration
Here is an [example](https://github.com/mobiusbyte/bumpit/blob/master/tests/fixtures/config/.bumpit-semver.yaml) of a configuration file for semver.

Important notes on configuration:
* `strategy.name` must be `semver`
* `strategy.part` supported values are `major`, `minor`, `patch`
* `startegy.version_format` does not apply to `semver`. It is completely ignored in the code. It is safe (and better) to not include this section for `semver` use case to avoid confusing the user.

### Part updates
Any semver part can be updated by giving `bumpit` a specific value to update the part to. This can be done through:
 - command line by using the `--part and --value` cli options, or
 - program by providing the `target_part` and `force_value` in [bumpit#run](https://github.com/mobiusbyte/bumpit/blob/master/bumpit/core/bumpit.py) method

Due to the free form nature of the `pre_release` and `build_metadata` parts, they can only be updated through the force method described above.

However, the biggest gain from using `bumpit` is to let the tool auto update your versions for you.

Out of the box, `bumpit` can auto update the `major`, `minor`, and the `patch` parts of semver. To accomplish this, specify the target part in the config file `strategy.part` section.


## Calendar Version
`bumpit` implements a very basic calver scheme. It assumes that the version follows the format `YYYYmm.variant` where
* `YYYY` - year
* `mm` - month zero padded
* `variant` - incrementing integer to distinguish different version for the same month

When the month rolls over to the next, `YYYYmm` will be the new month, and `variant` resets to `1`.

The format is quite concrete. This was sufficient enough for my use case. However, if you feel that this is too simplistic, please feel free to create an issue and perhaps a PR of your proposed solution.


# Development
## Contribution
Code and documentation improvements are all welcome. You can also file bug reports or feature suggestions.

The feature set is meant to handle different versioning strategies. Currently, the strategies I know are applied in the wild are implemented, but it is by no means complete!

## Publishing
To publish `bumpit`, run the following

```shell
git checkout master
git pull
bumpit
python setup.py bdist_wheel sdist
twine upload dist/*
```


# License
`bumpit` is released under the [MIT License](https://opensource.org/licenses/MIT).

