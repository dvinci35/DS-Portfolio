from starlette.applications import Starlette
from starlette.responses import StreamingResponse
from starlette.routing import Route
from transformers import (
    TextIteratorStreamer,
    AutoTokenizer,
    AutoModelForCausalLM,
)
import asyncio
from pathlib import Path
from threading import Thread

import yaml, os

CONFIG_FILE_PATH = os.environ.get("CONFIG_FILE_PATH")


def read_config(file_path):
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
    return config


async def homepage(request):
    payload = await request.body()
    input_str = payload.decode("utf-8")
    input_tokenized = app.tokenizer(input_str, return_tensors="pt").to("cuda")
    trd = Thread(
        target=app.model.generate,
        kwargs=dict(
            **input_tokenized,
            streamer=app.streamer,
            max_new_tokens=512,
        ),
    )
    trd.start()
    return StreamingResponse(app.streamer)


app = Starlette(
    routes=[
        Route("/", homepage, methods=["POST"]),
    ],
)


@app.on_event("startup")
async def startup_event():
    config = read_config(Path(CONFIG_FILE_PATH))
    app.tokenizer = AutoTokenizer.from_pretrained(config["pipeline_params"]["model"])

    app.model = AutoModelForCausalLM.from_pretrained(**config["pipeline_params"])
    app.streamer = TextIteratorStreamer(
        app.tokenizer,
        skip_prompt=True,
        skip_special_tokens=True,
    )
