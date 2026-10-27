# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Setup**: `scripts/setup` - Install dependencies and set up development environment (devcontainer). Locally, `uv sync` is enough.
- **Lint**: `scripts/lint` - Format code with ruff and run linting checks
- **Test**: `scripts/tests` - Run pytest with verbose output
- **Development**: `scripts/develop` - Start Home Assistant in development mode with debug logging
- **Version bump**: `scripts/version-bump` - Bump the version in `manifest.json` before a release

## Repository Architecture

This is a Home Assistant custom integration for Maytronics Dolphin pool cleaners that use the MyDolphin Plus app. The domain is `mydolphin_plus`.

### Core Structure

- `custom_components/mydolphin_plus/` - Main integration code
  - `__init__.py` - Entry point; stores the login tokens from the config flow, builds the `ConfigManager` and `MyDolphinPlusCoordinator`
  - `config_flow.py` - UI setup flow (delegates to `managers/flow_manager.py`)
  - `diagnostics.py` - Diagnostics download
  - Platform files: `binary_sensor.py`, `light.py`, `number.py`, `remote.py`, `select.py`, `sensor.py`, `vacuum.py`
  - `services.yaml`, `strings.json`, `translations/` - Services and UI strings

### Managers

- `managers/rest_api.py` - `RestAPI`: logs in to the Maytronics cloud (email OTP), refreshes tokens, and fetches robot details and AWS credentials
- `managers/aws_client.py` - `AWSClient`: MQTT connection to AWS IoT for live robot state and commands (uses `managers/AmazonRootCA.pem`)
- `managers/coordinator.py` - `MyDolphinPlusCoordinator`: owns the API and AWS clients, maps their data onto entity descriptions
- `managers/config_manager.py` - Config entry data, options and stored tokens and serial numbers

### Common and Models

- `common/` - Constants (`consts.py`), entity descriptions, `integration_info.py` (name and version from the manifest), enums for robot, power supply, clean mode and joystick state
- `models/` - Data classes; `system_details.py` turns the raw AWS shadow into the vacuum and calculated states

### Docs

- `docs/Maytronics/` - How the integration talks to Maytronics: overview, OTP setup, startup, ongoing calls and events, error recovery, entity actions. Start at `00-overview.md` and read the relevant file before changing the coordinator, API or AWS client
- `docs/MQTT_DEBOUNCING.md` - How MQTT updates are debounced
- `docs/ha-compat-last-audit.md` - Last Home Assistant forward-compatibility check (see the `ha-integration-forward-compat` skill)
- `docs/HA_ENTITIES.md` - Entities the integration creates

### Development Environment

- Home Assistant 2026.1.0 (the minimum in `hacs.json`; keep the two in step), Python 3.13, managed by `uv`
- Configuration in `config/configuration.yaml` with debug logging enabled for the `mydolphin_plus` component
- Custom component loaded via PYTHONPATH in `scripts/develop`

### Branches and Releases

- Upstream is `sh00t2kill/dolphin-robot` (remote `upstream`). Work branches from `develop` and PRs go back to `develop`
- Versions in `manifest.json` look like `v1.0.26` or `v1.0.26b3`; `scripts/version-bump` and the Release workflow expect that form

### Testing

Tests live in `tests/` and use pytest with `pytest-homeassistant-custom-component`. Only `test_*.py` files run. `tests/api_test.py`, `tests/genereate_aws_token_test.py` and `tests/translation_compare.py` are manual scripts that need live credentials or extra packages; pytest and ruff skip them. `.ruff.toml` also relaxes rules for the test files that came from upstream.

### Code Standards

- ruff with the `ALL` rule set (target Python 3.13); run `scripts/lint` before committing
- `.ruff.toml` lists rules the inherited code still breaks under `per-file-ignores` for `custom_components/**`. New code should pass them anyway; remove a rule from that list once the code is clean
- Type hints on new code
- Follow Home Assistant integration patterns; see the `home-assistant-integration-knowledge` skill. Upstream keeps its own skills in `.cursor/skills/`; `.claude/skills/` links to them
