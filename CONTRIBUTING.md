# Contributing

Thanks for helping improve MyDolphin Plus. Contributions are welcome as bug reports, documentation updates, translations, tests, and code changes.

## Before opening a pull request

- Check existing issues and pull requests to avoid duplicate work.
- Keep changes focused on one fix or feature at a time.
- Update `README.md`, `CHANGELOG.md`, or files in `docs/` when behavior or user-facing setup changes.
- For Home Assistant changes, follow the existing integration structure under `custom_components/mydolphin_plus/`.

## Development setup

The project uses [uv](https://docs.astral.sh/uv/) for Python 3.13 and its dependencies. A devcontainer (`.devcontainer.json`) sets everything up for VS Code; to work outside it, install uv and run `uv sync`.

| Command | What it does |
|---|---|
| `scripts/setup` | Installs system packages, uv and the dependencies (used by the devcontainer) |
| `scripts/develop` | Starts Home Assistant on port 8123 with the integration loaded and debug logging on |
| `scripts/lint` | Formats and lints with ruff, fixing what it can |
| `scripts/tests` | Runs the pytest suite |
| `scripts/version-bump` | Bumps the version in `manifest.json` |

Run `scripts/lint` and `scripts/tests` before opening a pull request; CI runs both, plus hassfest and HACS validation.

`.ruff.toml` turns on every ruff rule, then lists the ones the existing code still breaks. New code should pass them anyway. When you clean up a rule across the code, remove it from that list.

## Pull request guidelines

- Branch new development work from `develop` and open pull requests back into `develop`.
- Use `develop` for pre-release changes before they are promoted to a stable release.
- Explain the user-visible change and why it is needed.
- Include test details, even when the test is manual.
- Keep secrets, tokens, account emails, and robot identifiers out of issues, logs, and pull requests.
- Prefer small, reviewable pull requests over broad refactors.

## Creating a release

1. Run `scripts/version-bump` on `develop` and pick the bump. Versions look like `v1.0.26` for stable releases and `v1.0.26b3` for betas.
2. Commit and push the `manifest.json` change.
3. Run the **Release** workflow from the Actions tab, or `gh workflow run release.yml --ref <branch>`.

The workflow reads the version from `manifest.json`, fails if that tag exists, tags the commit, builds `mydolphin_plus.zip`, and publishes a GitHub release with generated notes. Versions ending in `aN`, `bN` or `rcN` are marked as prereleases.

## Contributors

Thanks to everyone who has contributed to this project:

- [Elad Bar](https://github.com/elad-bar)
- Dan Wheaton
- [sh00t2kill](https://github.com/sh00t2kill)
- [tigers75](https://github.com/tigers75)
- [Loïc](https://github.com/zoic21)
- Gil Peeters
- [devilismyfriend](https://github.com/devilismyfriend)
- [yumlevi](https://github.com/yumlevi)
- [grillp](https://github.com/grillp)
- [lordlala](https://github.com/lordlala)

If you contributed and are missing from this list, please open a pull request to add your name.
