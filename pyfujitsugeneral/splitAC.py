from .api import Api
from typing import Any

V_VANE_POSITION_UNKNOWN = "unknown"
V_VANE_POSITION_1 = "1_up"
V_VANE_POSITION_2 = "2"
V_VANE_POSITION_3 = "3"
V_VANE_POSITION_4 = "4_down"
V_VANE_POSITION_SWING = "swing"

SWING_LIST_DICT = [
    V_VANE_POSITION_UNKNOWN,
    V_VANE_POSITION_1,
    V_VANE_POSITION_2,
    V_VANE_POSITION_3,
    V_VANE_POSITION_4,
    V_VANE_POSITION_SWING,
]

_V_VANE_POSITION_LOOKUP = {
    0: V_VANE_POSITION_UNKNOWN,
    1: V_VANE_POSITION_1,
    2: V_VANE_POSITION_2,
    3: V_VANE_POSITION_3,
    4: V_VANE_POSITION_4,
    5: V_VANE_POSITION_SWING,
}


class SplitAC:
    def __init__(self, dsn: str, api_param: Api) -> None:
        self._dsn = dsn
        self._api = api_param  # Setting the API object

        # self.properties: For now this variable is not used but lots of device properties which are not implemented
        # this variable can be used to expose those properties and implement them.
        self.update_properties()

    # Method for getting new (refreshing) properties values
    def refresh_properties(self) -> None:
        self.update_properties()

    # Calling the api class _get_device_properties to get devices properties
    def update_properties(self) -> None:
        self._properties = self._api._get_device_properties(self._dsn)
        self.device_name = self._properties
        self.af_vertical_swing = self._properties
        self.af_vertical_direction = self._properties
        self.af_horizontal_swing = self._properties
        self.af_horizontal_direction = self._properties
        self.economy_mode = self._properties
        self.fan_speed = self._properties
        self.powerful_mode = self._properties
        self.min_heat = self._properties
        self.outdoor_low_noise = self._properties
        self.operation_mode = self._properties
        self.adjust_temperature = self._properties
        self.display_temperature = self._properties
        self.outdoor_temperature = self._properties

    # To Turn on the device get the last operation mode using property history method
    # Find the last not 'OFF'/'0' O.M.
    # Turn on by setting O.M. to the last O.M
    def turnOn(self):
        datapoints = self._get_device_property_history(self.operation_mode["key"])
        # Get the latest setting before turn off
        for datapoint in reversed(datapoints):
            if datapoint["datapoint"]["value"] != 0:
                last_operation_mode = int(datapoint["datapoint"]["value"])
                break

        self.operation_mode = last_operation_mode  # type: ignore
        self.refresh_properties()

    def turnOff(self):
        self.operation_mode = 0  # type: ignore
        self.refresh_properties()

    # Economy mode setting
    def economy_mode_on(self):
        self.economy_mode = 1

    def economy_mode_off(self):
        self.economy_mode = 0

    # Powerfull mode setting
    def powerfull_mode_on(self):
        self.powerful_mode = 1

    def powerfull_mode_off(self):
        self.powerful_mode = 0

    # Fan speed setting
    # Quiet Low Medium High Auto
    def changeFanSpeed(self, speed):
        if speed.upper() == "QUIET":
            self.fan_speed_quiet()
            return None
        if speed.upper() == "LOW":
            self.fan_speed_low()
            return None
        if speed.upper() == "MEDIUM":
            self.fan_speed_medium()
            return None
        if speed.upper() == "HIGH":
            self.fan_speed_high()
            return None
        if speed.upper() == "AUTO":
            self.fan_speed_auto()
            return None

    def fan_speed_quiet(self):
        self.fan_speed = 0

    def fan_speed_low(self):
        self.fan_speed = 1

    def fan_speed_medium(self):
        self.fan_speed = 2

    def fan_speed_high(self):
        self.fan_speed = 3

    def fan_speed_auto(self):
        self.fan_speed = 4

    def get_fan_speed_desc(self):
        FAN_SPEED_DICT = {0: "Quiet", 1: "Low", 2: "Medium", 3: "High", 4: "Auto"}
        return FAN_SPEED_DICT[self.fan_speed["value"]]

    # Vane vertical mode
    def changeSwingMode(self, mode) -> None:
        if mode.upper() == V_VANE_POSITION_1.upper():
            self.af_vertical_direction = 1
            self.af_vertical_swing = 0
            self.af_horizontal_swing = 0
        elif mode.upper() == V_VANE_POSITION_2.upper():
            self.af_vertical_direction = 2
            self.af_vertical_swing = 0
            self.af_horizontal_swing = 0
        elif mode.upper() == V_VANE_POSITION_3.upper():
            self.af_vertical_direction = 3
            self.af_vertical_swing = 0
            self.af_horizontal_swing = 0
        elif mode.upper() == V_VANE_POSITION_4.upper():
            self.af_vertical_direction = 4
            self.af_vertical_swing = 0
            self.af_horizontal_swing = 0
        elif mode.upper() == V_VANE_POSITION_SWING.upper():
            self.af_vertical_swing = 1
            self.af_horizontal_swing = 1

    def get_swing_mode_desc(self):
        try:
            return SWING_LIST_DICT[self.af_vertical_direction["value"]]
        except TypeError:
            return SWING_LIST_DICT[0]

    def vane_vertical_positions(self) -> list[str]:
        """Return available vertical vane positions."""
        SWING_LIST_DICT.pop(0)
        return SWING_LIST_DICT

    def vane_vertical(self) -> str:
        """Return vertical vane position."""
        verticalDirectionValue = self.af_vertical_direction["value"]
        verticalSwingValue = self.af_vertical_swing["value"]
        horizontalSwingValue = self.af_horizontal_swing["value"]
        if verticalSwingValue == 1 or horizontalSwingValue == 1:
            return V_VANE_POSITION_SWING
        else:
            return _V_VANE_POSITION_LOOKUP.get(
                verticalDirectionValue, V_VANE_POSITION_UNKNOWN
            )

    # Vertical
    def vertical_swing_on(self):
        self.af_vertical_swing = 1

    def vertical_swing_off(self):
        self.af_vertical_swing = 0

    # Horizontal
    def horizontal_swing_on(self):
        self.af_vertical_swing = 1

    def horizontal_swing_off(self):
        self.af_vertical_swing = 0

    # Temperature setting
    def changeTemperature(self, newTemperature):
        # set temperature for degree C
        if not isinstance(newTemperature, int) and not isinstance(
            newTemperature, float
        ):
            raise Exception("Wrong usage of method")
        # Fixing temps if not given as multiplies of 10 less than 160
        if newTemperature < 160:
            newTemperature = newTemperature * 10
        if newTemperature >= 160 and newTemperature <= 320:
            self.adjust_temperature = newTemperature
        else:
            raise Exception("out of range temperature!!")

    # Operation Mode setting
    def changeOperationMode(self, operationMode):
        if not isinstance(operationMode, int):
            operationMode = self._operation_mode_translate(operationMode)
        self.operation_mode = operationMode  # type: ignore

    # Class properties:

    @property
    def dsn(self):
        return self._dsn

    def _get_prop_from_json(
        self, propertyName: str, properties: Any
    ) -> dict[str, Any] | None:
        data = {}
        for property in properties:
            if property["property"]["name"] == propertyName:
                data = {
                    "value": property["property"]["value"],
                    "key": property["property"]["key"],
                }
        return data

    @property
    def operation_mode(self):
        return self._operation_mode

    @property
    def operation_mode_desc(self) -> Any:
        return self._operation_mode_translate(self.operation_mode["value"])

    @operation_mode.setter  # type: ignore
    def operation_mode(self, properties) -> None:
        if isinstance(properties, (list, tuple)):
            self._operation_mode = self._get_prop_from_json(
                "operation_mode", properties
            )
        elif isinstance(properties, int):
            self._api._set_device_property(self.operation_mode["key"], properties)
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method!")

    @property  # property to get display temperature in degree C
    def display_temperature_degree(self) -> float | None:
        data = None
        if self._display_temperature is not None:
            data = round(((self._display_temperature["value"] / 100 - 32) / 9 * 5), 1)
        return data

    @property  # property returns display temperature dict in 10 times of degree C
    def display_temperature(self) -> dict[str, Any] | None:
        return self._display_temperature

    @display_temperature.setter
    def display_temperature(self, properties: Any):
        if isinstance(properties, (list, tuple)):
            self._display_temperature = self._get_prop_from_json(
                "display_temperature", properties
            )
        elif isinstance(properties, int) or isinstance(properties, float):
            self._api._set_device_property(self.display_temperature["key"], properties)
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method!")

    @property  # property to get outdoor temperature in degree C
    def outdoor_temperature_degree(self) -> float | None:
        data = None
        if self._outdoor_temperature is not None:
            data = round(((self._outdoor_temperature["value"] / 100 - 32) / 9 * 5), 1)
        return data

    @property  # property returns outdoor temperature dict in 10 times of degree C
    def outdoor_temperature(self) -> dict[str, Any] | None:
        return self._outdoor_temperature

    @outdoor_temperature.setter
    def outdoor_temperature(self, properties: Any):
        if isinstance(properties, (list, tuple)):
            self._outdoor_temperature = self._get_prop_from_json(
                "outdoor_temperature", properties
            )
        elif isinstance(properties, int) or isinstance(properties, float):
            self._api._set_device_property(self.outdoor_temperature["key"], properties)
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method!")

    @property  # property to get temperature in degree C
    def adjust_temperature_degree(self) -> float | None:
        data = None
        if self._adjust_temperature is not None:
            adjustTemperatureValue = self._adjust_temperature["value"]
            if adjustTemperatureValue == 65535:
                datapoints = self._get_device_property_history(
                    self._adjust_temperature["key"]
                )
                # Get the latest setting other than invalid value
                for datapoint in reversed(datapoints):
                    if datapoint["datapoint"]["value"] != 65535:
                        adjustTemperatureValue = int(datapoint["datapoint"]["value"])
                        break
            data = round((adjustTemperatureValue / 10), 1)
        return data

    @property  # property returns temperature dict in 10 times of degree C
    def adjust_temperature(self):
        return self._adjust_temperature

    @adjust_temperature.setter
    def adjust_temperature(self, properties):
        if isinstance(properties, (list, tuple)):
            self._adjust_temperature = self._get_prop_from_json(
                "adjust_temperature", properties
            )
        elif isinstance(properties, int) or isinstance(properties, float):
            self._api._set_device_property(self.adjust_temperature["key"], properties)
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method!")

    @property
    def outdoor_low_noise(self):
        return self._outdoor_low_noise

    @outdoor_low_noise.setter
    def outdoor_low_noise(self, properties):
        if isinstance(properties, (list, tuple)):
            self._outdoor_low_noise = self._get_prop_from_json(
                "outdoor_low_noise", properties
            )
        elif isinstance(properties, int):
            self._api._set_device_property(self.outdoor_low_noise["key"], properties)
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method!")

    @property
    def powerful_mode(self):
        return self._powerful_mode

    @powerful_mode.setter
    def powerful_mode(self, properties):
        if isinstance(properties, (list, tuple)):
            self._powerful_mode = self._get_prop_from_json("powerful_mode", properties)
        elif isinstance(properties, int):
            self._api._set_device_property(self.powerful_mode["key"], properties)
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method!")

    @property
    def fan_speed(self):
        return self._fan_speed

    @fan_speed.setter
    def fan_speed(self, properties):
        if isinstance(properties, (list, tuple)):
            self._fan_speed = self._get_prop_from_json("fan_speed", properties)
        elif isinstance(properties, int):
            self._api._set_device_property(self.fan_speed["key"], properties)
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method!")

    @property
    def min_heat(self):
        return self._min_heat

    @min_heat.setter
    def min_heat(self, properties):
        if isinstance(properties, (list, tuple)):
            self._min_heat = self._get_prop_from_json("min_heat", properties)
        elif isinstance(properties, int):
            self._api._set_device_property(self.min_heat["key"], properties)
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method!")

    @property
    def economy_mode(self):
        return self._economy_mode

    @economy_mode.setter
    def economy_mode(self, properties):
        if isinstance(properties, (list, tuple)):
            self._economy_mode = self._get_prop_from_json("economy_mode", properties)
        elif isinstance(properties, int):
            self._api._set_device_property(self.economy_mode["key"], properties)
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method!")

    @property
    def af_horizontal_direction(self):
        return self._af_horizontal_direction

    @af_horizontal_direction.setter
    def af_horizontal_direction(self, properties):
        if isinstance(properties, (list, tuple)):
            self._af_horizontal_direction = self._get_prop_from_json(
                "af_horizontal_direction", properties
            )
        elif isinstance(properties, int):
            self._api._set_device_property(
                self.af_horizontal_direction["key"], properties
            )
            self.horizontal_swing_off()  # If direction set then swing will be turned OFF
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method or direction out of range!")

    @property
    def af_horizontal_swing(self):
        return self._af_horizontal_swing

    @af_horizontal_swing.setter
    def af_horizontal_swing(self, properties: Any):
        if isinstance(properties, (list, tuple)):
            self._af_horizontal_swing = self._get_prop_from_json(
                "af_horizontal_swing", properties
            )
        elif isinstance(properties, int):
            self._api._set_device_property(self.af_horizontal_swing["key"], properties)
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method!")

    @property
    def af_vertical_direction(self):
        return self._af_vertical_direction

    @af_vertical_direction.setter
    def af_vertical_direction(self, properties: Any) -> None:
        if isinstance(properties, (list, tuple)):
            self._af_vertical_direction = self._get_prop_from_json(
                "af_vertical_direction", properties
            )
        elif isinstance(properties, int):
            self._api._set_device_property(
                self.af_vertical_direction["key"], properties
            )
            self.vertical_swing_off()  ##If direction set then swing will be turned OFF
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method or direction out of range!")

    @property
    def af_vertical_swing(self) -> Any:
        return self._af_vertical_swing

    @af_vertical_swing.setter
    def af_vertical_swing(self, properties: Any) -> None:
        if isinstance(properties, (list, tuple)):
            self._af_vertical_swing = self._get_prop_from_json(
                "af_vertical_swing", properties
            )
        elif isinstance(properties, int):
            self._api._set_device_property(self.af_vertical_swing["key"], properties)
            self.refresh_properties()
        else:
            raise Exception("Wrong usage of the method!")

    @property
    def device_name(self) -> dict[str, Any] | None:
        return self._device_name

    @device_name.setter
    def device_name(self, properties: Any) -> None:
        self._device_name = self._get_prop_from_json("device_name", properties)

    @property
    def op_status(self) -> dict[str, Any] | None:
        return self._get_prop_from_json("op_status", self._properties)

    def get_op_status_desc(self) -> str | None:
        data = None
        if self.op_status is not None:
            DICT_OP_MODE = {0: "Normal", 16777216: "Defrost"}
            status = self.op_status["value"]
            data = (
                DICT_OP_MODE[status] if status in DICT_OP_MODE else f"Unknown {status}"
            )
            return data
        return data

    # Get a property history
    def _get_device_property_history(self, propertyCode: int) -> Any:
        propertyHistory = self._api._get_device_property(propertyCode)
        propertyHistory = propertyHistory.json()

        return propertyHistory

    # Translate the operation mode to descriptive values and reverse
    def _operation_mode_translate(self, operation_mode: Any) -> Any:
        DICT_OPERATION_MODE = {
            "off": 0,
            "heat": 1,
            "cool": 2,
            "auto": 3,
            "dry": 4,
            "fan_only": 5,
            "heat_alt": 6,
            0: "off",
            1: "heat",
            2: "cool",
            3: "auto",
            4: "dry",
            5: "fan_only",
            6: "heat",
        }
        return DICT_OPERATION_MODE[operation_mode]
