import datetime as dt
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import mapped_column

created_at = Annotated[dt.datetime, mapped_column(server_default=func.current_timestamp())]
