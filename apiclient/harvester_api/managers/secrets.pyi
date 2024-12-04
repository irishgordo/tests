from typing import ClassVar, Optional, NoReturn, Tuple

from requests.models import Response

from .base import BaseManager


class SecretsManager(BaseManager):
    PATH_fmt: ClassVar[str]
    CREATE_fmt: ClassVar[str]
    API_VERSION: ClassVar[str]

    def create_data(
        self,
        name: str,
        namespace: str,
        string_data: dict
    ) -> dict:
        """
        """
    def get(
        self,
        name: str = ...,
        namespace: str = ...,
        *,
        raw: Optional[bool] = ...
    ) -> dict | Response:
        """
        """
    def create(
        self,
        name: str,
        namespace: str = ...,
        string_data: str = ...,
        *,
        raw: Optional[bool] = ...
    ) -> dict | Response:
        """
        """
    def update(self, *args, **kwargs) -> NoReturn:
        """
        """
    def delete(self, name: str, namespace: str, *, raw: Optional[bool] = ...) -> dict | Response:
        """
        """
    def replace(self, uid: str, *, raw: Optional[bool] = ...) -> dict | Response:
        """
        """
