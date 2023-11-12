class ReadModelRecordNotFound(Exception):
    def __init__(self, message="Failed to get read model record"):
        self.message = message
        super().__init__(self.message)


class FailedToSaveReadModel(Exception):
    def __init__(self, message="Failed to save read model"):
        self.message = message
        super().__init__(self.message)


class FailedToUpdateReadModel(Exception):
    def __init__(self, message="Failed to update read model"):
        self.message = message
        super().__init__(self.message)
