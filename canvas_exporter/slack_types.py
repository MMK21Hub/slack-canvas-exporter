from typing import Annotated
from pydantic import Field


ChannelId = Annotated[str, Field(pattern=r"^C[A-Z0-9]{8,}$")]
FileId = Annotated[str, Field(pattern=r"^F[A-Z0-9]{8,}$")]
CanvasId = FileId
