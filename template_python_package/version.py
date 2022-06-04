class Version:
    """ Object represents version """

    def __init__(self) -> None:
        self._major = 0
        self._minor = 0
        self._patch = 1
        self._rc = 0

    @property
    def version(self) -> str:
        """ A string name of version """
        return f"{self._major}.{self._minor}.{self._patch}" + (f"rc{self._rc}" if self._rc > 0 else "")

    def __str__(self) -> str:
        return self.version
