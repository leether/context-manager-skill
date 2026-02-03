# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v0.1.0.html).

## [Unreleased]

### Added
- Initial release preparation
- Open source project structure
- Comprehensive documentation

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
