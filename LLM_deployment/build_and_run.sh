docker build -t inf_api .

docker run \
    --runtime nvidia \
    --gpus all \
    -p 80:80 \
    inf_api