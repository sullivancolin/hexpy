"""Module for working with Monitor Project"""

import inspect
from enum import Enum
from functools import partial, wraps
from typing import Any, Callable, List, Optional, Union

import pendulum
from pydantic import BaseModel, Extra, validator

from .base import JSONDict
from .models import GenderEnum
from .monitor import MonitorAPI
from .session import HexpySession


def substitute_default(
    func: Callable[..., JSONDict], monitor_id: int, start: str, end: str
) -> Callable[..., JSONDict]:
    """Substitute function with default arguments"""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> JSONDict:
        """Wrap function."""
        return func(monitor_id=monitor_id, start=start, end=end, *args, **kwargs)

    return wrapper


class MonitorTypeEnum(str, Enum):
    """Valid values for Monitor Type"""

    BUZZ = "BUZZ"
    OPINION = "OPINION"
    SOCIAL = "SOCIAL"


class Project(BaseModel):
    """Class for working with a Crimson Hexagon Monitor Project.

    # Example usage.

    ```python
    >>> from hexpy import HexpySession, Project
    >>> session = HexpySession.load_auth_from_file()
    >>> project = Project.get_from_monitor_id(session, monitor_id=123456789)
    >>> description = project.description
    >>> start = project.resultsStart
    >>> end = project.resultsEnd
    >>> sample_posts = project.posts()
    ```
    """

    id: int
    name: str
    description: str
    type: MonitorTypeEnum
    enabled: bool
    resultsStart: pendulum.DateTime
    resultsEnd: pendulum.DateTime
    keywords: str
    languages: JSONDict
    geolocations: JSONDict
    gender: Optional[GenderEnum] = None
    sources: List[str]
    timezone: str
    teamName: str
    tags: List[str]
    subfilters: List[JSONDict]
    categories: List[JSONDict]
    emotions: List[JSONDict]
    session: HexpySession

    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True

    @validator("gender", pre=True)
    def validate_empty_gender(cls, value: Optional[str]) -> Union[str, None]:
        """Validate empty string is None"""
        if value:
            return value
        else:
            return None

    @classmethod
    def get_from_monitor_id(cls, session: HexpySession, monitor_id: int) -> "Project":
        """Instantiate from session and Monitor ID"""
        client = MonitorAPI(session)
        details = client.details(monitor_id)
        details["session"] = session

        return cls(**details)

    def __init__(self, **data: Any):
        super().__init__(**data)
        client = MonitorAPI(self.session)
        self.days = [
            day.to_date_string()
            for day in pendulum.period(self.resultsStart, self.resultsEnd).range("days")
        ]

        for name, fn in inspect.getmembers(client, inspect.isfunction):

            args_spec = inspect.signature(fn)
            args = args_spec.parameters.keys()
            if "monitor_id" in args and "start" in args and "end" in args:
                if name != "gender":
                    setattr(
                        self,
                        name,
                        substitute_default(
                            fn,
                            monitor_id=self.id,
                            start=self.days[0],
                            end=self.days[-1],
                        ),
                    )
                else:
                    setattr(
                        self,
                        "monitor_" + name,
                        substitute_default(
                            fn,
                            monitor_id=self.id,
                            start=self.days[0],
                            end=self.days[-1],
                        ),
                    )
            elif "monitor_id" in args:
                setattr(self, name, partial(fn, monitor_id=self.id))

            else:
                setattr(self, name, fn)

    def __len__(self) -> int:
        return len(self.days)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Project ('{self.name}', {self.resultsStart} ,{self.resultsEnd})>"

    def __iter__(self):  # type: ignore
        for day in self.days:
            yield day

    def __getitem__(self, index):  # type: ignore
        days = self.days[index]
        return days
