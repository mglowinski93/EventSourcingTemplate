class StatusCantBeChanged(Exception):
    def __init__(self, old_status: str, new_status: str):
        super().__init__(f"Status can't be changed from {old_status} to {new_status}.")
