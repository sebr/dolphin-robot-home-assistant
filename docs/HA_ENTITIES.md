# MyDolphin Plus - Home Assistant Entities

Every entity the MyDolphin Plus integration creates, what it shows and what it does.

## Overview

The integration creates **21 entities** across 8 platforms, or **22** on M700 robots, which also get a water temperature sensor.

Entity IDs start with the robot's name from the MyDolphin Plus app, shown here as `{robot_name}`. For a robot named Willy, the clean mode sensor is `sensor.willy_clean_mode`.

### Devices

The integration creates two devices:

- **{Robot Name} Power Supply** holds the Wi-Fi and cloud connection. It shows the power supply firmware, and has the Power Supply Status, Power Supply Error, RSSI, Network Name, AWS Broker and Power Supply Connection entities.
- **{Robot Name}** is the robot, connected through the power supply. It shows the product name (for example DOLPHIN PREMIUM 2000 AU) as its model, the part number as its model ID, the robot firmware, the robot type (for example S4) as its hardware, and the serial number. It has every other entity.

The product name and supported clean modes load from the Maytronics API at startup; the versions appear once the robot first reports its state.

Power supply entities keep entity IDs based on the robot's name, such as `sensor.{robot_name}_rssi`.

---

## 🤖 Vacuum Entity (1)

