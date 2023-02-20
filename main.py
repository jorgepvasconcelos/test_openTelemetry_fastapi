import random
import time

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from tracing import tracer, tracer_provider, tracer_endpoint
from utils import dict_to_str

app = FastAPI()


def long_func():
    with tracer.start_as_current_span(name='long_func') as span:
        random_value = random.randint(1, 3)
        time.sleep(random_value)
        span.set_attribute("long_func.return", random_value)
        return random_value


@app.get(
    path='/index')
@tracer_endpoint()
def home():
    r = long_func()
    f_return = {'return': r}
    return JSONResponse(content=f_return,status_code=200)


FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)
uvicorn.run(
    app=app
            )