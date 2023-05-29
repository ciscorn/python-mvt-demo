.PHONY: init run test

MVT_PROTO = ./mvt_demo/mvt/

init:
	poetry install

run-single:  # single-process
	poetry run uvicorn mvt_demo:app --reload

run-mp:  # multi-process
	poetry run gunicorn -w 10 -k uvicorn.workers.UvicornWorker mvt_demo:app

update_proto:
	protoc -I=$(MVT_PROTO) --python_out=$(MVT_PROTO) --pyi_out=$(MVT_PROTO) vector_tile.proto
