# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import TYPE_CHECKING
import warnings

from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.paging import ItemPaged
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpRequest, HttpResponse
from azure.core.polling import LROPoller, NoPolling, PollingMethod
from azure.mgmt.core.exceptions import ARMErrorFormat
from azure.mgmt.core.polling.arm_polling import ARMPolling

from .. import models as _models

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Generic, Iterable, Optional, TypeVar, Union

    T = TypeVar('T')
    ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

class RegistriesOperations(object):
    """RegistriesOperations operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~azure.mgmt.containerregistry.v2017_03_01.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = _models

    def __init__(self, client, config, serializer, deserializer):
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    def check_name_availability(
        self,
        registry_name_check_request,  # type: "_models.RegistryNameCheckRequest"
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.RegistryNameStatus"
        """Checks whether the container registry name is available for use. The name must contain only
        alphanumeric characters, be globally unique, and between 5 and 50 characters in length.

        :param registry_name_check_request: The object containing information for the availability
         request.
        :type registry_name_check_request: ~azure.mgmt.containerregistry.v2017_03_01.models.RegistryNameCheckRequest
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: RegistryNameStatus, or the result of cls(response)
        :rtype: ~azure.mgmt.containerregistry.v2017_03_01.models.RegistryNameStatus
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.RegistryNameStatus"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2017-03-01"
        content_type = kwargs.pop("content_type", "application/json")
        accept = "application/json"

        # Construct URL
        url = self.check_name_availability.metadata['url']  # type: ignore
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        body_content_kwargs = {}  # type: Dict[str, Any]
        body_content = self._serialize.body(registry_name_check_request, 'RegistryNameCheckRequest')
        body_content_kwargs['content'] = body_content
        request = self._client.post(url, query_parameters, header_parameters, **body_content_kwargs)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('RegistryNameStatus', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    check_name_availability.metadata = {'url': '/subscriptions/{subscriptionId}/providers/Microsoft.ContainerRegistry/checkNameAvailability'}  # type: ignore

    def get(
        self,
        resource_group_name,  # type: str
        registry_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.Registry"
        """Gets the properties of the specified container registry.

        :param resource_group_name: The name of the resource group to which the container registry
         belongs.
        :type resource_group_name: str
        :param registry_name: The name of the container registry.
        :type registry_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Registry, or the result of cls(response)
        :rtype: ~azure.mgmt.containerregistry.v2017_03_01.models.Registry
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.Registry"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2017-03-01"
        accept = "application/json"

        # Construct URL
        url = self.get.metadata['url']  # type: ignore
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', min_length=1),
            'registryName': self._serialize.url("registry_name", registry_name, 'str', max_length=50, min_length=5, pattern=r'^[a-zA-Z0-9]*$'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        request = self._client.get(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('Registry', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    get.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerRegistry/registries/{registryName}'}  # type: ignore

    def _create_initial(
        self,
        resource_group_name,  # type: str
        registry_name,  # type: str
        registry_create_parameters,  # type: "_models.RegistryCreateParameters"
        **kwargs  # type: Any
    ):
        # type: (...) -> Optional["_models.Registry"]
        cls = kwargs.pop('cls', None)  # type: ClsType[Optional["_models.Registry"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2017-03-01"
        content_type = kwargs.pop("content_type", "application/json")
        accept = "application/json"

        # Construct URL
        url = self._create_initial.metadata['url']  # type: ignore
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', min_length=1),
            'registryName': self._serialize.url("registry_name", registry_name, 'str', max_length=50, min_length=5, pattern=r'^[a-zA-Z0-9]*$'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        body_content_kwargs = {}  # type: Dict[str, Any]
        body_content = self._serialize.body(registry_create_parameters, 'RegistryCreateParameters')
        body_content_kwargs['content'] = body_content
        request = self._client.put(url, query_parameters, header_parameters, **body_content_kwargs)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 202]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = None
        if response.status_code == 200:
            deserialized = self._deserialize('Registry', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    _create_initial.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerRegistry/registries/{registryName}'}  # type: ignore

    def begin_create(
        self,
        resource_group_name,  # type: str
        registry_name,  # type: str
        registry_create_parameters,  # type: "_models.RegistryCreateParameters"
        **kwargs  # type: Any
    ):
        # type: (...) -> LROPoller["_models.Registry"]
        """Creates a container registry with the specified parameters.

        :param resource_group_name: The name of the resource group to which the container registry
         belongs.
        :type resource_group_name: str
        :param registry_name: The name of the container registry.
        :type registry_name: str
        :param registry_create_parameters: The parameters for creating a container registry.
        :type registry_create_parameters: ~azure.mgmt.containerregistry.v2017_03_01.models.RegistryCreateParameters
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be ARMPolling.
         Pass in False for this operation to not poll, or pass in your own initialized polling object for a personal polling strategy.
        :paramtype polling: bool or ~azure.core.polling.PollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no Retry-After header is present.
        :return: An instance of LROPoller that returns either Registry or the result of cls(response)
        :rtype: ~azure.core.polling.LROPoller[~azure.mgmt.containerregistry.v2017_03_01.models.Registry]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        polling = kwargs.pop('polling', True)  # type: Union[bool, PollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.Registry"]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = self._create_initial(
                resource_group_name=resource_group_name,
                registry_name=registry_name,
                registry_create_parameters=registry_create_parameters,
                cls=lambda x,y,z: x,
                **kwargs
            )

        kwargs.pop('error_map', None)
        kwargs.pop('content_type', None)

        def get_long_running_output(pipeline_response):
            deserialized = self._deserialize('Registry', pipeline_response)

            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized

        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', min_length=1),
            'registryName': self._serialize.url("registry_name", registry_name, 'str', max_length=50, min_length=5, pattern=r'^[a-zA-Z0-9]*$'),
        }

        if polling is True: polling_method = ARMPolling(lro_delay, path_format_arguments=path_format_arguments,  **kwargs)
        elif polling is False: polling_method = NoPolling()
        else: polling_method = polling
        if cont_token:
            return LROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        else:
            return LROPoller(self._client, raw_result, get_long_running_output, polling_method)
    begin_create.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerRegistry/registries/{registryName}'}  # type: ignore

    def delete(
        self,
        resource_group_name,  # type: str
        registry_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        """Deletes a container registry.

        :param resource_group_name: The name of the resource group to which the container registry
         belongs.
        :type resource_group_name: str
        :param registry_name: The name of the container registry.
        :type registry_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2017-03-01"

        # Construct URL
        url = self.delete.metadata['url']  # type: ignore
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', min_length=1),
            'registryName': self._serialize.url("registry_name", registry_name, 'str', max_length=50, min_length=5, pattern=r'^[a-zA-Z0-9]*$'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]

        request = self._client.delete(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if cls:
            return cls(pipeline_response, None, {})

    delete.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerRegistry/registries/{registryName}'}  # type: ignore

    def update(
        self,
        resource_group_name,  # type: str
        registry_name,  # type: str
        registry_update_parameters,  # type: "_models.RegistryUpdateParameters"
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.Registry"
        """Updates a container registry with the specified parameters.

        :param resource_group_name: The name of the resource group to which the container registry
         belongs.
        :type resource_group_name: str
        :param registry_name: The name of the container registry.
        :type registry_name: str
        :param registry_update_parameters: The parameters for updating a container registry.
        :type registry_update_parameters: ~azure.mgmt.containerregistry.v2017_03_01.models.RegistryUpdateParameters
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Registry, or the result of cls(response)
        :rtype: ~azure.mgmt.containerregistry.v2017_03_01.models.Registry
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.Registry"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2017-03-01"
        content_type = kwargs.pop("content_type", "application/json")
        accept = "application/json"

        # Construct URL
        url = self.update.metadata['url']  # type: ignore
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', min_length=1),
            'registryName': self._serialize.url("registry_name", registry_name, 'str', max_length=50, min_length=5, pattern=r'^[a-zA-Z0-9]*$'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        body_content_kwargs = {}  # type: Dict[str, Any]
        body_content = self._serialize.body(registry_update_parameters, 'RegistryUpdateParameters')
        body_content_kwargs['content'] = body_content
        request = self._client.patch(url, query_parameters, header_parameters, **body_content_kwargs)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('Registry', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    update.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerRegistry/registries/{registryName}'}  # type: ignore

    def list_by_resource_group(
        self,
        resource_group_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> Iterable["_models.RegistryListResult"]
        """Lists all the container registries under the specified resource group.

        :param resource_group_name: The name of the resource group to which the container registry
         belongs.
        :type resource_group_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either RegistryListResult or the result of cls(response)
        :rtype: ~azure.core.paging.ItemPaged[~azure.mgmt.containerregistry.v2017_03_01.models.RegistryListResult]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.RegistryListResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2017-03-01"
        accept = "application/json"

        def prepare_request(next_link=None):
            # Construct headers
            header_parameters = {}  # type: Dict[str, Any]
            header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

            if not next_link:
                # Construct URL
                url = self.list_by_resource_group.metadata['url']  # type: ignore
                path_format_arguments = {
                    'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
                    'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', min_length=1),
                }
                url = self._client.format_url(url, **path_format_arguments)
                # Construct parameters
                query_parameters = {}  # type: Dict[str, Any]
                query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

                request = self._client.get(url, query_parameters, header_parameters)
            else:
                url = next_link
                query_parameters = {}  # type: Dict[str, Any]
                request = self._client.get(url, query_parameters, header_parameters)
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize('RegistryListResult', pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response

        return ItemPaged(
            get_next, extract_data
        )
    list_by_resource_group.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerRegistry/registries'}  # type: ignore

    def list(
        self,
        **kwargs  # type: Any
    ):
        # type: (...) -> Iterable["_models.RegistryListResult"]
        """Lists all the container registries under the specified subscription.

        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either RegistryListResult or the result of cls(response)
        :rtype: ~azure.core.paging.ItemPaged[~azure.mgmt.containerregistry.v2017_03_01.models.RegistryListResult]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.RegistryListResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2017-03-01"
        accept = "application/json"

        def prepare_request(next_link=None):
            # Construct headers
            header_parameters = {}  # type: Dict[str, Any]
            header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

            if not next_link:
                # Construct URL
                url = self.list.metadata['url']  # type: ignore
                path_format_arguments = {
                    'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
                }
                url = self._client.format_url(url, **path_format_arguments)
                # Construct parameters
                query_parameters = {}  # type: Dict[str, Any]
                query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

                request = self._client.get(url, query_parameters, header_parameters)
            else:
                url = next_link
                query_parameters = {}  # type: Dict[str, Any]
                request = self._client.get(url, query_parameters, header_parameters)
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize('RegistryListResult', pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response

        return ItemPaged(
            get_next, extract_data
        )
    list.metadata = {'url': '/subscriptions/{subscriptionId}/providers/Microsoft.ContainerRegistry/registries'}  # type: ignore

    def list_credentials(
        self,
        resource_group_name,  # type: str
        registry_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.RegistryListCredentialsResult"
        """Lists the login credentials for the specified container registry.

        :param resource_group_name: The name of the resource group to which the container registry
         belongs.
        :type resource_group_name: str
        :param registry_name: The name of the container registry.
        :type registry_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: RegistryListCredentialsResult, or the result of cls(response)
        :rtype: ~azure.mgmt.containerregistry.v2017_03_01.models.RegistryListCredentialsResult
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.RegistryListCredentialsResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2017-03-01"
        accept = "application/json"

        # Construct URL
        url = self.list_credentials.metadata['url']  # type: ignore
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', min_length=1),
            'registryName': self._serialize.url("registry_name", registry_name, 'str', max_length=50, min_length=5, pattern=r'^[a-zA-Z0-9]*$'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        request = self._client.post(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('RegistryListCredentialsResult', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    list_credentials.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerRegistry/registries/{registryName}/listCredentials'}  # type: ignore

    def regenerate_credential(
        self,
        resource_group_name,  # type: str
        registry_name,  # type: str
        regenerate_credential_parameters,  # type: "_models.RegenerateCredentialParameters"
        **kwargs  # type: Any
    ):
        # type: (...) -> "_models.RegistryListCredentialsResult"
        """Regenerates one of the login credentials for the specified container registry.

        :param resource_group_name: The name of the resource group to which the container registry
         belongs.
        :type resource_group_name: str
        :param registry_name: The name of the container registry.
        :type registry_name: str
        :param regenerate_credential_parameters: Specifies name of the password which should be
         regenerated -- password or password2.
        :type regenerate_credential_parameters: ~azure.mgmt.containerregistry.v2017_03_01.models.RegenerateCredentialParameters
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: RegistryListCredentialsResult, or the result of cls(response)
        :rtype: ~azure.mgmt.containerregistry.v2017_03_01.models.RegistryListCredentialsResult
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.RegistryListCredentialsResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2017-03-01"
        content_type = kwargs.pop("content_type", "application/json")
        accept = "application/json"

        # Construct URL
        url = self.regenerate_credential.metadata['url']  # type: ignore
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', min_length=1),
            'registryName': self._serialize.url("registry_name", registry_name, 'str', max_length=50, min_length=5, pattern=r'^[a-zA-Z0-9]*$'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = self._serialize.header("accept", accept, 'str')

        body_content_kwargs = {}  # type: Dict[str, Any]
        body_content = self._serialize.body(regenerate_credential_parameters, 'RegenerateCredentialParameters')
        body_content_kwargs['content'] = body_content
        request = self._client.post(url, query_parameters, header_parameters, **body_content_kwargs)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('RegistryListCredentialsResult', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    regenerate_credential.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ContainerRegistry/registries/{registryName}/regenerateCredential'}  # type: ignore
