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
"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import json

import grpc

from ouroboros_pb2 import ouroboros_pb2
from ouroboros_pb2_grpc import ouroboros_pb2_grpc

traversal_json = {
    "selection": {
        "totalCount": True,
        "__typename": True
    },
    "has_mutation": False,
    "job_name": "visit"
}


def make_request(job, message):
    return ouroboros_pb2.Request(
        job=job,
        message=message
    )


def generate_messages():
    messages = [
        make_request("traversal", "{'memorial': '1'}"),
        make_request("traversal", "{'memorial': '2'}"),
        make_request("traversal", "{'memorial': '3'}"),
        make_request("traversal", "{'memorial': '4'}"),
    ]
    for msg in messages:
        print("Sending %s at %s" % (msg.job, msg.message))
        yield msg


def traversal_chat(stub):
    response = stub.SyncJob(make_request("memorial.visit", json.dumps(traversal_json)))
    print(f"Received message {response.message}")


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = ouroboros_pb2_grpc.OuroborosStub(channel)
    print("-------------- TraversalChat --------------")
    traversal_chat(stub)
    # print("-------------- MutationChat --------------")
    # mutation_chat(stub)


if __name__ == '__main__':
    run()
