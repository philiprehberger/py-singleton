# Changelog

## 0.4.0 (2026-06-15)

- Add `is_instantiated()` classmethod on `@singleton`-decorated classes — non-raising counterpart to `instance()` for branching without try/except
- Add package-card image to README

## 0.3.0 (2026-04-28)

- Add `instance()` classmethod on `@singleton`-decorated classes — returns the cached instance without constructing one, raises `RuntimeError` if not yet built

## 0.2.0 (2026-04-04)

- Add `clear_on_exit` decorator for context manager support on singletons

## 0.1.2 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility
- Add GitHub issue templates, dependabot config, and PR template

## 0.1.1 (2026-03-22)

- Standardize badge format in README
- Remove Requirements section from README
- Convert API table to standard two-column format
- Fix Development section commands
- Fix License section format

## 0.1.0 (2026-03-21)

- Initial release
- Thread-safe singleton decorator
- Multiton decorator (one instance per key)
- Reset support for testing
