from typing import ClassVar, Optional, NoReturn, Tuple

from requests.models import Response

from .base import BaseManager


class OpenStackSourceManager(BaseManager):
    PATH_fmt: ClassVar[str]
    CREATE_fmt: ClassVar[str]
    API_VERSION: ClassVar[str]

    def create_data(
        self,
        name: str,
        ns: str,
        endpoint: str,
        region: str,
        credentials: dict
    ) -> dict:
        """
        """
    def get(
        self,
        name: str = ...,
        ns: str = ...,
        *,
        raw: Optional[bool] = ...
    ) -> dict | Response:
        """
        """
    def create(
        self,
        name: str,
        ns: str,
        endpoint: str,
        region: str,
        credentials: dict,
        *,
        raw: Optional[bool] = ...
    ) -> dict | Response:
        """
        """
    def update(self, name: str, ns: str, *args, **kwargs) -> NoReturn:
        """
        """
    def delete(self, name: str, ns: str, *, raw: Optional[bool] = ...) -> dict | Response:
        """
        """
    def replace(self, name: str, ns: str, *, raw: Optional[bool] = ...) -> dict | Response:
        """
        """
