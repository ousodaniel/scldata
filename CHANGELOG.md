# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
---

## [Release] - YYYY-MM-DD
### Added
- FASTA output feature
- Help with no options provided
- Variations for the target logging: long-and-abbr, abbr, and long
- File output-saving param
- Option to display summary data structure

### Changed
- Project structure: moved package into src
- Refactored the development data partition naming from evaluation (evl/eval) to validation (vld/valid)

### Deprecated

### Removed
- Default dumping of the full dataset when CLI is run without any options

### Fixed
- Data fold range in the README from 0 -> 5 to 0 -> 4 and other small updates

### Security

---

## [2025.6.0] - 2025-07-10
### Added
- Installation instructions and example usage to the README
- Updated this CHANGELOG

### Changed

### Deprecated

### Removed

### Fixed
- [Issue #1](https://github.com/ousodaniel/scldata/issues/1)

### Security

---

## [2025.6a2] - 2025-06-20

### Added

- This CHANGELOG file to capture the major evolution of this project as a standardised open-source project CHANGELOG.

### Changed

### Deprecated

- 2025.6a1; bug in version-parse rendered it unusable.
    
### Removed

### Fixed

- Update metadata `__version__` string in `__init__.py`, which is dynamically parsed by `importlib.metadata.version`; was breaking the whole package.

### Security

## [Unreleased] - YYYY-MM-DD

---

## Block template

## [Release] - YYYY-MM-DD
### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security
