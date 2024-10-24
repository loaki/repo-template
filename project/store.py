import json
import os
from collections import OrderedDict
from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta,
)
from typing import (
    Dict,
    List,
    Optional,
    Set,
    TypeVar,
    Union,
    cast,
)

import isodate


T = TypeVar("T")


@dataclass
class SettingVariable:
    description: str
    additional_columns: Dict[str, str]


EnvDictionary = Dict[str, SettingVariable]


class Store:
    _settings: EnvDictionary

    def __init__(self) -> None:
        self._settings = {}

    def _store(
        self, key: str, description: Optional[str] = None, additional_columns: Optional[Dict[str, str]] = None
    ) -> None:
        if key in self._settings:
            return None
        self._settings[key] = SettingVariable(
            description=description or "", additional_columns=additional_columns or dict()
        )

    def get_env(
        self,
        key: str,
        default: T,
        description: Optional[str] = None,
        additional_columns: Optional[Dict[str, str]] = None,
    ) -> Union[str, T]:
        self._store(key, description=description, additional_columns=additional_columns)
        return os.getenv(key, default)

    def get_env_as_str(
        self,
        key: str,
        default: str = "",
        description: Optional[str] = None,
        additional_columns: Optional[Dict[str, str]] = None,
    ) -> str:
        return self.get_env(key, default, description=description, additional_columns=additional_columns)

    def get_env_as_bool(
        self,
        key: str,
        default: bool = False,
        description: Optional[str] = None,
        additional_columns: Optional[Dict[str, str]] = None,
    ) -> bool:
        value = self.get_env(key, "", description=description, additional_columns=additional_columns)
        if not value:
            return default
        return value.lower() in ["1", "true", "on"] if value is not None else default

    def get_env_as_int(
        self,
        key: str,
        default: int,
        description: Optional[str] = None,
        additional_columns: Optional[Dict[str, str]] = None,
    ) -> int:
        value = self.get_env(key, "", description=description, additional_columns=additional_columns)
        if not value:
            return default
        return int(value)

    def get_env_as_float(
        self,
        key: str,
        default: float,
        description: Optional[str] = None,
        additional_columns: Optional[Dict[str, str]] = None,
    ) -> float:
        value = self.get_env(key, "", description=description, additional_columns=additional_columns)
        if not value:
            return default
        return float(value)

    def get_env_as_str_list(
        self,
        key: str,
        default: List[str],
        description: Optional[str] = None,
        additional_columns: Optional[Dict[str, str]] = None,
    ) -> List[str]:
        value = self.get_env(key, "", description=description, additional_columns=additional_columns)
        if not value:
            return default

        return value.split(",")

    def get_env_pattern_as_str_dict(
        self,
        prefix: str,
        description: Optional[str] = None,
        additional_columns: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        self._store(f"{prefix}{{STR}}", description=description, additional_columns=additional_columns)
        values = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                values[key.removeprefix(prefix)] = value
        return values

    def get_env_pattern_as_int_dict(
        self, prefix: str, description: Optional[str] = None, additional_columns: Optional[Dict[str, str]] = None
    ) -> Dict[str, int]:
        self._store(f"{prefix}{{STR}}", description=description, additional_columns=additional_columns)
        values = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                values[key.removeprefix(prefix)] = int(value)
        return values

    def get_env_as_date(
        self,
        key: str,
        default: T,
        format: str = "%d/%m/%Y %H:%M:%S%z",
        description: Optional[str] = None,
        additional_columns: Optional[Dict[str, str]] = None,
    ) -> Union[datetime, T]:
        """
        Parse date from environment according to the following default format:
        "%d/%m/%Y %H:%M:%S%z"

        example: '21/02/2024 16:04:39+0000'
        """
        value = self.get_env(key, "", description=description, additional_columns=additional_columns)
        if not value:
            return default
        try:
            return datetime.strptime(value, format)
        except ValueError:
            return default

    def get_env_as_iso8601_duration(
        self,
        key: str,
        default: timedelta,
        description: Optional[str] = None,
        additional_columns: Optional[Dict[str, str]] = None,
    ) -> timedelta:
        """
        Parse duration from environment according to the ISO 8601 duration format.

        example: 'P4DT1H15M20S'
        datetime.timedelta(days=4, seconds=4520)
        """

        value = self.get_env(key, "", description=description, additional_columns=additional_columns)
        if not value:
            return default
        duration = isodate.parse_duration(value)
        if isinstance(duration, isodate.Duration):
            return cast(timedelta, duration.tdelta)
        elif isinstance(duration, timedelta):
            return duration
        raise ValueError(f"Received an invalid type from the isodate library: {key=} {duration=} from {value=}")

    def get_env_as_int_set(
        self,
        key: str,
        default: Set[int],
        description: Optional[str] = None,
        additional_columns: Optional[Dict[str, str]] = None,
    ) -> Set[int]:
        value = self.get_env(key, None, description=description, additional_columns=additional_columns)

        if value is None or not value:
            return default

        return set(map(int, value.split(",")))

    @property
    def sorted_settings(self) -> EnvDictionary:
        return OrderedDict(sorted(self._settings.items()))

    def dump_markdown(self, crlf: str = "\n") -> str:
        from pytablewriter import MarkdownTableWriter

        headers = ["Key", "Description"]
        for setting_variable_key in self._settings:
            setting_variable = self._settings[setting_variable_key]
            for key in setting_variable.additional_columns:
                if key not in headers:
                    headers.append(key)

        value_matrix = []

        for setting_variable_key in self.sorted_settings:
            setting_variable = self._settings[setting_variable_key]
            base = [setting_variable_key, setting_variable.description]

            if len(headers) > 2:
                for index in range(2, len(headers)):
                    key = list(headers)[index]
                    if key in setting_variable.additional_columns:
                        base.append(setting_variable.additional_columns[key])
                    else:
                        base.append("")
            value_matrix.append(base)

        writer = MarkdownTableWriter(
            table_name="Settings\n",
            headers=headers,
            value_matrix=value_matrix,
            margin=1,
        )
        return writer.dumps()

    def dump_jsonl(self, crlf: str = "\n") -> str:
        output = ""
        for setting_variable_key in self.sorted_settings:
            setting_variable = self._settings[setting_variable_key]
            output += (
                json.dumps(
                    {
                        "key": setting_variable_key,
                        "description": setting_variable.description,
                        "additional_columns": setting_variable.additional_columns,
                    }
                )
                + crlf
            )
        return output


store = Store()
