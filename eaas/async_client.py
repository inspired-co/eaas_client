from __future__ import annotations

import uuid
from collections.abc import Callable
from threading import Thread
from typing import Any

from eaas import Client, Config


class AsyncRequest:
    def __init__(self, eaas_client: AsyncClient, request_id: str):
        self._eaas_client = eaas_client
        self._request_id = request_id
        self._result = None

    def get_result(self):
        if self._result is None:
            self._result = self._eaas_client.wait_and_get_result(self._request_id)
        return self._result


# TODO(odashi): Use async concurrency to implement this functionality.
class AsyncClient(Client):
    """
    A client that supports async requests to EaaS. It uses threads so there is a
    limit to the maximum number of parallel requests it can make.
    Example usage:
      1. `request = client.score([])` to start a new thread and make a request
      2. `request.get_result()` to join the thread and get the result
    """

    def __init__(self, config: Config):
        super().__init__(config)
        self._threads: dict[str, Thread] = {}
        self._results: dict[str, Any] = {}

    def _run_thread(self, original_fn: Callable[[], Any]) -> AsyncRequest:
        request_id = str(uuid.uuid1())

        def fn():
            self._results[request_id] = original_fn()

        self._threads[request_id] = Thread(target=fn)
        self._threads[request_id].start()
        return AsyncRequest(self, request_id)

    def async_score(
        self,
        inputs: list[dict],
        task="sum",
        metrics=None,
        lang="en",
        cal_attributes=False,
    ):
        return self._run_thread(
            lambda: super(AsyncClient, self).score(
                inputs, metrics, task, lang, cal_attributes
            )
        )

    def wait_and_get_result(self, request_id: str):
        if request_id not in self._threads:
            raise Exception(f"thread_id {request_id} doesn't exist")
        self._threads[request_id].join()
        result = self._results[request_id]
        self._results.pop(request_id)
        self._threads.pop(request_id)
        return result