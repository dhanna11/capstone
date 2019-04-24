all: smartchess_pb2_grpc.py smartchess_pb2.py

smartchess_pb2_grpc.py: smartchess.proto
	python3 -m grpc_tools.protoc --proto_path=. smartchess.proto --python_out=. --grpc_python_out=.

smartchess_pb2.py: smartchess.proto
	python3 -m grpc_tools.protoc --proto_path=. smartchess.proto --python_out=. --grpc_python_out=.
