#!/usr/bin/env python3

from concurrent import futures
import time
import logging

import grpc

import smartchess_pb2
import smartchess_pb2_grpc

from sensor_read import SensorReadMultiplayerMock

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class SensorReader(smartchess_pb2_grpc.SensorReadServicer):

    def __init__(self):
        self.sensorRead = SensorReadMultiplayerMock()
    
    def SendSensorData(self, request, context):
        return smartchess_pb2.SensorResponse(self.sensorRead.read_sensors())

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    smartchess_pb2_grpc.add_SensorReadServicer_to_server(SensorReader(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    logging.basicConfig()
    serve()
    
