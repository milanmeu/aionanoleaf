# Copyright 2021, Milan Meulemans.
#
# This file is part of aionanoleaf.
#
# aionanoleaf is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# aionanoleaf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with aionanoleaf.  If not, see <https://www.gnu.org/licenses/>.

"""Nanoleaf."""
from __future__ import annotations

import asyncio
import json

from aiohttp import (
    ClientConnectorError,
    ClientResponse,
    ClientSession,
    ClientTimeout,
    ServerDisconnectedError,
)

from .exceptions import InvalidEffect, InvalidToken, NoAuthToken, Unauthorized, Unavailable
from .typing import InfoData


class Nanoleaf:
    """Nanoleaf device."""

    _REQUEST_TIMEOUT = ClientTimeout(total=5, sock_connect=3)

    def __init__(
        self,
        session: ClientSession,
        host: str,
        auth_token: str | None = None,
        port: int = 16021,
    ) -> None:
        """Initialize the Nanoleaf."""
        self._session = session
        self._host = host
        self._auth_token = auth_token
        self._port = port

    @property
    def host(self) -> str:
        """Return the host."""
        return self._host

    @property
    def auth_token(self) -> str:
        """Return the auth_token."""
        if self._auth_token is None:
            raise NoAuthToken(
                "Authorize or set an auth_token before making this request."
            )
        return self._auth_token

    @property
    def port(self) -> int:
        """Return the port."""
        return self._port

    @property
    def name(self) -> str:
        """Return the name."""
        return self._name

    @property
    def serial_no(self) -> str:
        """Return the serialNo."""
        return self._serial_no

    @property
    def manufacturer(self) -> str:
        """Return the manufacturer."""
        return self._manufacturer

    @property
    def firmware_version(self) -> str:
        """Return the firmware version."""
        return self._firmware_version

    @property
    def model(self) -> str:
        """Return the model."""
        return self._model

    @property
    def is_on(self) -> bool:
        """Return if the Nanoleaf is on."""
        return self._is_on

    @property
    def brightness(self) -> int:
        """Return the brightness."""
        return self._brightness

    @property
    def brightness_max(self) -> int:
        """Return the maximum brightness."""
        return self._brightness_max

    @property
    def brightness_min(self) -> int:
        """Return the minimum brightness."""
        return self._brightness_min

    @property
    def hue(self) -> int:
        """Return the hue."""
        return self._hue

    @property
    def hue_max(self) -> int:
        """Return the maximum hue."""
        return self._hue_max

    @property
    def hue_min(self) -> int:
        """Return the minimum hue."""
        return self._hue_min

    @property
    def saturation(self) -> int:
        """Return the saturation."""
        return self._saturation

    @property
    def saturation_max(self) -> int:
        """Return the maximum saturation."""
        return self._saturation_max

    @property
    def saturation_min(self) -> int:
        """Return the minimum saturation."""
        return self._saturation_min

    @property
    def color_temperature(self) -> int:
        """Return the color temperature."""
        return self._color_temperature

    @property
    def color_temperature_max(self) -> int:
        """Return the maximum color temperature."""
        return self._color_temperature_max

    @property
    def color_temperature_min(self) -> int:
        """Return the minimum color temperature."""
        return self._color_temperature_min

    @property
    def color_mode(self) -> str:
        """Return the color mode."""
        return self._color_mode

    @property
    def effects_list(self) -> list[str]:
        """Return the effectsList."""
        return self._effects_list

    @property
    def effect(self) -> str:
        """Return the effect."""
        return self._effect

    @property
    def selected_effect(self) -> str | None:
        """Return the selected effect."""
        return self.effect if self.effect in self.effects_list else None

    @property
    def _api_url(self) -> str:
        return f"http://{self.host}:{self.port}/api/v1"

    async def _request(
        self, method: str, path: str, data: dict | None = None
    ) -> ClientResponse:
        """Make an authorized request to Nanoleaf with an auth_token."""
        url = f"{self._api_url}/{self.auth_token}/{path}"
        data = json.dumps(data)
        try:
            try:
                resp = await self._session.request(method, url, data=data, timeout=self._REQUEST_TIMEOUT)
            except ServerDisconnectedError:
                # Retry request once if the device disconnected
                resp = await self._session.request(method, url, data=data, timeout=self._REQUEST_TIMEOUT)
        except ClientConnectorError as err:
            raise Unavailable from err
        except asyncio.TimeoutError as err:
            raise Unavailable from err
        if resp.status == 401:
            raise InvalidToken
        resp.raise_for_status()
        return resp

    async def authorize(self) -> None:
        """
        Authorize to get a new Nanoleaf auth_token.

        Hold the on-off button down for 5-7 seconds until the LED starts flashing in a pattern and call authorize() within 30 seconds.
        """
        try:
            resp = await self._session.post(f"{self._api_url}/new")
        except ClientConnectorError as err:
            raise Unavailable from err
        if resp.status == 403:
            raise Unauthorized(
                "Hold the on-off button down for 5-7 seconds until the LED starts flashing in a pattern and call authorize() within 30 seconds."
            )
        resp.raise_for_status()
        self._auth_token = (await resp.json())["auth_token"]

    async def deauthorize(self) -> None:
        """Remove the auth_token from the Nanoleaf."""
        await self._request("delete", "")
        self._auth_token = None

    async def get_info(self) -> None:
        """Get all device info."""
        resp = await self._request("get", "")
        data: InfoData = await resp.json()
        self._name = data["name"]
        self._serial_no = data["serialNo"]
        self._manufacturer = data["manufacturer"]
        self._firmware_version = data["firmwareVersion"]
        self._model = data["model"]
        self._is_on = data["state"]["on"]["value"]
        self._brightness = data["state"]["brightness"]["value"]
        self._brightness_max = data["state"]["brightness"]["max"]
        self._brightness_min = data["state"]["brightness"]["min"]
        self._hue = data["state"]["hue"]["value"]
        self._hue_max = data["state"]["hue"]["max"]
        self._hue_min = data["state"]["hue"]["min"]
        self._saturation = data["state"]["sat"]["value"]
        self._saturation_max = data["state"]["sat"]["max"]
        self._saturation_min = data["state"]["sat"]["min"]
        self._color_temperature = data["state"]["ct"]["value"]
        self._color_temperature_max = data["state"]["ct"]["max"]
        self._color_temperature_min = data["state"]["ct"]["min"]
        self._color_mode = data["state"]["colorMode"]
        self._effects_list = data["effects"]["effectsList"]
        self._effect = data["effects"]["select"]

    async def set_state(
        self,
        on: bool | None = None,
        brightness: int | None = None,
        brightness_relative: bool = False,
        brightness_transition: int | None = None,
        color_temperature: int | None = None,
        color_temperature_relative: bool = False,
        hue: int | None = None,
        hue_relative: bool = False,
        saturation: int | None = None,
        saturation_relative: bool = False,
    ) -> None:
        """Write a new state to Nanoleaf."""
        data = {}

        async def _add_topic_to_data(
            topic: str, value: int | bool | None, relative: bool = False
        ) -> None:
            if value is not None:
                if relative:
                    data[topic] = {"increment": value}
                else:
                    data[topic] = {"value": value}

        await _add_topic_to_data("brightness", brightness, brightness_relative)
        if brightness_transition is not None:
            if "brightness" in data:
                data["brightness"]["duration"] = brightness_transition
        await _add_topic_to_data("ct", color_temperature, color_temperature_relative)
        await _add_topic_to_data("hue", hue, hue_relative)
        await _add_topic_to_data("sat", saturation, saturation_relative)
        await _add_topic_to_data("on", on)  # "on" must be the last key in data
        if data:
            await self._request("put", "state", data)

    async def _set_state(
        self,
        topic: str,
        value: int | bool,
        relative: bool = False,
        transition: int | None = None,
    ) -> None:
        """Write state to Nanoleaf."""
        data: dict
        if relative:
            data = {topic: {"increment": value}}
        else:
            data = {topic: {"value": value}}
        if transition is not None:
            data[topic]["duration"] = transition
        await self._request("put", "state", data)

    async def set_effect(self, effect: str) -> None:
        """Write effect to Nanoleaf."""
        if effect not in self.effects_list:
            raise InvalidEffect
        await self._request("put", "effects", {"select": effect})

    async def set_brightness(
        self, brightness: int, relative: bool = False, transition: int | None = None
    ) -> None:
        """Set absolute or relative brightness with or without transition."""
        await self._set_state("brightness", brightness, relative, transition)

    async def set_saturation(self, saturation: int, relative: bool = False) -> None:
        """Set absolute or relative saturation."""
        await self._set_state("sat", saturation, relative)

    async def set_hue(self, hue: int, relative: bool = False) -> None:
        """Set absolute or relative hue."""
        await self._set_state("hue", hue, relative)

    async def set_color_temperature(
        self, color_temperature: int, relative: bool = False
    ) -> None:
        """Set absolute or relative color temperature."""
        await self._set_state("ct", color_temperature, relative)

    async def turn_on(self) -> None:
        """Turn the Nanoleaf on."""
        await self._set_state("on", True)

    async def turn_off(self, transition: int | None = None) -> None:
        """Turn the Nanoleaf off with or without transition."""
        if transition is None:
            await self._set_state("on", False)
        else:
            await self.set_brightness(0, transition=transition)

    async def identify(self) -> None:
        """Identify the Nanoleaf."""
        await self._request("put", "identify")
