import random
import time

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from tracing import tracer, tracer_provider

app = FastAPI()


def long_func():
    random_value = random.randint(1, 2)
    time.sleep(random_value)
    return random_value


@app.get(
    path='/')
def home():
    with tracer.start_as_current_span(name='nameeeee') as span:
        r = long_func()
        return r


FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)
