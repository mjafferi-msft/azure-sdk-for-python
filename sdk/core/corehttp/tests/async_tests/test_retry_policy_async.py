# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# -------------------------------------------------------------------------
"""Tests for the retry policy."""
from io import BytesIO
import tempfile
import os
import asyncio
from typing import Any
from itertools import product
from unittest.mock import Mock

import pytest
from corehttp.exceptions import (
    BaseError,
    ServiceRequestError,
    ServiceRequestTimeoutError,
    ServiceResponseError,
    ServiceResponseTimeoutError,
)
from corehttp.runtime.policies import (
    AsyncRetryPolicy,
    RetryMode,
)
from corehttp.runtime.pipeline import AsyncPipeline, PipelineResponse, PipelineRequest
from corehttp.transport import AsyncHttpTransport

from utils import HTTP_REQUESTS, ASYNC_HTTP_RESPONSES, create_http_response, request_and_responses_product


def test_retry_code_class_variables():
    retry_policy = AsyncRetryPolicy()
    assert retry_policy._RETRY_CODES is not None
    assert 408 in retry_policy._RETRY_CODES
    assert 429 in retry_policy._RETRY_CODES
    assert 501 not in retry_policy._RETRY_CODES


def test_retry_types():
    history = ["1", "2", "3"]
    settings = {"history": history, "backoff": 1, "max_backoff": 10}
    retry_policy = AsyncRetryPolicy()
    backoff_time = retry_policy.get_backoff_time(settings)
    assert backoff_time == 4

    retry_policy = AsyncRetryPolicy(retry_mode=RetryMode.Fixed)
    backoff_time = retry_policy.get_backoff_time(settings)
    assert backoff_time == 1

    retry_policy = AsyncRetryPolicy(retry_mode=RetryMode.Exponential)
    backoff_time = retry_policy.get_backoff_time(settings)
    assert backoff_time == 4


@pytest.mark.parametrize(
    "retry_after_input,http_request,http_response",
    product(["0", "800", "1000", "1200"], HTTP_REQUESTS, ASYNC_HTTP_RESPONSES),
)
def test_retry_after(retry_after_input, http_request, http_response):
    retry_policy = AsyncRetryPolicy()
    request = http_request("GET", "http://localhost")
    response = create_http_response(http_response, request, None, headers={"Retry-After": retry_after_input})
    pipeline_response = PipelineResponse(request, response, None)
    retry_after = retry_policy.get_retry_after(pipeline_response)
    seconds = float(retry_after_input)
    assert retry_after == seconds


@pytest.mark.asyncio
@pytest.mark.parametrize("http_request,http_response", request_and_responses_product(ASYNC_HTTP_RESPONSES))
async def test_retry_on_429(http_request, http_response):
    class MockTransport(AsyncHttpTransport):
        def __init__(self):
            self._count = 0

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def close(self):
            pass

        async def open(self):
            pass

        async def send(self, request: PipelineRequest, **kwargs: Any) -> PipelineResponse:
            self._count += 1
            response = create_http_response(http_response, request, None, status_code=429)
            return response

    http_request = http_request("GET", "http://localhost/")
    http_retry = AsyncRetryPolicy(retry_total=1)
    transport = MockTransport()
    pipeline = AsyncPipeline(transport, [http_retry])
    await pipeline.run(http_request)
    assert transport._count == 2


@pytest.mark.asyncio
@pytest.mark.parametrize("http_request,http_response", request_and_responses_product(ASYNC_HTTP_RESPONSES))
async def test_no_retry_on_201(http_request, http_response):
    class MockTransport(AsyncHttpTransport):
        def __init__(self):
            self._count = 0

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def close(self):
            pass

        async def open(self):
            pass

        async def send(self, request: PipelineRequest, **kwargs: Any) -> PipelineResponse:
            self._count += 1
            response = create_http_response(http_response, request, None, status_code=201, headers={"Retry-After": "1"})
            return response

    http_request = http_request("GET", "http://localhost/")
    http_retry = AsyncRetryPolicy(retry_total=1)
    transport = MockTransport()
    pipeline = AsyncPipeline(transport, [http_retry])
    await pipeline.run(http_request)
    assert transport._count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("http_request,http_response", request_and_responses_product(ASYNC_HTTP_RESPONSES))
