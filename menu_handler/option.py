class Option:
    """
    Selectable Menu option

    @:param id: string
    """

    def __init__(self, id="default", description=None, payload=None):
        self.id = id
        self.__description = description
        self.__payload = payload

    def get_id(self):
        return self.id

    def get_payload(self):
        return self.__payload

    def select(self):
        return self

    def __str__(self):
        return f'{self.id}{" - " + self.__description if self.__description else ""}'
