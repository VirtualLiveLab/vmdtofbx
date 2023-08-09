from datetime import UTC, datetime, timedelta, tzinfo


class JST(tzinfo):
    def __repr__(self) -> str:
        return self.tzname()

    def utcoffset(self, dt: datetime | None = None) -> timedelta:  # noqa: ARG002
        # ローカル時刻とUTCの差分に等しいtimedeltaを返す
        return timedelta(hours=9)

    def tzname(self, dt: datetime | None = None) -> str:  # noqa: ARG002
        # タイムゾーン名を返す
        return "Asia/Tokyo"

    def dst(self, dt: datetime | None = None) -> timedelta:  # noqa: ARG002
        # 夏時間を返す。有効でない場合はtimedelta(0)を返す
        return timedelta(0)


class TimeUtils:
    @classmethod
    def get_now(cls, timezone: tzinfo = UTC) -> datetime:
        """get current datetime object in specific timezone.
        default is UTC.

        Returns:
            datetime: [:class:`datetime.datetime`]
        """
        return datetime.now(timezone)

    @classmethod
    def get_now_jst(cls) -> datetime:
        """get current datetime object in JST.

        Returns:
            datetime: [:class:`datetime.datetime`]
        """
        return cls.get_now(JST())

    @classmethod
    def dt_to_str(cls, datetime: datetime | None = None, date_format: str = "%Y.%m.%d %H:%M:%S") -> str:
        """convert datetime object to string.

        Args:
            datetime (datetime, optional): a datetime object. Defaults to datetime.now(JST()).
            if there is no tzinfo, this function will replace with UTC timezone.
            format (str, optional): a format used in strfttime(). Defaults to "%Y/%m/%d %H:%M:%S".

        Returns:
            str: converted string.
        """
        if datetime is None:
            datetime = cls.get_now_jst()

        if not datetime.tzinfo:
            datetime.replace(tzinfo=UTC)
        if datetime.tzinfo != JST:
            datetime = datetime.astimezone(JST())
        return datetime.strftime(date_format)

    @classmethod
    def str_to_dt(
        cls,
        string: str,
        /,
        *,
        timezone: tzinfo = UTC,
        date_format: str = "%Y.%m.%d %H:%M:%S",
    ) -> datetime:
        """convert string to datetime object.

        Args:
            string (str): a string to convert.
            timezone (timezone): a timezone object.
            format (str, optional): a format used in strptime(). Defaults to "%Y/%m/%d %H:%M:%S".

        Returns:
            datetime: converted datetime object. If there is no tzinfo, this function will replace it with UTC timezone.
        """
        return datetime.strptime(string, date_format).replace(tzinfo=timezone)
