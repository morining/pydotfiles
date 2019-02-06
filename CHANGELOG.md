# Changelog | Pydotfiles

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
