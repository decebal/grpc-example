# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC route guide server."""
import json
from concurrent import futures
import time

import grpc
from opencensus.trace.samplers import always_on
# from opencensus.trace.exporters import stackdriver_exporter
from opencensus.trace.ext.grpc import server_interceptor
from opencensus.trace.exporters import print_exporter
from opencensus.trace.exporters.transports import background_thread

from ouroboros_pb2 import ouroboros_pb2
from ouroboros_pb2_grpc import ouroboros_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class OuroborosServicer(ouroboros_pb2_grpc.OuroborosServicer):
    """Provides methods that implement functionality of route guide server."""

    def SyncJob(self, request, context):
        data = json.loads(request.message)
        try:
            response_bag = data
            # response_bag = worker().work(data)
        except ValueError as exc:
            response_bag = ({}, str(exc))

        return ouroboros_pb2.Response(
            message=json.dumps(response_bag)
        )


class OuroborosServer(object):

    def __init__(self, **kwargs):
        self.host = kwargs.get('host', "[::]")
        self.port = kwargs.get('port', 80)
        self.max_workers = kwargs.get('max', 100)

    def start(self):
        server = self._instance()
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)

    def stop(self):
        self._instance().stop(1)

    def restart(self):
        self._instance().stop(1)
        self.start()

    def _instance(self):
        sampler = always_on.AlwaysOnSampler()
        exporter = print_exporter.PrintExporter(transport=background_thread.BackgroundThreadTransport)
        # exporter = stackdriver_exporter.StackdriverExporter(project_id="")
        tracer_interceptor = server_interceptor.OpenCensusServerInterceptor(sampler, exporter)
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=self.max_workers),
            interceptors=(tracer_interceptor,)
        )
        ouroboros_pb2_grpc.add_OuroborosServicer_to_server(
            OuroborosServicer(),
            server
        )
        server.add_insecure_port(f"{self.host}:{self.port}")

        return server


if __name__ == '__main__':
    OuroborosServer().start()
