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

from .typing import (
    EffectsEventData,
    #EmersionEventData,
    LayoutEventData,
    StateEventData,
    TouchEventData,
)

SINGLE_TAP = "Single Tap"
DOUBLE_TAP = "Double Tap"
SWIPE_UP = "Swipe Up"
SWIPE_DOWN = "Swipe Down"
SWIPE_LEFT = "Swipe Left"
SWIPE_RIGHT = "Swipe Right"


class Event(ABC):
    """Abstract Nanoleaf event."""

    EVENT_TYPE_ID: int


class StateEvent(Event):
    """Nanoleaf state event."""

    EVENT_TYPE_ID = 1

    def __init__(self, event_data: StateEventData) -> None:
        """Init Nanoleaf state event."""
        self._event_data = event_data

    @property
    def attribute_id(self) -> int:
        """Return attribute ID."""
        return self._event_data["attr"]

    @property
    def attribute(self) -> str:
        """Return event attribute."""
        return {
            1: "is_on",
            2: "brightness",
            3: "hue",
            4: "saturation",
            5: "color_temperature",
            6: "color_mode",
        }[self.attribute_id]

    @property
    def value(self) -> str | int:
        """Return event value, this is the new state of the attribute."""
        return self._event_data["value"]


class LayoutEvent(Event):
    """Nanoleaf layout event."""

    EVENT_TYPE_ID = 2

    def __init__(self, event_data: LayoutEventData) -> None:
        """Init Nanoleaf layout event."""
        self._event_data = event_data

    @property
    def attribute_id(self) -> int:
        """Return event attribute ID."""
        return self._event_data["attr"]

    @property
    def attribute(self) -> str:
        """Return event attribute."""
        return {
            1: "layout",
            2: "global_orientation",
        }[self.attribute_id]


class EffectsEvent(Event):
    """Nanoleaf effects event."""

    EVENT_TYPE_ID = 3

    def __init__(self, event_data: EffectsEventData) -> None:
        """Init Nanoleaf effects event."""
        self._event_data = event_data

    @property
    def attribute_id(self) -> int:
        """Return event attribute ID."""
        return self._event_data["attr"]

    @property
    def effect(self) -> str:
        """Return the active effect."""
        return self._event_data["value"]
    
# class EmersionEvent(Event):
#     """Nanoleaf Emersion (4D) event. Not implemented yet since there are no events for this in the api :("""

#     EVENT_TYPE_ID = 5

#     def __init__(self, event_data: EmersionEventData) -> None:
#         """Init Nanoleaf emersion event."""
#         self._event_data = event_data

#     @property
#     def attribute_id(self) -> int:
#         """Return event attribute ID."""
#         return self._event_data["attr"]

#     @property
#     def effect(self) -> str:
#         """Return the active Emersion mode."""
#         return self._event_data["value"]
    
#     def emersion(self) -> int:
#         """Return event attribute."""
#         return {
#             1: 6, #1D
#             2: 2, #2D
#             3: 3, #3D
#             4: 5, #4D
#         }[self.attribute_id]


class TouchEvent(Event):
    """Nanoleaf touch event."""

    EVENT_TYPE_ID = 4

    def __init__(self, event_data: TouchEventData) -> None:
        """Init Nanoleaf touch event."""
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
        }.get(self.gesture_id, str(self.gesture_id))

    @property
    def panel_id(self) -> int | None:
        """Return panel ID if gesture has an associated panel else None."""
        panel_id = self._event_data["panelId"]
        return None if panel_id == -1 else panel_id


class TouchStreamEvent:
    """Nanoleaf touch stream event."""

    def __init__(
        self,
        panel_id: int,
        touch_type_id: int,
        strength: int,
        panel_id_2: int,
    ) -> None:
        """Init Nanoleaf touch stream event."""
        self._panel_id = panel_id
        self._touch_type_id = touch_type_id
        self._strength = strength
        self._panel_id_2 = panel_id_2

    @property
    def panel_id(self) -> int:
        """Return touch panel ID."""
        return self._panel_id

    @property
    def touch_type_id(self) -> int:
        """Return touch type ID."""
        return self._touch_type_id

    @property
    def touch_type(self) -> str:
        """Return touch type."""
        return {
            0: "Hover",
            1: "Down",
            2: "Hold",
            3: "Up",
            4: "Swipe",
        }.get(self._touch_type_id, str(self._touch_type_id))

    @property
    def strength(self) -> int:
        """Return touch strength."""
        return self._strength

    @property
    def panel_id_2(self) -> int | None:
        """Return second panel ID."""
        if self._panel_id_2 == 2 ^ 16:
            return None
        return self._panel_id_2
