# Text Detection
## Baseline
### Build & Run
```shell
docker build -t text_detection --build-arg SERVICE_PORT=8083 .
docker run -p8083:8083 text_detection
```
### Test
```shell
./test.sh
```
or
```shell
python3 test.py
```
