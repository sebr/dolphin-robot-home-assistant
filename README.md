<!-- markdownlint-disable no-inline-html -->
# dolphin-robot-home-assistant

Maytronics Dolphin pool robot component for [Home Assistant](https://www.home-assistant.io/), for robots that use the MyDolphin Plus app.

This is a fork of [sh00t2kill/dolphin-robot](https://github.com/sh00t2kill/dolphin-robot), the integration in the default HACS store. It adds fixes and features that haven't reached upstream yet. To use it, add this repository to HACS as a custom repository (see [Installation](#installation)).

<!-- If this integration has been useful to you, please consider chipping in and buying me a coffee! -->

<a href="https://www.buymeacoffee.com/sebr" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee"></a>

## Supported Devices

This integration works with Dolphin robots that:

- use the [MyDolphin Plus app](https://www.maytronics.com/), and
- connect to the cloud through the power supply's Wi-Fi ("Always Connected").

It talks to the same Maytronics cloud as the app, so it needs a MyDolphin Plus account with the robot already paired.

The following robots have been tested with this fork. As an unofficial project that Maytronics doesn't support, it can't promise to keep working with current or future robots.

- Dolphin Premium 2000 (robot type S4)

M700 robots also get a water temperature sensor.

## Supported Entities

Home Assistant creates two devices: the **robot**, and its **power supply**, which holds the Wi-Fi and cloud connection.

- `vacuum` to start, pause and pick up the robot, and to choose its clean mode.
- `number` for the current clean's cycle time and the LED brightness.
- `sensor` for status, clean mode, cycle time left, filter bag, cycle count, errors, Wi-Fi signal and network name, and water temperature on M700 robots.
- `binary_sensor` for the cloud connection and the power supply connection.
- `button` to reset the filter bag indicator.
- `light` and `select` to turn the robot's LED on and off and choose its mode.
- `remote` to drive the robot by hand.

## Installation

Install through the [Home Assistant Community Store (HACS)](https://hacs.xyz/). [![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/docs/faq/custom_repositories/)

### 1. Install via HACS

This fork isn't in the default HACS store, so add it as a custom repository first. If you don't use HACS, download the latest version from the [releases page](https://github.com/sebr/dolphin-robot-home-assistant/releases), copy `custom_components/mydolphin_plus` into your Home Assistant `config/custom_components` folder, and go to step 2.

1. Open HACS.
2. Open the menu (⋮) in the top right and choose **Custom repositories**.
3. Enter `https://github.com/sebr/dolphin-robot-home-assistant`, choose the **Integration** type, and click **Add**.
4. Search for `MyDolphin Plus` and download it.
5. Restart Home Assistant.

The fork and upstream share the `mydolphin_plus` domain, so only one can be installed. If you have the upstream version, remove it in HACS before you download this one. Your MyDolphin Plus entry carries over.

### 2. Configure via Home Assistant

1. Go to **Settings > Devices & Services**.
2. Click **+ Add Integration**.
3. Search for `MyDolphin Plus`.
4. Enter the email address of your MyDolphin Plus account.
5. Maytronics emails you a one-time login code. Enter it in Home Assistant.

The integration then keeps itself logged in. You only need a new code if Maytronics ends the login, which can happen after about 30 days, or if you remove and re-add the integration. Home Assistant asks you to sign in again when that happens.

### Help

Common set-up mistakes:

- Installing the integration in HACS and stopping there. You still need to add it in **Devices & Services**.
- Not restarting Home Assistant after installing.
- Using an email that the MyDolphin Plus app doesn't know. Check that you can sign in to the app with it first.

## Vacuum Entity

The robot's **vacuum** entity starts and pauses a clean. **Return to base** runs Pickup, which brings the robot to the pool wall so you can lift it out.

### Clean Modes

The vacuum's fan speed is the clean mode. The list holds the modes your robot supports, as the MyDolphin Plus app shows them, plus Pickup. The integration reads them from Maytronics at startup. If it can't, it lists every mode.

| Mode     | App name      |
| -------- | ------------- |
| `all`    | Regular       |
| `short`  | Fast mode     |
| `floor`  | Floor only    |
| `water`  | Water line    |
| `ultra`  | Ultra clean   |
| `stairs` | Full coverage |
| `pickup` | Pickup        |

## Number Entities

### Cycle Time

A **cycle time** `number` entity shows how long the current clean runs, in minutes (1 to 600). Set it while the robot cleans to make the clean longer or shorter. The robot ignores it while idle, so Home Assistant shows an error instead.

When you start a clean from Home Assistant, the robot runs for its usual time for that mode, as set in the app.

### LED Intensity

An **LED intensity** `number` entity sets the brightness of the robot's LED, from 0 to 100%.

## Sensor Entities

### Status

A **status** `sensor` shows the overall state of the robot and power supply: Off, On, Checking Environment, Cleaning, Programming, Idle (Delay), Idle (Weekly) or Error. Its attributes hold the robot and power supply states it's based on.

### Robot Status and Power Supply Status

A **robot status** `sensor` and a **power supply status** `sensor` show what each part reports on its own.

### Clean Mode

A **clean mode** `sensor` shows the mode of the current or last clean.

### Cycle Time Left

A **cycle time left** `sensor` shows how long the current clean has left. Home Assistant shows it in hours and minutes, and you can choose another unit in the entity settings.

### Filter Status

A **filter status** `sensor` shows how full the filter bag is: Empty, Partially full, Getting full, Almost full or Full. Use the **Reset Filter Indicator** button once you've cleaned it.

### Cycle Count

A **cycle count** `sensor` counts the cleans the robot has run.

### Robot Error and Power Supply Error

A **robot error** `sensor` and a **power supply error** `sensor` show the error from the current clean, or OK. See [Error Event](#error-event) for the codes.

### Wi-Fi

The power supply has an **RSSI** `sensor` for Wi-Fi signal strength, and a **network name** `sensor` for the network it's on.

### Temperature

M700 robots get a **temperature** `sensor` for the water temperature, in °C.

## Binary Sensor Entities

### AWS Broker

An **AWS broker** `binary_sensor` turns on while Home Assistant is connected to the Maytronics cloud.

### Power Supply Connection

A **power supply connection** `binary_sensor` turns on while the power supply is online.

## Button Entities

### Reset Filter Indicator

A **reset filter indicator** `button` clears the filter bag indicator after you clean the filter. The Filter Status sensor updates when the robot next reports.

## Light and Select Entities

### LED

An **LED** `light` turns the robot's LED on and off, and an **LED mode** `select` chooses its pattern: Blinking, Always on or Disco.

## Remote Entities

### Manual Drive

A **remote** entity drives the robot by hand. Turn it on to start manual mode, choose an activity to move, and turn it off to leave manual mode.

Activities: `stop`, `forward`, `backward`, `left`, `right`.

```yaml
# Start manual mode and drive forward
service: remote.turn_on
target:
  entity_id: remote.{robot_name}
data:
  activity: forward

# Stop and leave manual mode
service: remote.turn_off
target:
  entity_id: remote.{robot_name}
```

## Error Event

The integration fires a `mydolphin_plus_error` event when the robot or power supply reports an error.

```json
{
  "name": "{Robot | Power Supply} Error",
  "Robot Name": "{Robot Name}",
  "state": 1,
  "Description": "{Robot | Power Supply} Error",
  "instructions": "steps to clear the fault, when known"
}
```

| Code | Description                   | Code | Description               |
| ---- | ----------------------------- | ---- | ------------------------- |
| 0    | OK                            | 13   | Wall/floor sensor 2       |
| 1    | DC in voltage                 | 14   | Robot stuck               |
| 2    | Out of water                  | 15   | Power supply overheat     |
| 3    | Impeller overload<sup>†</sup> | 16   | Power supply overload     |
| 4    | Impeller 1 underload          | 17   | Impeller 1 driver failure |
| 5    | Impeller overload<sup>†</sup> | 18   | Impeller 2 driver failure |
| 6    | Impeller 2 underload          | 19   | Drive 1 driver failure    |
| 7    | Drive overload<sup>†</sup>    | 20   | Drive 2 driver failure    |
| 8    | Drive 1 underload             | 21   | Servo overload            |
| 9    | Drive overload<sup>†</sup>    | 22   | Impeller 1 motor failure  |
| 10   | Drive 2 underload             | 23   | Impeller 2 motor failure  |
| 11   | Wall/floor sensor             | 24   | Drive 1 motor failure     |
| 12   | DC in voltage 23V             | 25   | Drive 2 motor failure     |
|      |                               | 255  | OK                        |

<sup>†</sup> The event's `instructions` field gives steps to clear the fault.

## Dashboard Card

The built-in tile card works well with the vacuum:

```yaml
type: tile
entity: vacuum.{robot_name}
show_entity_picture: true
features:
  - type: vacuum-commands
    commands:
      - start_pause
      - return_home
```

For a robot picture, copy the icons from [`www`](www) into your Home Assistant `config/www` folder.

## Troubleshooting

### Logs and diagnostics

Before opening an issue, turn on debug logs:

```yaml
logger:
  default: warning
  logs:
    custom_components.mydolphin_plus: debug
```

Then attach the logs and the integration's diagnostics: **Settings > Devices & Services > MyDolphin Plus > ⋮ > Download diagnostics**.

### Login code problems

- **No email arrives**: check spam, then try again. After several tries Maytronics may hold back codes for a few minutes.
- **"Invalid or expired login code"**: codes only last a short time. Start again to get a new one.
- **"Failed to send login code"**: Maytronics doesn't know the email. Check that you can sign in to the MyDolphin Plus app with it.

### Signed out

If Maytronics ends the login, Home Assistant asks you to sign in again with a new code. If it doesn't ask, or you can't finish, remove the integration and add it again.

Short internet or DNS outages don't sign you out. The integration reconnects once the network is back.

### Upgrading from 1.0.25b5 or older

Maytronics retired the old email and password login. After you update, Home Assistant asks you to sign in again with a login code. You don't need to reinstall.

## Contributors

Thanks to everyone who has worked on this integration, upstream and here:

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

See [Contributing](CONTRIBUTING.md) to help out. For every entity and attribute, see [docs/HA_ENTITIES.md](docs/HA_ENTITIES.md).
