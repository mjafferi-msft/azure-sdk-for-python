# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from abc import ABC
from typing import Dict, Optional, Union

from azure.ai.ml._restclient.v2023_04_01_preview.models import LogVerbosity, SamplingAlgorithmType
from azure.ai.ml._utils.utils import camel_to_snake
from azure.ai.ml.entities._inputs_outputs import Input
from azure.ai.ml.entities._job.automl.automl_vertical import AutoMLVertical
from azure.ai.ml.entities._job.automl.image.image_limit_settings import ImageLimitSettings
from azure.ai.ml.entities._job.automl.image.image_sweep_settings import ImageSweepSettings
from azure.ai.ml.entities._job.sweep.early_termination_policy import (
    BanditPolicy,
    MedianStoppingPolicy,
    TruncationSelectionPolicy,
)
from azure.ai.ml.exceptions import ErrorCategory, ErrorTarget, ValidationException


class AutoMLImage(AutoMLVertical, ABC):
    """Base class for all AutoML Image jobs.
    You should not instantiate this class directly.
    Instead you should create classes for specific AutoML Image tasks.

    :keyword task_type: Required. Type of task to run.
    Possible values include: "ImageClassification", "ImageClassificationMultilabel",
                              "ImageObjectDetection", "ImageInstanceSegmentation"
    :paramtype task_type: str
    :keyword limits: Limit settings for all AutoML Image jobs. Defaults to None.
    :paramtype limits: Optional[~azure.ai.ml.automl.ImageLimitSettings]
    :keyword sweep: Sweep settings for all AutoML Image jobs. Defaults to None.
    :paramtype sweep: Optional[~azure.ai.ml.automl.ImageSweepSettings]
    :keyword kwargs: Additional keyword arguments for AutoMLImage.
    :paramtype kwargs: Dict[str, Any]
    """

    def __init__(
        self,
        *,
        task_type: str,
        limits: Optional[ImageLimitSettings] = None,
        sweep: Optional[ImageSweepSettings] = None,
        **kwargs,
    ) -> None:
        self.log_verbosity = kwargs.pop("log_verbosity", LogVerbosity.INFO)
        self.target_column_name = kwargs.pop("target_column_name", None)
        self.validation_data_size = kwargs.pop("validation_data_size", None)

        super().__init__(
            task_type=task_type,
            training_data=kwargs.pop("training_data", None),
            validation_data=kwargs.pop("validation_data", None),
            **kwargs,
        )

        # Set default value for self._limits as it is a required property in rest object.
        self._limits = limits or ImageLimitSettings()
        self._sweep = sweep

    @property
    def log_verbosity(self) -> LogVerbosity:
        """Returns the verbosity of the logger.

        :return: The log verbosity.
        :rtype: ~azure.ai.ml._restclient.v2023_04_01_preview.models.LogVerbosity
        """
        return self._log_verbosity

    @log_verbosity.setter
    def log_verbosity(self, value: Union[str, LogVerbosity]):
        """Sets the verbosity of the logger.

        :param value: The value to set the log verbosity to.
                      Possible values include: "NotSet", "Debug", "Info", "Warning", "Error", "Critical".
        :type value: Union[str, ~azure.ai.ml._restclient.v2023_04_01_preview.models.LogVerbosity]
        """
        self._log_verbosity = None if value is None else LogVerbosity[camel_to_snake(value).upper()]

    @property
    def limits(self) -> ImageLimitSettings:
        """Returns the limit settings for all AutoML Image jobs.

        :return: The limit settings.
        :rtype: ~azure.ai.ml.automl.ImageLimitSettings
        """
        return self._limits

    @limits.setter
    def limits(self, value: Union[Dict, ImageLimitSettings]) -> None:
        if isinstance(value, ImageLimitSettings):
            self._limits = value
        else:
            if not isinstance(value, dict):
                msg = "Expected a dictionary for limit settings."
                raise ValidationException(
                    message=msg,
                    no_personal_data_message=msg,
                    target=ErrorTarget.AUTOML,
                    error_category=ErrorCategory.USER_ERROR,
                )
            self.set_limits(**value)

    @property
    def sweep(self) -> ImageSweepSettings:
        """Returns the sweep settings for all AutoML Image jobs.

        :return: The sweep settings.
        :rtype: ~azure.ai.ml.automl.ImageSweepSettings
        """
        return self._sweep

    @sweep.setter
    def sweep(self, value: Union[Dict, ImageSweepSettings]) -> None:
        """Sets the sweep settings for all AutoML Image jobs.

        :param value: The value to set the sweep settings to.
        :type value: Union[Dict, ~azure.ai.ml.automl.ImageSweepSettings]
        :raises ~azure.ai.ml.exceptions.ValidationException: If value is not a dictionary.
        :return: None
        """
        if isinstance(value, ImageSweepSettings):
            self._sweep = value
        else:
            if not isinstance(value, dict):
                msg = "Expected a dictionary for sweep settings."
                raise ValidationException(
                    message=msg,
                    no_personal_data_message=msg,
                    target=ErrorTarget.AUTOML,
                    error_category=ErrorCategory.USER_ERROR,
                )
            self.set_sweep(**value)

    def set_data(
        self,
        *,
        training_data: Input,
        target_column_name: str,
        validation_data: Optional[Input] = None,
        validation_data_size: Optional[float] = None,
    ) -> None:
        """Data settings for all AutoML Image jobs.

        :keyword training_data: Required. Training data.
        :type training_data: ~azure.ai.ml.entities.Input
        :keyword target_column_name: Required. Target column name.
        :type target_column_name: str
        :keyword validation_data: Optional. Validation data.
        :type validation_data: Optional[~azure.ai.ml.entities.Input]
        :keyword validation_data_size: Optional. The fraction of training dataset that needs to be set aside for
                                      validation purpose. Values should be in range (0.0 , 1.0).
                                      Applied only when validation dataset is not provided.
        :type validation_data_size: Optional[float]
        :return: None
        """
        self.target_column_name = self.target_column_name if target_column_name is None else target_column_name
        self.training_data = self.training_data if training_data is None else training_data
        self.validation_data = self.validation_data if validation_data is None else validation_data
        self.validation_data_size = self.validation_data_size if validation_data_size is None else validation_data_size

    def set_limits(
        self,
        *,
        max_concurrent_trials: Optional[int] = None,
        max_trials: Optional[int] = None,
        timeout_minutes: Optional[int] = None,
    ) -> None:
        """Limit settings for all AutoML Image Jobs.

        :keyword max_concurrent_trials: Maximum number of trials to run concurrently.
        :type max_concurrent_trials: Optional[int]. Defaults to None.
        :keyword max_trials: Maximum number of trials to run. Defaults to None.
        :type max_trials: Optional[int]
        :keyword timeout_minutes: AutoML job timeout.
        :type timeout_minutes: ~datetime.timedelta
        :return: None
        """
        self._limits = self._limits or ImageLimitSettings()
        self._limits.max_concurrent_trials = (
            max_concurrent_trials if max_concurrent_trials is not None else self._limits.max_concurrent_trials
        )
        self._limits.max_trials = max_trials if max_trials is not None else self._limits.max_trials
        self._limits.timeout_minutes = timeout_minutes if timeout_minutes is not None else self._limits.timeout_minutes

    def set_sweep(
        self,
        *,
        sampling_algorithm: Union[
            str, SamplingAlgorithmType.RANDOM, SamplingAlgorithmType.GRID, SamplingAlgorithmType.BAYESIAN
        ],
        early_termination: Optional[Union[BanditPolicy, MedianStoppingPolicy, TruncationSelectionPolicy]] = None,
    ) -> None:
        """Sweep settings for all AutoML Image jobs.

        :keyword sampling_algorithm: Required. Type of the hyperparameter sampling
            algorithms. Possible values include: "Grid", "Random", "Bayesian".
        :type sampling_algorithm: Union[str, ~azure.mgmt.machinelearningservices.models.SamplingAlgorithmType.RANDOM,
            ~azure.mgmt.machinelearningservices.models.SamplingAlgorithmType.GRID,
            ~azure.mgmt.machinelearningservices.models.SamplingAlgorithmType.BAYESIAN]
        :keyword early_termination: Type of early termination policy.
        :type early_termination: Union[
            ~azure.mgmt.machinelearningservices.models.BanditPolicy,
            ~azure.mgmt.machinelearningservices.models.MedianStoppingPolicy,
            ~azure.mgmt.machinelearningservices.models.TruncationSelectionPolicy]
        :return: None
        """
        if self._sweep:
            self._sweep.sampling_algorithm = sampling_algorithm
        else:
            self._sweep = ImageSweepSettings(sampling_algorithm=sampling_algorithm)

        self._sweep.early_termination = early_termination or self._sweep.early_termination

    def __eq__(self, other) -> bool:
        """Compares two AutoMLImage objects for equality.

        :param other: The other AutoMLImage object to compare to.
        :type other: ~azure.ai.ml.automl.AutoMLImage
        :return: True if the two AutoMLImage objects are equal; False otherwise.
        :rtype: bool
        """
        if not isinstance(other, AutoMLImage):
            return NotImplemented

        return (
            self.target_column_name == other.target_column_name
            and self.training_data == other.training_data
            and self.validation_data == other.validation_data
            and self.validation_data_size == other.validation_data_size
            and self._limits == other._limits
            and self._sweep == other._sweep
        )

    def __ne__(self, other) -> bool:
        """Compares two AutoMLImage objects for inequality.

        :param other: The other AutoMLImage object to compare to.
        :type other: ~azure.ai.ml.automl.AutoMLImage
        :return: True if the two AutoMLImage objects are not equal; False otherwise.
        :rtype: bool
        """
        return not self.__eq__(other)
