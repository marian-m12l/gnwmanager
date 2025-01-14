from enum import Enum

from pyocd.flash.eraser import FlashEraser
from typer import Argument
from typing_extensions import Annotated


class EraseLocation(str, Enum):
    bank1 = "bank1"
    bank2 = "bank2"
    ext = "ext"
    all = "all"


def erase(
    location: Annotated[EraseLocation, Argument(case_sensitive=False, help="Section to erase.")],
):
    """Erase a section of flash."""
    from .main import session

    target = session.target

    location = location.value

    if location in ("ext", "all"):
        # Just setting an artibrarily long timeout
        # TODO: maybe add visualization callback
        target.erase_ext(0, 0, whole_chip=True, timeout=10_000)

    if location in ("bank1", "all"):
        target.erase_int(1, 0, 256 << 10)

    if location in ("bank2", "all"):
        target.erase_int(2, 0, 256 << 10)
