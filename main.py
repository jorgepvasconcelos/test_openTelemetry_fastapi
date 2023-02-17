import random
import time

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from tracing import OTLPProvider

app = FastAPI()


def long_func():
    random_value = random.randint(1, 2)
    time.sleep(random_value)
    return random_value


@app.get(
    path='/')
def home():
    r = long_func()
    return r



provider = OTLPProvider()
FastAPIInstrumentor.instrument_app(app,tracer_provider=provider.tracer_provider)