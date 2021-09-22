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

"""Nanoleaf events."""
from __future__ import annotations

from abc import ABC

SINGLE_TAP = "Single Tap"
DOUBLE_TAP = "Double Tap"
SWIPE_UP = "Swipe Up"
SWIPE_DOWN = "Swipe Down"
SWIPE_LEFT = "Swipe Left"
SWIPE_RIGHT = "Swipe Right"


class Event(ABC):
    """Abstract Nanoleaf event."""

    # Docs: https://forum.nanoleaf.me/docs/openapi#_1qvwts5tbjof
    EVENT_TYPE_ID: int


class StateEvent(Event):
    """Nanoleaf state event."""

    EVENT_TYPE_ID = 1

    def __init__(self, event_data: dict) -> None:
        """Init Nanoleaf state event."""
        self._event_data = event_data

    @property
    def attribute_id(self) -> int:
        """Return attribute ID."""
        return self._event_data["attr"]

    @property
    def attribute(self) -> str:
        """Return event attribute."""
        # Docs: https://forum.nanoleaf.me/docs/openapi#_mwh9o1uit6dg
        return {
            1: "on",
            2: "brightness",
            3: "hue",
            4: "saturation",
            5: "ct",
            6: "colorMode",
        }[self.attribute_id]

    @property
    def value(self) -> int | str:
        """Return event value, this is the new state of the attribute."""
        return self._event_data["value"]


class LayoutEvent(Event):
    """Nanoleaf layout event."""

    EVENT_TYPE_ID = 2

    def __init__(self, event_data: dict) -> None:
        self._event_data = event_data

    @property
    def attribute_id(self) -> int:
        """Return event attribute ID."""
        return self._event_data["attr"]

    @property
    def attribute(self) -> str:
        """Return event attribute."""
        # Docs: https://forum.nanoleaf.me/docs/openapi#_dxks97cpzdpf
        return {
            1: "layout",
            2: "globalOrientation",
        }[self.attribute_id]


class EffectsEvent(Event):
    """Nanoleaf effects event."""
    # Docs: https://forum.nanoleaf.me/docs/openapi#_mq2t1mg34g97

    EVENT_TYPE_ID = 3

    def __init__(self, event_data: dict) -> None:
        self._event_data = event_data

    @property
    def attribute_id(self) -> int:
        """Return event attribute ID."""
        return self._event_data["attr"]


class TouchEvent(Event):
    """Nanoleaf touch event."""

    EVENT_TYPE_ID = 4

    def __init__(self, event_data) -> None:
        self._event_data = event_data

    @property
    def gesture_id(self) -> int:
        """Return gesture ID."""
        return self._event_data["gesture"]

    @property
    def gesture(self) -> str:
        """Return gesture."""
        return {
            0: SINGLE_TAP,
            1: DOUBLE_TAP,
            2: SWIPE_UP,
            3: SWIPE_DOWN,
            4: SWIPE_LEFT,
            5: SWIPE_RIGHT,
        }[self.gesture_id]

    @property
    def panel_id(self) -> int | None:
        """Return panel ID if gesture has an associated panel else None."""
        # Docs: https://forum.nanoleaf.me/docs/openapi#_842h3097vbgq
        panel_id = self._event_data["panelId"]
        return None if panel_id == -1 else panel_id
