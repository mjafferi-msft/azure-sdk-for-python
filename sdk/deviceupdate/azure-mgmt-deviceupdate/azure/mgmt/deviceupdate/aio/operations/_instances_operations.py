# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from io import IOBase
from typing import Any, AsyncIterable, Callable, Dict, IO, Optional, TypeVar, Union, cast, overload
import urllib.parse

from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.polling import AsyncLROPoller, AsyncNoPolling, AsyncPollingMethod
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat
from azure.mgmt.core.polling.async_arm_polling import AsyncARMPolling

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._instances_operations import (
    build_create_request,
    build_delete_request,
    build_get_request,
    build_head_request,
    build_list_by_account_request,
    build_update_request,
)
from .._vendor import DeviceUpdateMgmtClientMixinABC

T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class InstancesOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.deviceupdate.aio.DeviceUpdateMgmtClient`'s
        :attr:`instances` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace
    def list_by_account(
        self, resource_group_name: str, account_name: str, **kwargs: Any
    ) -> AsyncIterable["_models.Instance"]:
        """Returns instances for the given account name.

        :param resource_group_name: The resource group name. Required.
        :type resource_group_name: str
        :param account_name: Account name. Required.
        :type account_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either Instance or the result of cls(response)
        :rtype: ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.deviceupdate.models.Instance]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[_models.InstanceList] = kwargs.pop("cls", None)

        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        def prepare_request(next_link=None):
            if not next_link:

                request = build_list_by_account_request(
                    resource_group_name=resource_group_name,
                    account_name=account_name,
                    subscription_id=self._config.subscription_id,
                    api_version=api_version,
                    template_url=self.list_by_account.metadata["url"],
                    headers=_headers,
                    params=_params,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)

            else:
                # make call to next link with the client's api-version
                _parsed_next_link = urllib.parse.urlparse(next_link)
                _next_request_params = case_insensitive_dict(
                    {
                        key: [urllib.parse.quote(v) for v in value]
                        for key, value in urllib.parse.parse_qs(_parsed_next_link.query).items()
                    }
                )
                _next_request_params["api-version"] = self._config.api_version
                request = HttpRequest(
                    "GET", urllib.parse.urljoin(next_link, _parsed_next_link.path), params=_next_request_params
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("InstanceList", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)  # type: ignore
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            _stream = False
            pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
                request, stream=_stream, **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response

        return AsyncItemPaged(get_next, extract_data)

    list_by_account.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DeviceUpdate/accounts/{accountName}/instances"
    }

    @distributed_trace_async
    async def get(
        self, resource_group_name: str, account_name: str, instance_name: str, **kwargs: Any
    ) -> _models.Instance:
        """Returns instance details for the given instance and account name.

        :param resource_group_name: The resource group name. Required.
        :type resource_group_name: str
        :param account_name: Account name. Required.
        :type account_name: str
        :param instance_name: Instance name. Required.
        :type instance_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Instance or the result of cls(response)
        :rtype: ~azure.mgmt.deviceupdate.models.Instance
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[_models.Instance] = kwargs.pop("cls", None)

        request = build_get_request(
            resource_group_name=resource_group_name,
            account_name=account_name,
            instance_name=instance_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self.get.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("Instance", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DeviceUpdate/accounts/{accountName}/instances/{instanceName}"
    }

    @distributed_trace_async
    async def head(self, resource_group_name: str, account_name: str, instance_name: str, **kwargs: Any) -> bool:
        """Checks whether instance exists.

        :param resource_group_name: The resource group name. Required.
        :type resource_group_name: str
        :param account_name: Account name. Required.
        :type account_name: str
        :param instance_name: Instance name. Required.
        :type instance_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: bool or the result of cls(response)
        :rtype: bool
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[None] = kwargs.pop("cls", None)

        request = build_head_request(
            resource_group_name=resource_group_name,
            account_name=account_name,
            instance_name=instance_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self.head.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        if cls:
            return cls(pipeline_response, None, {})
        return 200 <= response.status_code <= 299

    head.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DeviceUpdate/accounts/{accountName}/instances/{instanceName}"
    }

    async def _create_initial(
        self,
        resource_group_name: str,
        account_name: str,
        instance_name: str,
        instance: Union[_models.Instance, IO],
        **kwargs: Any
    ) -> _models.Instance:
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.Instance] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(instance, (IOBase, bytes)):
            _content = instance
        else:
            _json = self._serialize.body(instance, "Instance")

        request = build_create_request(
            resource_group_name=resource_group_name,
            account_name=account_name,
            instance_name=instance_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            template_url=self._create_initial.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("Instance", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    _create_initial.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DeviceUpdate/accounts/{accountName}/instances/{instanceName}"
    }

    @overload
    async def begin_create(
        self,
        resource_group_name: str,
        account_name: str,
        instance_name: str,
        instance: _models.Instance,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> AsyncLROPoller[_models.Instance]:
        """Creates or updates instance.

        :param resource_group_name: The resource group name. Required.
        :type resource_group_name: str
        :param account_name: Account name. Required.
        :type account_name: str
        :param instance_name: Instance name. Required.
        :type instance_name: str
        :param instance: Instance details. Required.
        :type instance: ~azure.mgmt.deviceupdate.models.Instance
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncARMPolling. Pass in False for
         this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either Instance or the result of
         cls(response)
        :rtype: ~azure.core.polling.AsyncLROPoller[~azure.mgmt.deviceupdate.models.Instance]
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def begin_create(
        self,
        resource_group_name: str,
        account_name: str,
        instance_name: str,
        instance: IO,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> AsyncLROPoller[_models.Instance]:
        """Creates or updates instance.

        :param resource_group_name: The resource group name. Required.
        :type resource_group_name: str
        :param account_name: Account name. Required.
        :type account_name: str
        :param instance_name: Instance name. Required.
        :type instance_name: str
        :param instance: Instance details. Required.
        :type instance: IO
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncARMPolling. Pass in False for
         this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either Instance or the result of
         cls(response)
        :rtype: ~azure.core.polling.AsyncLROPoller[~azure.mgmt.deviceupdate.models.Instance]
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def begin_create(
        self,
        resource_group_name: str,
        account_name: str,
        instance_name: str,
        instance: Union[_models.Instance, IO],
        **kwargs: Any
    ) -> AsyncLROPoller[_models.Instance]:
        """Creates or updates instance.

        :param resource_group_name: The resource group name. Required.
        :type resource_group_name: str
        :param account_name: Account name. Required.
        :type account_name: str
        :param instance_name: Instance name. Required.
        :type instance_name: str
        :param instance: Instance details. Is either a Instance type or a IO type. Required.
        :type instance: ~azure.mgmt.deviceupdate.models.Instance or IO
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncARMPolling. Pass in False for
         this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either Instance or the result of
         cls(response)
        :rtype: ~azure.core.polling.AsyncLROPoller[~azure.mgmt.deviceupdate.models.Instance]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.Instance] = kwargs.pop("cls", None)
        polling: Union[bool, AsyncPollingMethod] = kwargs.pop("polling", True)
        lro_delay = kwargs.pop("polling_interval", self._config.polling_interval)
        cont_token: Optional[str] = kwargs.pop("continuation_token", None)
        if cont_token is None:
            raw_result = await self._create_initial(
                resource_group_name=resource_group_name,
                account_name=account_name,
                instance_name=instance_name,
                instance=instance,
                api_version=api_version,
                content_type=content_type,
                cls=lambda x, y, z: x,
                headers=_headers,
                params=_params,
                **kwargs
            )
        kwargs.pop("error_map", None)

        def get_long_running_output(pipeline_response):
            deserialized = self._deserialize("Instance", pipeline_response)
            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized

        if polling is True:
            polling_method: AsyncPollingMethod = cast(
                AsyncPollingMethod,
                AsyncARMPolling(lro_delay, lro_options={"final-state-via": "azure-async-operation"}, **kwargs),
            )
        elif polling is False:
            polling_method = cast(AsyncPollingMethod, AsyncNoPolling())
        else:
            polling_method = polling
        if cont_token:
            return AsyncLROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output,
            )
        return AsyncLROPoller(self._client, raw_result, get_long_running_output, polling_method)  # type: ignore

    begin_create.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DeviceUpdate/accounts/{accountName}/instances/{instanceName}"
    }

    async def _delete_initial(  # pylint: disable=inconsistent-return-statements
        self, resource_group_name: str, account_name: str, instance_name: str, **kwargs: Any
    ) -> None:
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[None] = kwargs.pop("cls", None)

        request = build_delete_request(
            resource_group_name=resource_group_name,
            account_name=account_name,
            instance_name=instance_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self._delete_initial.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 202, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        response_headers = {}
        if response.status_code == 202:
            response_headers["Location"] = self._deserialize("str", response.headers.get("Location"))

        if cls:
            return cls(pipeline_response, None, response_headers)

    _delete_initial.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DeviceUpdate/accounts/{accountName}/instances/{instanceName}"
    }

    @distributed_trace_async
    async def begin_delete(
        self, resource_group_name: str, account_name: str, instance_name: str, **kwargs: Any
    ) -> AsyncLROPoller[None]:
        """Deletes instance.

        :param resource_group_name: The resource group name. Required.
        :type resource_group_name: str
        :param account_name: Account name. Required.
        :type account_name: str
        :param instance_name: Instance name. Required.
        :type instance_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncARMPolling. Pass in False for
         this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either None or the result of cls(response)
        :rtype: ~azure.core.polling.AsyncLROPoller[None]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        cls: ClsType[None] = kwargs.pop("cls", None)
        polling: Union[bool, AsyncPollingMethod] = kwargs.pop("polling", True)
        lro_delay = kwargs.pop("polling_interval", self._config.polling_interval)
        cont_token: Optional[str] = kwargs.pop("continuation_token", None)
        if cont_token is None:
            raw_result = await self._delete_initial(  # type: ignore
                resource_group_name=resource_group_name,
                account_name=account_name,
                instance_name=instance_name,
                api_version=api_version,
                cls=lambda x, y, z: x,
                headers=_headers,
                params=_params,
                **kwargs
            )
        kwargs.pop("error_map", None)

        def get_long_running_output(pipeline_response):  # pylint: disable=inconsistent-return-statements
            if cls:
                return cls(pipeline_response, None, {})

        if polling is True:
            polling_method: AsyncPollingMethod = cast(
                AsyncPollingMethod, AsyncARMPolling(lro_delay, lro_options={"final-state-via": "location"}, **kwargs)
            )
        elif polling is False:
            polling_method = cast(AsyncPollingMethod, AsyncNoPolling())
        else:
            polling_method = polling
        if cont_token:
            return AsyncLROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output,
            )
        return AsyncLROPoller(self._client, raw_result, get_long_running_output, polling_method)  # type: ignore

    begin_delete.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DeviceUpdate/accounts/{accountName}/instances/{instanceName}"
    }

    @overload
    async def update(
        self,
        resource_group_name: str,
        account_name: str,
        instance_name: str,
        tag_update_payload: _models.TagUpdate,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.Instance:
        """Updates instance's tags.

        :param resource_group_name: The resource group name. Required.
        :type resource_group_name: str
        :param account_name: Account name. Required.
        :type account_name: str
        :param instance_name: Instance name. Required.
        :type instance_name: str
        :param tag_update_payload: Updated tags. Required.
        :type tag_update_payload: ~azure.mgmt.deviceupdate.models.TagUpdate
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Instance or the result of cls(response)
        :rtype: ~azure.mgmt.deviceupdate.models.Instance
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def update(
        self,
        resource_group_name: str,
        account_name: str,
        instance_name: str,
        tag_update_payload: IO,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.Instance:
        """Updates instance's tags.

        :param resource_group_name: The resource group name. Required.
        :type resource_group_name: str
        :param account_name: Account name. Required.
        :type account_name: str
        :param instance_name: Instance name. Required.
        :type instance_name: str
        :param tag_update_payload: Updated tags. Required.
        :type tag_update_payload: IO
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Instance or the result of cls(response)
        :rtype: ~azure.mgmt.deviceupdate.models.Instance
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def update(
        self,
        resource_group_name: str,
        account_name: str,
        instance_name: str,
        tag_update_payload: Union[_models.TagUpdate, IO],
        **kwargs: Any
    ) -> _models.Instance:
        """Updates instance's tags.

        :param resource_group_name: The resource group name. Required.
        :type resource_group_name: str
        :param account_name: Account name. Required.
        :type account_name: str
        :param instance_name: Instance name. Required.
        :type instance_name: str
        :param tag_update_payload: Updated tags. Is either a TagUpdate type or a IO type. Required.
        :type tag_update_payload: ~azure.mgmt.deviceupdate.models.TagUpdate or IO
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Instance or the result of cls(response)
        :rtype: ~azure.mgmt.deviceupdate.models.Instance
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.Instance] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(tag_update_payload, (IOBase, bytes)):
            _content = tag_update_payload
        else:
            _json = self._serialize.body(tag_update_payload, "TagUpdate")

        request = build_update_request(
            resource_group_name=resource_group_name,
            account_name=account_name,
            instance_name=instance_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            template_url=self.update.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponse, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("Instance", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    update.metadata = {
        "url": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DeviceUpdate/accounts/{accountName}/instances/{instanceName}"
    }