| Entity                                     | Type     | Functionality                                                                                                                                                                                                                                              |
| ------------------------------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [**{Robot Name}**](#vacuum-entity-details) | `vacuum` | Main robot control:<br/>• **Start** - Start a clean in the current mode<br/>• **Pause** - Stop the clean<br/>• **Return to Base** - Run Pickup<br/>• **Set Fan Speed** - Choose the clean mode<br/>• Shows the state: docked, cleaning, returning or error |

---

## 🎮 Remote Control Entity (1)

| Entity                                       | Type     | Functionality                                                                                                                                                     |
| -------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [**Remote**](#remote-control-entity-details) | `remote` | Drive the robot by hand:<br/>• **Turn On** / **Send Command** - Move in a direction (forward, backward, left, right, stop)<br/>• **Turn Off** - Leave manual mode |

---

## 💡 Light Entity (1)

| Entity                           | Type    | Functionality                                                 |
| -------------------------------- | ------- | ------------------------------------------------------------- |
| [**LED**](#light-entity-details) | `light` | Turn the robot's LED on and off<br/>• Category: Configuration |

---

## 🎚️ Select Entity (1)

| Entity                                 | Type     | Functionality                                                           |
| -------------------------------------- | -------- | ----------------------------------------------------------------------- |
| [**LED Mode**](#select-entity-details) | `select` | LED pattern: Blinking, Always on or Disco<br/>• Category: Configuration |

---

## 🔢 Number Entities (2)

| Entity                              | Type     | Range     | Functionality                                                                        |
| ----------------------------------- | -------- | --------- | ------------------------------------------------------------------------------------ |
| [**LED Intensity**](#led-intensity) | `number` | 0-100%    | LED brightness<br/>• Category: Configuration                                         |
| [**Cycle Time**](#cycle-time)       | `number` | 1-600 min | Length of the current clean<br/>• Change it while the robot cleans to set a new time |

---

## 📊 Sensor Entities (13)

12 on every robot, plus Temperature on M700 robots.

### Status & Diagnostic Sensors

| Entity                                          | Type     | Device       | Functionality                                                                                         |
| ----------------------------------------------- | -------- | ------------ | ----------------------------------------------------------------------------------------------------- |
| [**Status**](#status)                           | `sensor` | Robot        | Overall state of the robot and power supply<br/>• Category: Diagnostic                                |
| [**RSSI**](#wi-fi-signal-strength-rssi)         | `sensor` | Power supply | Wi-Fi signal strength in dBm<br/>• Device Class: Signal Strength<br/>• Category: Diagnostic           |
| [**Network Name**](#network-name)               | `sensor` | Power supply | Wi-Fi network the power supply is on<br/>• Category: Diagnostic                                       |
| [**Clean Mode**](#clean-mode)                   | `sensor` | Robot        | Mode of the current or last clean<br/>• Category: Diagnostic                                          |
| [**Power Supply Status**](#power-supply-status) | `sensor` | Power supply | State the power supply reports<br/>• Category: Diagnostic                                             |
| [**Robot Status**](#robot-status)               | `sensor` | Robot        | State the robot reports<br/>• Category: Diagnostic                                                    |
| [**Robot Type**](#robot-type)                   | `sensor` | Robot        | Robot type, such as S4<br/>• Category: Diagnostic                                                     |
| [**Cycle Count**](#cycle-count)                 | `sensor` | Robot        | How many times the robot has turned on<br/>• State Class: Total Increasing<br/>• Category: Diagnostic |

### Cleaning Cycle Sensors

| Entity                                  | Type     | Unit  | Functionality                                                                                               |
| --------------------------------------- | -------- | ----- | ----------------------------------------------------------------------------------------------------------- |
| [**Cycle Time Left**](#cycle-time-left) | `sensor` | Hours | Time left in the current clean<br/>• Start and expected end time in attributes<br/>• Device Class: Duration |

### Filter & Maintenance Sensors

| Entity                              | Type     | Functionality                                                                                             |
| ----------------------------------- | -------- | --------------------------------------------------------------------------------------------------------- |
| [**Filter Status**](#filter-status) | `sensor` | How full the filter bag is, from Empty to Full<br/>• Raw value in attributes<br/>• Icon follows the state |

### Error Sensors

| Entity                                        | Type     | Device       | Functionality                                                                                           |
| --------------------------------------------- | -------- | ------------ | ------------------------------------------------------------------------------------------------------- |
| [**Robot Error**](#robot-error)               | `sensor` | Robot        | Robot error from the current clean, or Ok<br/>• Icon changes on error<br/>• Category: Diagnostic        |
| [**Power Supply Error**](#power-supply-error) | `sensor` | Power supply | Power supply error from the current clean, or Ok<br/>• Icon changes on error<br/>• Category: Diagnostic |

### Environment Sensors

| Entity                                           | Type     | Unit | Functionality                                                                                       |
| ------------------------------------------------ | -------- | ---- | --------------------------------------------------------------------------------------------------- |
| [**Temperature**](#temperature-m700-models-only) | `sensor` | °C   | Water temperature (M700 robots only)<br/>• Device Class: Temperature<br/>• State Class: Measurement |

---

## 🔌 Binary Sensor Entities (2)

| Entity                                                  | Type            | Functionality                                                                                                                                                            |
| ------------------------------------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [**AWS Broker**](#aws-broker-connectivity)              | `binary_sensor` | Home Assistant's connection to the Maytronics cloud:<br/>• **On** - Connected<br/>• **Off** - Disconnected<br/>• Device Class: Connectivity<br/>• Category: Diagnostic   |
| [**Power Supply Connection**](#power-supply-connection) | `binary_sensor` | Whether the power supply is connected to the Maytronics cloud:<br/>• **On** - Online<br/>• **Off** - Offline<br/>• Device Class: Connectivity<br/>• Category: Diagnostic |

---

## 🔘 Button Entity (1)

| Entity                                                | Type     | Functionality                                                                                                                                               |
| ----------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [**Reset Filter Indicator**](#reset-filter-indicator) | `button` | Clears the "filter full" indicator after you clean the filter:<br/>• Sends `resetFbi` to the robot, as the MyDolphin app does<br/>• Category: Configuration |

---

## Summary by Platform

| Platform          | Count  | Purpose                                    |
| ----------------- | ------ | ------------------------------------------ |
| **Vacuum**        | 1      | Main robot control                         |
| **Remote**        | 1      | Manual drive                               |
| **Light**         | 1      | LED on and off                             |
| **Select**        | 1      | LED pattern                                |
| **Number**        | 2      | LED intensity and cycle time               |
| **Sensor**        | 13     | Status, diagnostics, cleaning info, errors |
| **Binary Sensor** | 2      | Cloud and power supply connection          |
| **Button**        | 1      | Reset the filter indicator                 |
| **TOTAL**         | **22** | 21 without the M700 temperature sensor     |

---

## Entity Categories

- **Configuration** (`EntityCategory.CONFIG`, 4): LED, LED Mode, LED Intensity, Reset Filter Indicator
- **Diagnostic** (`EntityCategory.DIAGNOSTIC`, 12): Status, RSSI, Network Name, Clean Mode, Power Supply Status, Robot Status, Robot Type, Cycle Count, Robot Error, Power Supply Error, AWS Broker, Power Supply Connection
- **No category** (5, or 6 on M700): Vacuum, Remote, Cycle Time, Filter Status, Cycle Time Left, Temperature

Home Assistant shows configuration and diagnostic entities in their own sections on the device page. Entities with no category are the main controls and sensors.

---

# Detailed Entity Information

---

## Vacuum Entity Details

### Main Vacuum Control

| Attribute     | Value                                       |
| ------------- | ------------------------------------------- |
| **Entity ID** | `vacuum.{robot_name}`                       |
| **Platform**  | Vacuum                                      |
| **Features**  | Start, Pause, Return to Base, Set Fan Speed |

#### Functionality

- **Start** (`vacuum.start`) - Start a clean in the current mode. Within a minute of the start, when the robot starts up, the integration sets the cycle time to the robot's own time for that mode. Otherwise the robot would reuse the time of its last clean.
- **Pause** (`vacuum.pause`) - Turn the power supply off, which ends the clean. It does nothing while the robot is docked.
- **Return to Base** (`vacuum.return_to_base`) - Run Pickup, which brings the robot to the pool wall so you can lift it out.
- **Set Fan Speed** (`vacuum.set_fan_speed`) - Choose the clean mode. The list holds the modes the robot supports, as the MyDolphin app shows them, plus Pickup. If Maytronics doesn't say which modes the robot supports, the list holds all of them:
  - `all` - Regular
  - `short` - Fast mode
  - `floor` - Floor only
  - `water` - Water line
  - `ultra` - Ultra clean
  - `stairs` - Full coverage
  - `pickup` - Pickup

#### States

- `docked` - Not cleaning
- `cleaning` - Cleaning the pool
- `returning` - Running Pickup
- `error` - The robot or power supply reports a fault

#### Attributes

- `fan_speed` - Current clean mode
- `fan_speed_list` - Modes you can choose
- `mode` - Current clean mode, the same as `fan_speed`

---

## Remote Control Entity Details

### Manual Drive

| Attribute     | Value                 |
| ------------- | --------------------- |
| **Entity ID** | `remote.{robot_name}` |
| **Platform**  | Remote                |
| **Features**  | Activity              |

#### Functionality

- **Turn On** (`remote.turn_on`) - Start manual mode. Pass an `activity` to move in that direction; with none, the robot stops.
- **Send Command** (`remote.send_command`) - Move in a direction:
  - `forward`
  - `backward`
  - `left`
  - `right`
  - `stop`
- **Turn Off** (`remote.turn_off`) - Leave manual mode

#### States

- `on` - Manual mode
- `off` - Not in manual mode

#### Attributes

- `Activity` - Last direction sent

#### Notes

- The robot only takes directions while it cleans or is already in manual mode. Otherwise the integration logs an error and sends nothing.
- Every direction runs at full speed; `stop` sends speed 0.

---

## Light Entity Details

### LED Light Control

| Attribute           | Value                    |
| ------------------- | ------------------------ |
| **Entity ID**       | `light.{robot_name}_led` |
| **Platform**        | Light                    |
| **Color Mode**      | On/off                   |
| **Entity Category** | Configuration            |

#### Functionality

- **Turn On** (`light.turn_on`) - Turn the LED on
- **Turn Off** (`light.turn_off`) - Turn the LED off

The light has no brightness. Use [LED Intensity](#led-intensity) to set it, and [LED Mode](#select-entity-details) to choose the pattern.

---

## Select Entity Details

### LED Mode Selection

| Attribute           | Value                          |
| ------------------- | ------------------------------ |
| **Entity ID**       | `select.{robot_name}_led_mode` |
| **Platform**        | Select                         |
| **Entity Category** | Configuration                  |

#### Options

| Option | Shown as  |
| ------ | --------- |
| `1`    | Blinking  |
| `2`    | Always on |
| `3`    | Disco     |

The icon follows the chosen option.

---

## Number Entities Details

### LED Intensity

| Attribute           | Value                               |
| ------------------- | ----------------------------------- |
| **Entity ID**       | `number.{robot_name}_led_intensity` |
| **Platform**        | Number                              |
| **Entity Category** | Configuration                       |
| **Range**           | 0-100                               |
| **Unit**            | %                                   |

Sets the brightness of the robot's LED.

---

### Cycle Time

| Attribute        | Value                            |
| ---------------- | -------------------------------- |
| **Entity ID**    | `number.{robot_name}_cycle_time` |
| **Platform**     | Number                           |
| **Device Class** | Duration                         |
| **Range**        | 1-600                            |
| **Unit**         | Minutes                          |

How long the current clean runs, as the robot reports it. When the robot is idle, this is the time of its last clean.

#### Functionality

- **Set Value** (`number.set_value`) - Change how long the current clean runs. The robot only accepts this while it cleans or starts up, so setting it while idle fails with an error.
- A clean started from Home Assistant uses the robot's own time for its mode (see [Start](#main-vacuum-control)). A clean started from the MyDolphin app or a schedule keeps the time it chose.

**Attributes**: `start_time` - When the clean started

**Icon**: Clock showing the hours

---

## Sensor Entities Details

### Status & Diagnostic Sensors

#### Status

| Attribute           | Value                        |
| ------------------- | ---------------------------- |
| **Entity ID**       | `sensor.{robot_name}_status` |
| **Entity Category** | Diagnostic                   |

The overall state, worked out from the robot and power supply states.

**States**: Off, On, Checking Environment, Cleaning, Programming, Idle (Delay), Idle (Weekly), Error

**Attributes**: `Calculated State`, `Vacuum State`, `Power Supply State`, `Robot State`, `Robot Type`, `Busy`, `Turn On Count`, `Time Zone`, `Activity`

---

#### Wi-Fi Signal Strength (RSSI)

| Attribute           | Value                      |
| ------------------- | -------------------------- |
| **Entity ID**       | `sensor.{robot_name}_rssi` |
| **Device**          | {Robot Name} Power Supply  |
| **Device Class**    | Signal Strength            |
| **Entity Category** | Diagnostic                 |
| **Unit**            | dBm                        |

Wi-Fi signal strength at the power supply. About -30 dBm is excellent and -90 dBm is poor.

---

#### Network Name

| Attribute           | Value                              |
| ------------------- | ---------------------------------- |
| **Entity ID**       | `sensor.{robot_name}_network_name` |
| **Device**          | {Robot Name} Power Supply          |
| **Entity Category** | Diagnostic                         |

Name (SSID) of the Wi-Fi network the power supply is on.

---

#### Clean Mode

| Attribute           | Value                            |
| ------------------- | -------------------------------- |
| **Entity ID**       | `sensor.{robot_name}_clean_mode` |
| **Entity Category** | Diagnostic                       |

Mode of the current or last clean.

| State    | Shown as      |
| -------- | ------------- |
| `all`    | Regular       |
| `short`  | Fast mode     |
| `floor`  | Floor only    |
| `water`  | Water line    |
| `ultra`  | Ultra clean   |
| `stairs` | Full coverage |
| `pickup` | Pickup        |

---

#### Power Supply Status

| Attribute           | Value                                     |
| ------------------- | ----------------------------------------- |
| **Entity ID**       | `sensor.{robot_name}_power_supply_status` |
| **Device**          | {Robot Name} Power Supply                 |
| **Entity Category** | Diagnostic                                |

State the power supply reports.

**States**: On, Off, Cleaning, Programming, Idle (Delay), Idle (Weekly), Error

---

#### Robot Status

| Attribute           | Value                              |
| ------------------- | ---------------------------------- |
| **Entity ID**       | `sensor.{robot_name}_robot_status` |
| **Entity Category** | Diagnostic                         |

State the robot reports.

**States**: Initialized, Scanning, Finished, Programming, Fault, Disconnected

---

#### Robot Type

| Attribute           | Value                            |
| ------------------- | -------------------------------- |
| **Entity ID**       | `sensor.{robot_name}_robot_type` |
| **Entity Category** | Diagnostic                       |

Robot type code, such as S4. The device page also shows it as the hardware version.

---

#### Cycle Count

| Attribute           | Value                             |
| ------------------- | --------------------------------- |
| **Entity ID**       | `sensor.{robot_name}_cycle_count` |
| **Entity Category** | Diagnostic                        |
| **State Class**     | Total Increasing                  |

How many times the robot has turned on, which is about one per clean.

---

### Cleaning Cycle Sensors

#### Cycle Time Left

| Attribute        | Value                                 |
| ---------------- | ------------------------------------- |
| **Entity ID**    | `sensor.{robot_name}_cycle_time_left` |
| **Device Class** | Duration                              |
| **State Class**  | Measurement                           |
| **Unit**         | Hours                                 |

Time left in the current clean. The robot reports seconds; Home Assistant shows hours and minutes by default, such as 0h 45m, and you can pick another unit in the entity settings. It shows 0 when the robot isn't cleaning.

**Attributes**:

- `start_time` - When the clean started
- `expected_end_time` - When the clean should finish

**Icon**: Clock showing the hours left

---

### Filter & Maintenance Sensors

#### Filter Status

| Attribute     | Value                               |
| ------------- | ----------------------------------- |
| **Entity ID** | `sensor.{robot_name}_filter_status` |

How full the filter bag is.

| State            | Shown as       | Raw value |
| ---------------- | -------------- | --------- |
| `empty`          | Empty          | 0         |
| `partially_full` | Partially full | 1-25      |
| `getting_full`   | Getting full   | 26-74     |
| `almost_full`    | Almost full    | 75-99     |
| `full`           | Full           | 100       |
| `fault`          | Fault          | 101       |
| `not_available`  | Not available  | 102       |
| `unknown`        | Unknown        | -1        |

**Attributes**:

- `status` - Raw value from the robot
- `reset_fbi` - Whether a filter indicator reset is pending

**Icon**: Gauge that follows the state

---

#### Reset Filter Indicator

| Attribute           | Value                                        |
| ------------------- | -------------------------------------------- |
| **Entity ID**       | `button.{robot_name}_reset_filter_indicator` |
| **Entity Category** | Configuration                                |

Press after cleaning the filter to clear the "filter full" indicator. It sends `{"filterBagIndication": {"resetFbi": true}}` to the robot. The Filter Status sensor changes when the robot next reports.

**Attributes**: `status` and `reset_fbi`, the same values as the Filter Status sensor.

---

### Error Sensors

Both sensors show the error code as a name, such as Robot stuck. They show Ok unless the error comes from the current clean, so an old error clears when the robot next turns on. Codes 0 and 255 both mean Ok.

When the state changes to an error, the integration fires a `mydolphin_plus_error` event. See the [README](../README.md#error-event) for the event data and the list of codes.

#### Robot Error

| Attribute           | Value                                              |
| ------------------- | -------------------------------------------------- |
| **Entity ID**       | `sensor.{robot_name}_robot_error`                  |
| **Entity Category** | Diagnostic                                         |
| **Icon**            | `mdi:robot-vacuum-variant`, with `-alert` on error |

Errors the robot reports.

---

#### Power Supply Error

| Attribute           | Value                                      |
| ------------------- | ------------------------------------------ |
| **Entity ID**       | `sensor.{robot_name}_power_supply_error`   |
| **Device**          | {Robot Name} Power Supply                  |
| **Entity Category** | Diagnostic                                 |
| **Icon**            | `mdi:water-boiler`, with `-alert` on error |

Errors the power supply reports.

---

### Environment Sensors

#### Temperature (M700 Models Only)

| Attribute        | Value                             |
| ---------------- | --------------------------------- |
| **Entity ID**    | `sensor.{robot_name}_temperature` |
| **Device Class** | Temperature                       |
| **State Class**  | Measurement                       |
| **Unit**         | °C                                |

Water temperature from the robot. Only M700 robots get this entity.

---

## Binary Sensor Entity Details

### AWS Broker Connectivity

| Attribute           | Value                                   |
| ------------------- | --------------------------------------- |
| **Entity ID**       | `binary_sensor.{robot_name}_aws_broker` |
| **Device**          | {Robot Name} Power Supply               |
| **Device Class**    | Connectivity                            |
| **Entity Category** | Diagnostic                              |
| **Icon**            | `mdi:aws`                               |

Whether Home Assistant is connected to the Maytronics cloud (AWS IoT), which carries the robot's updates and commands.

#### States

- `on` - Connected; updates arrive as the robot sends them, and commands go out at once
- `off` - Disconnected; the integration retries after 1, 2, 4 and 8 minutes, then every 15 minutes

#### Attributes

- `status` - Connection status, such as `Connected to the API`

---

### Power Supply Connection

| Attribute           | Value                                                |
| ------------------- | ---------------------------------------------------- |
| **Entity ID**       | `binary_sensor.{robot_name}_power_supply_connection` |
| **Device**          | {Robot Name} Power Supply                            |
| **Device Class**    | Connectivity                                         |
| **Entity Category** | Diagnostic                                           |

Whether the power supply is connected to the Maytronics cloud, from `isConnected.connected` in the robot's state. This differs from AWS Broker, which is Home Assistant's own connection.

The power supply stays online when the robot is off between cleans, so this can be on while the robot reports as disconnected.

---

## Usage Examples

### Starting a Clean

```yaml
# Start a clean in the current mode
service: vacuum.start
target:
  entity_id: vacuum.my_dolphin

# Choose Floor only, then start
service: vacuum.set_fan_speed
data:
  fan_speed: floor
target:
  entity_id: vacuum.my_dolphin

service: vacuum.start
target:
  entity_id: vacuum.my_dolphin
```

### Manual Drive

```yaml
# Start manual mode and drive forward
service: remote.turn_on
data:
  activity: forward
target:
  entity_id: remote.my_dolphin

# Stop
service: remote.send_command
data:
  command: stop
target:
  entity_id: remote.my_dolphin

# Leave manual mode
service: remote.turn_off
target:
  entity_id: remote.my_dolphin
```

### LED Control

```yaml
# Turn the LED on at half brightness
service: light.turn_on
target:
  entity_id: light.my_dolphin_led

service: number.set_value
data:
  value: 50
target:
  entity_id: number.my_dolphin_led_intensity
```

### Change the Current Clean's Time

```yaml
# Run the current clean for 90 minutes; the robot must be cleaning
service: number.set_value
data:
  value: 90
target:
  entity_id: number.my_dolphin_cycle_time
```

### Automation Examples

#### Daily Clean

```yaml
automation:
  - alias: "Pool Robot Daily Clean"
    trigger:
      - platform: time
        at: "06:00:00"
    condition:
      - condition: state
        entity_id: binary_sensor.my_dolphin_aws_broker
        state: "on"
    action:
      - service: vacuum.set_fan_speed
        data:
          fan_speed: all # Regular
        target:
          entity_id: vacuum.my_dolphin
      - service: vacuum.start
        target:
          entity_id: vacuum.my_dolphin
```

#### Filter Alert

```yaml
automation:
  - alias: "Pool Robot Filter Almost Full"
    trigger:
      - platform: state
        entity_id: sensor.my_dolphin_filter_status
        to: "almost_full"
    action:
      - service: notify.mobile_app
        data:
          title: "Pool Robot Maintenance"
          message: "The pool robot filter is almost full."
```

#### Error Alert

```yaml
automation:
  - alias: "Pool Robot Error Alert"
    trigger:
      - platform: event
        event_type: mydolphin_plus_error
    action:
      - service: notify.mobile_app
        data:
          title: "{{ trigger.event.data.name }}"
          message: >
            Error code {{ trigger.event.data.state }}.
            {{ trigger.event.data.instructions or '' }}
```

#### Connection Lost

```yaml
automation:
  - alias: "Pool Robot Connection Lost"
    trigger:
      - platform: state
        entity_id: binary_sensor.my_dolphin_aws_broker
        to: "off"
        for:
          minutes: 5
    action:
      - service: notify.mobile_app
        data:
          title: "Pool Robot Offline"
          message: "Home Assistant lost its connection to the pool robot."
```

---

## Additional Resources

- **Integration GitHub**: https://github.com/sebr/dolphin-robot-home-assistant
- **How the integration talks to Maytronics**: [docs/Maytronics](Maytronics/00-overview.md)
- **Home Assistant Vacuum Documentation**: https://www.home-assistant.io/integrations/vacuum/
- **Maytronics**: https://www.maytronics.com/

---

## Notes

1. **Entity IDs**: You can change entity IDs, names and icons in Home Assistant's entity settings.
2. **Updates**: Most entities update as the robot sends its state. The integration also asks the robot for its full state every 30 seconds.
3. **M700 robots**: Only M700 robots get the temperature sensor.
