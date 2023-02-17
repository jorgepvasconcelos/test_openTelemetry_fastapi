import functools

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor


class OTLPProvider:
    def __init__(self):
        # set the service name to show in traces
        resource = Resource(attributes={"service.name": "service_fastapi"})

        # set the tracer provider
        self.__tracer_provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer_provider=self.__tracer_provider)

        # set the processor
        otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
        span_processor = BatchSpanProcessor(otlp_exporter)
        self.__tracer_provider.add_span_processor(span_processor=span_processor)

    @property
    def tracer_provider(self) -> TracerProvider:
        return self.__tracer_provider


def instrument(name="request"):
    def decorator(method):
        @functools.wraps(method)
        async def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(name=name) as span:
                response = await method(*args, **kwargs)
                return response

        return wrapper

    return decorator


def instrument_sync(name="request"):
    def decorator(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(name=name) as span:
                response = method(*args, **kwargs)
                return response

        return wrapper

    return decorator
