from pathlib import Path

class Config:
    def __init__(self) -> None:
        self.data_directory = Path("data")