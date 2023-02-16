import random
import time

import uvicorn
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from tracing import *

app = FastAPI()


@app.get(
path='/'
)
def home():
    time.sleep(random.randint(1,2))
    return "funfou"



FastAPIInstrumentor.instrument_app(app)
