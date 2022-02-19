"""
Nanoleaf ext control stream
Implementation of the streaming protocol defines here: https://forum.nanoleaf.me/docs#_9gd8j3cnjaju
"""
import asyncio
from asyncio import transports
from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    red: int
    green: int
    blue: int
    white: int  # Note: white is not used

    def encode(self):
        buf = b''
        buf += self.red.to_bytes(1, 'big')
        buf += self.green.to_bytes(1, 'big')
        buf += self.blue.to_bytes(1, 'big')
        buf += self.white.to_bytes(1, 'big')
        return buf


@dataclass(frozen=True)
class Update:
    id: int
    color: Color
    time: int

    def encode(self):
        buf = b''
        buf += self.id.to_bytes(2, 'big')
        buf += self.color.encode()
        buf += self.time.to_bytes(2, 'big')
        return buf


class Stream:
    def __init__(self, transport, protocol):
        self._transport = transport
        self._protocol = protocol
        pass

    async def send_updates(self, updates: list[Update]) -> None:
        buf = b''
        count = len(updates)
        buf += count.to_bytes(2, 'big')
        for upd in updates:
            buf += upd.encode()

        self._transport.sendto(buf)


class _NanoleafStreamProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport: transports.DatagramTransport) -> None:
        print('hey')

    def connection_lost(self, exc) -> None:
        print('oh no')

    def error_received(self, exc: Exception) -> None:
        print('err')

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        print('recv')
