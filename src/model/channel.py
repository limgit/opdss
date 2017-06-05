import threading

from typing import Callable

from model.signage import Signage
from utils import utils


class Channel:
    def __init__(self, channel_id: str, description: str, signage: Signage):
        self._id = channel_id
        self._description = description
        self._signage = signage

        self._id_change_handler = lambda channel, old_id: None
        self._value_change_handler = lambda channel: None
        self._redirect_event_handler = lambda channel, old_id: None
        self._count_event_handler = lambda channel: 0

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, new_id: str) -> None:
        utils.validate_id(new_id)

        old_id = self._id
        self._id = new_id

        self._id_change_handler(self, old_id)
        self._value_change_handler(self)
        self._redirect_event_handler(self, old_id)

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_value: str) -> None:
        self._description = new_value

        self._value_change_handler(self)

    @property
    def signage(self) -> Signage:
        return self._signage

    @signage.setter
    def signage(self, new_value: Signage) -> None:
        self._signage = new_value

        self._value_change_handler(self)
        self.request_refresh()

    @property
    def id_change_handler(self) -> Callable[['Channel', str], None]:
        return self._id_change_handler

    @id_change_handler.setter
    def id_change_handler(self, new_handler: Callable[['Channel', str], None]) -> None:
        self._id_change_handler = new_handler

    @property
    def value_change_handler(self) -> Callable[['Channel'], None]:
        return self._value_change_handler

    @value_change_handler.setter
    def value_change_handler(self, new_handler: Callable[['Channel'], None]) -> None:
        self._value_change_handler = new_handler

    @property
    def redirect_event_handler(self) -> Callable[['Channel', str], None]:
        return self._redirect_event_handler

    @redirect_event_handler.setter
    def redirect_event_handler(self, new_handler: Callable[['Channel', str], None]) -> None:
        self._redirect_event_handler = new_handler

    @property
    def count_event_handler(self) -> Callable[['Channel'], int]:
        return self._count_event_handler

    @count_event_handler.setter
    def count_event_handler(self, new_handler: Callable[['Channel'], int]) -> None:
        self._count_event_handler = new_handler

    def request_refresh(self):
        self._redirect_event_handler(self, self.id)

    def request_connection_count(self, callback: Callable[[int], None]):
        def request():
            callback(self._count_event_handler(self))

        threading.Thread(target=request).start()

    def to_dict(self) -> dict:
        return {
            "description": self._description,
            "signage": self._signage.id
        }
