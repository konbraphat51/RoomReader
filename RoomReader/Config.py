from pathlib import Path


class Config:
    def __init__(self) -> None:
        self.library_directory = Path(__file__).parent
        self.data_directory = self.library_directory / Path("Data")
        self.sampledata_directory = self.library_directory / Path("SampleData")