async def test_retry_seekable_stream(http_request, http_response):
    class MockTransport(AsyncHttpTransport):
        def __init__(self):
            self._first = True

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def close(self):
            pass

        async def open(self):
            pass

        async def send(self, request: PipelineRequest, **kwargs: Any) -> PipelineResponse:
            if self._first:
                self._first = False
                request.content.seek(0, 2)
                raise BaseError("fail on first")
            position = request.content.tell()
            assert position == 0
            response = create_http_response(http_response, request, None, status_code=400)
            return response

    data = BytesIO(b"Lots of dataaaa")
    http_request = http_request("GET", "http://localhost/", content=data)
    http_retry = AsyncRetryPolicy(retry_total=1)
    pipeline = AsyncPipeline(MockTransport(), [http_retry])
    await pipeline.run(http_request)


@pytest.mark.asyncio
@pytest.mark.parametrize("http_request,http_response", request_and_responses_product(ASYNC_HTTP_RESPONSES))
async def test_retry_seekable_file(http_request, http_response):
    class MockTransport(AsyncHttpTransport):
        def __init__(self):
            self._first = True

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def close(self):
            pass

        async def open(self):
            pass

        async def send(self, request: PipelineRequest, **kwargs: Any) -> PipelineResponse:
            if self._first:
                self._first = False
                for value in request._files.values():
                    name, body = value[0], value[1]
                    if name and body and hasattr(body, "read"):
                        body.seek(0, 2)
                        raise BaseError("fail on first")
            for value in request._files.values():
                name, body = value[0], value[1]
                if name and body and hasattr(body, "read"):
                    position = body.tell()
                    assert not position
                    response = create_http_response(http_response, request, None, status_code=400)
                    return response

    file = tempfile.NamedTemporaryFile(delete=False)
    file.write(b"Lots of dataaaa")
    file.close()
    headers = {"Content-Type": "multipart/form-data"}
    with open(file.name, "rb") as f:
        form_data_content = {
            "fileContent": f,
            "fileName": f.name,
        }
        http_request = http_request("GET", "http://localhost/", headers=headers, files=form_data_content)
        http_retry = AsyncRetryPolicy(retry_total=1)
        pipeline = AsyncPipeline(MockTransport(), [http_retry])
        await pipeline.run(http_request)
    os.unlink(f.name)


@pytest.mark.asyncio
@pytest.mark.parametrize("http_request", HTTP_REQUESTS)
async def test_retry_timeout(http_request):
    timeout = 1

    def send(request, **kwargs):
        assert kwargs["connection_timeout"] <= timeout, "policy should set connection_timeout not to exceed timeout"
        raise ServiceResponseError("oops")

    transport = Mock(
        spec=AsyncHttpTransport,
        send=Mock(wraps=send),
        connection_config={"connection_timeout": timeout * 2},
        sleep=asyncio.sleep,
    )
    pipeline = AsyncPipeline(transport, [AsyncRetryPolicy(timeout=timeout)])

    with pytest.raises(ServiceResponseTimeoutError):
        await pipeline.run(http_request("GET", "http://localhost/"))


@pytest.mark.asyncio
@pytest.mark.parametrize("http_request,http_response", request_and_responses_product(ASYNC_HTTP_RESPONSES))
async def test_timeout_defaults(http_request, http_response):
    """When "timeout" is not set, the policy should not override the transport's timeout configuration"""

    async def send(request, **kwargs):
        for arg in ("connection_timeout", "read_timeout"):
            assert arg not in kwargs, "policy should defer to transport configuration when not given a timeout"
        response = create_http_response(http_response, request, None, status_code=200)
        return response

    transport = Mock(
        spec_set=AsyncHttpTransport,
        send=Mock(wraps=send),
        sleep=Mock(side_effect=Exception("policy should not sleep: its first send succeeded")),
    )
    pipeline = AsyncPipeline(transport, [AsyncRetryPolicy()])

    await pipeline.run(http_request("GET", "http://localhost/"))
    assert transport.send.call_count == 1, "policy should not retry: its first send succeeded"


combinations = [(ServiceRequestError, ServiceRequestTimeoutError), (ServiceResponseError, ServiceResponseTimeoutError)]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "combinations,http_request",
    product(combinations, HTTP_REQUESTS),
)
async def test_does_not_sleep_after_timeout(combinations, http_request):
    # With default settings policy will sleep twice before exhausting its retries: 1.6s, 3.2s.
    # It should not sleep the second time when given timeout=1
    transport_error, expected_timeout_error = combinations
    timeout = 1

    transport = Mock(
        spec=AsyncHttpTransport,
        send=Mock(side_effect=transport_error("oops")),
        sleep=Mock(wraps=asyncio.sleep),
    )
    pipeline = AsyncPipeline(transport, [AsyncRetryPolicy(timeout=timeout)])

    with pytest.raises(expected_timeout_error):
        await pipeline.run(http_request("GET", "http://localhost/"))

    assert transport.sleep.call_count == 1
