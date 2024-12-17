from abc import ABC, abstractmethod

import pandas as pd
import yaml  # type: ignore
from torchvision.transforms import Compose

from src.utils import logger_config

# Initialize the logger for the module
logger = logger_config.setup_logger("dataset")


class DataTransformer(ABC):
    @abstractmethod
    def __call__(self, data):
        """
        Abstract method that all derived classes must implement.
        It performs a transformation on the input data.
        """


class ChooseColsTransform(DataTransformer):
    def __init__(self, columns) -> None:
        """
        Initializes the transformer with the columns to select.

        Args:
            columns (list): List of column names to keep.
        """
        self.columns = columns

    def __call__(
        self, data: pd.DataFrame | list[pd.DataFrame]
    ) -> pd.DataFrame | list[pd.DataFrame]:
        """
        Select specific columns from the data.

        Args:
            data (pd.DataFrame): Input DataFrame or list of DataFrames.

        Returns:
            pd.DataFrame or list of pd.DataFrame: DataFrame(s) with only the selected
            columns.
        """
        if isinstance(data, list):
            result = [df[self.columns] for df in data]
            logger.info(f"Selected columns from {len(data)} DataFrames.")
            return result

        result = data[self.columns]
        logger.info("Selected columns from a single DataFrame.")
        return result


class DeleteOutlierInVolume(DataTransformer):
    def __init__(self, volume_threshold) -> None:
        """
        Initializes the transformer with a threshold value.

        Args:
            volume_threshold (float): The threshold for filtering out rows with high
            volumes.
        """
        self.volume_threshold = volume_threshold

    def __call__(
        self, data: pd.DataFrame | list[pd.DataFrame]
    ) -> pd.DataFrame | list[pd.DataFrame]:
        """
        Remove rows where the 'volume' column exceeds the threshold.

        Args:
            data (pd.DataFrame): Input DataFrame or list of DataFrames.

        Returns:
            pd.DataFrame or list of pd.DataFrame: Filtered DataFrame(s).
        """
        if isinstance(data, list):
            result = [df[df["volume"] <= self.volume_threshold] for df in data]
            logger.info(f"Filtered {len(data)} DataFrames.")
            return result

        result = data[data["volume"] <= self.volume_threshold]
        logger.info("Filtered a single DataFrame.")
        return result


class ConcatDataFrames(DataTransformer):
    def __init__(self, join_type) -> None:
        """
        Initializes the transformer with the join type for concatenation.

        Args:
            join_type (str): Type of join operation ('inner', 'outer', etc.).
        """
        self.join_type = join_type

    def __call__(self, data: list[pd.DataFrame]) -> pd.DataFrame:
        """
        Concatenate multiple DataFrames along axis 0 and reset the index.

        Args:
            data (list of pd.DataFrame): List of DataFrames to concatenate.

        Returns:
            pd.DataFrame: A single concatenated DataFrame with reset index.
        """
        logger.info(f"Concatenating DataFrames with join type '{self.join_type}'.")
        result = pd.concat(data, axis=0, join=self.join_type)
        result.reset_index(drop=True, inplace=True)
        logger.info(
            f"Concatenated {len(data)} DataFrames into one DataFrame with"
            f"shape {result.shape}."
        )
        return result


class DataPipeline:
    def __init__(self, config_path):
        """
        Initializes the DataPipeline class, loads the YAML configuration file,
        and builds the data transformation pipeline.

        Args:
            config_path (str): Path to the YAML configuration file.
        """
        self.config_path = config_path
        self.transformations = []
        self.composed_transforms = None
        self._load_config()
        self._build_pipeline()

    def _load_config(self) -> None:
        """
        Internal method: Loads the YAML configuration file.
        """
        with open(self.config_path, "r", encoding="utf-8") as file:
            self.pre_processing_config = yaml.safe_load(file)

    def _build_pipeline(self) -> None:
        """
        Internal method: Builds the data transformation pipeline based on the YAML
        configuration.
        """
        logger.info("Building data transformation pipeline.")
        for step in self.pre_processing_config["pre_processing_steps"]:
            step_name = step["step"]
            params = step["params"]

            if step_name == "choose_columns":
                self.transformations.append(ChooseColsTransform(**params))
            elif step_name == "delete_outlier_in_volume":
                self.transformations.append(DeleteOutlierInVolume(**params))
            elif step_name == "concat_dataframes":
                self.transformations.append(ConcatDataFrames(**params))
            logger.info(f"Added step '{step_name}' to the pipeline.")

        self.composed_transforms = Compose(self.transformations)
        logger.info("Data transformation pipeline built successfully.")

    def apply(self, data):
        """
        Applies all transformation steps from the data pipeline to the input data.

        Args:
            data: Input data, either a DataFrame or a list of DataFrames.

        Returns:
            Transformed data after applying all steps.
        """
        logger.info("Applying the data transformation pipeline.")
        if self.composed_transforms is None:
            raise RuntimeError(
                "The transformation pipeline has not been built successfully."
            )

        result = self.composed_transforms(data)
        logger.info("Data transformation pipeline applied successfully.")
        return result
