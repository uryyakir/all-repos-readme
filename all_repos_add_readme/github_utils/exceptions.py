class InvalidReadme(BaseException):
    def __init__(self) -> None:
        super(InvalidReadme, self).__init__("invalid mark-down file or mark-down string")
