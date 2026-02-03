# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v0.1.0.html).

## [Unreleased]

## [0.1.1] - 2026-02-04

### Added
- **Enhanced README**: Complete restructure with scenario-based approach
  - Added 3 typical usage scenarios
  - Deep dive into pain points and solutions
  - Design philosophy with 4 detailed trade-off analyses
  - ROI calculation with 3 user scenarios
  - Comprehensive industry comparison (vs planning-with-files, beads, Obsidian, Jira)
- **GitHub Actions CI/CD**: Complete automated workflow
  - CI pipeline: lint, test (Python 3.9-3.13), build, integration tests
  - Release automation: auto-create GitHub releases and PyPI publishing
  - Code coverage integration with Codecov
- **Repository metadata**: Added 15 GitHub topics for better discoverability
- **CI status badge**: Added to README for real-time build status

### Changed
- README structure reorganized for better storytelling
  - From feature-focused → scenario-driven approach
  - Added decision tree for tool selection
  - Enhanced quick start guide with realistic examples
  - Improved technical implementation details
- Updated test coverage badge (58% → 57.7%)

### Fixed
- README encoding issue ("工区" → "工作区")
- CI workflow improved error handling

### Documentation
- README expanded from 548 to 1051 lines (+915/-340)
- Added deep trade-off analysis for design decisions
- Added ROI calculations with concrete numbers
- Added tool comparison matrix

## [0.1.0] - 2026-02-03

### Added
- **Dual-format parser**: Auto-detect and parse v1 (legacy) and v2 (new) context.md formats
- **Smart migration**: `ctx migrate` command to upgrade legacy format to fused format
- **Session tracking**: Automatic session count and Git branch tracking
- **Status management**: Project status classification (active/paused/completed)
- **Project categories**: Enhanced categorization (探索性/产品/临时/学习)
- **Enhanced template**: Fused template combining v1 and v2 format advantages
- **Field updates**: Support for updating 8 key fields via `ctx update` command
- **Shell integration**: Improved `go` command and tab completion
- **Auto-increment**: Session count automatically increases on updates
- **Complete documentation**: SKILL.md, MIGRATION.md, and comprehensive guides

### Changed
- **Parser architecture**: Unified parser supporting multiple format versions
- **Template structure**: Reorganized with clear sections and comments
- **Status display**: Enhanced to show session count and branch information
- **Error handling**: Improved error messages and validation

### Fixed
- Duplicate field values during migration
- Incorrect field replacement in update command
- Missing session count tracking

### Deprecated
- Old v1 format (still supported via migration)

### Removed
- None (all legacy formats remain compatible)

### Security
- None

## [1.0.0] - 2025-01-XX

### Added
- Initial context tracking functionality
- Basic project listing
- Context display with ASCII art
- Session count tracking
- Git branch tracking
- Shell integration

[Unreleased]: https://github.com/your-username/context-manager/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-username/context-manager/compare/v1.0.0...v0.1.0
[1.0.0]: https://github.com/your-username/context-manager/releases/tag/v1.0.0
