from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa


class TimeStamp(sa.types.TypeDecorator):
    """
    This class is used to create time stamps for things like when clients submit code during the competiton.
    """
    impl = sa.types.DateTime

    # ensures `value` is converted to UTC before stored in the database
    def process_bind_param(self, value: Optional[datetime], dialect: sa.Dialect):
        if value is None:
            return datetime.utcnow()
        if not value.tzinfo is None:
            return value.astimezone(timezone.utc)

        return value

    # ensures `value`'s timezone' is set to UTC when retrieved from the database
    def process_result_value(self, value: Optional[datetime], dialect: sa.Dialect):
        if value is None:
            return value
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value
