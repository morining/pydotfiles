# Changelog | Pydotfiles

## [3.1.1](https://github.com/morining/pydotfiles/compare/v3.1.0...v3.1.1) (2019-07-08)


### Bug Fixes

* this is a fix message ([03b659f](https://github.com/morining/pydotfiles/commit/03b659f))

# [3.1.0](https://github.com/JasonYao/pydotfiles/compare/v3.0.0...v3.1.0) (2019-02-15)


### Features

* **developer environments:** Adds in the ability to install language runtimes and specified virtual ([15395b4](https://github.com/JasonYao/pydotfiles/commit/15395b4)), closes [#42](https://github.com/JasonYao/pydotfiles/issues/42) [#43](https://github.com/JasonYao/pydotfiles/issues/43) [#66](https://github.com/JasonYao/pydotfiles/issues/66) [#59](https://github.com/JasonYao/pydotfiles/issues/59)

# [3.0.0](https://github.com/JasonYao/pydotfiles/compare/v2.1.0...v3.0.0) (2019-02-09)


### Features

* **validation:** Formalizes the schema for default setting validation, and enables multiple-schema ([b1bde2d](https://github.com/JasonYao/pydotfiles/commit/b1bde2d)), closes [#57](https://github.com/JasonYao/pydotfiles/issues/57)


### BREAKING CHANGES

* **validation:** Requires a 'version' and 'schema' field for all core and referenced schemas. Valid
schema options currently include 'core' and 'default_settings'

# [2.1.0](https://github.com/JasonYao/pydotfiles/compare/v2.0.0...v2.1.0) (2019-02-06)


### Features

* **dock:** Adds in the ability to set the dock icons via config ([b55d99a](https://github.com/JasonYao/pydotfiles/commit/b55d99a)), closes [#52](https://github.com/JasonYao/pydotfiles/issues/52)

# [2.0.0](https://github.com/JasonYao/pydotfiles/compare/v1.2.0...v2.0.0) (2019-02-06)


### Bug Fixes

* **default-settings:** Fixes sudo command execution and grants the ability to ignore return code val ([f672b6f](https://github.com/JasonYao/pydotfiles/commit/f672b6f))


### BREAKING CHANGES

* **default-settings:** 'run_as_sudo' should instead be called 'sudo'. If you want to ignore return code
errors, please use ''check_output': false'

Fixes 54

# [1.2.0](https://github.com/JasonYao/pydotfiles/compare/v1.1.0...v1.2.0) (2019-02-06)


### Features

* **downloads:** Enables downloading a default set of basic dotfiles if one is not provided ([c0c8651](https://github.com/JasonYao/pydotfiles/commit/c0c8651)), closes [#17](https://github.com/JasonYao/pydotfiles/issues/17)

# [1.1.0](https://github.com/JasonYao/pydotfiles/compare/v1.0.0...v1.1.0) (2019-02-06)


### Features

* **defaults:** Adds in the ability to set default settings for a given OS ([ba7aebd](https://github.com/JasonYao/pydotfiles/commit/ba7aebd)), closes [#46](https://github.com/JasonYao/pydotfiles/issues/46)

# [1.0.0](https://github.com/JasonYao/pydotfiles/compare/v0.1.0...v1.0.0) (2019-02-06)


### Bug Fixes

* **ci/cd:** Fixes the broken test due to an out of date pytest dependency ([8bfea51](https://github.com/JasonYao/pydotfiles/commit/8bfea51)), closes [#50](https://github.com/JasonYao/pydotfiles/issues/50)


### Features

* **validator:** Adds in the ability to validate a given file or directory ([0acc0b9](https://github.com/JasonYao/pydotfiles/commit/0acc0b9)), closes [#9](https://github.com/JasonYao/pydotfiles/issues/9)


### BREAKING CHANGES

* **validator:** All settings.yaml/.json/.yml will now require a 'version' field, with the only
currently available version being 'alpha'

# [0.1.0](https://github.com/JasonYao/pydotfiles/compare/v0.0.5...v0.1.0) (2018-11-23)


### Features

* **ci/cd:** Adds in automatic artifact release for pypi and github (along with automatic semver) ([70bf842](https://github.com/JasonYao/pydotfiles/commit/70bf842)), closes [#3](https://github.com/JasonYao/pydotfiles/issues/3) [#5](https://github.com/JasonYao/pydotfiles/issues/5)
