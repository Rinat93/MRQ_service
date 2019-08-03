import copy

from pika import SelectConnection, BaseConnection, connection
from pika.adapters import IOLoop
from pika.adapters.utils import nbio_interface
from pika.adapters.utils.selector_ioloop_adapter import SelectorIOServicesAdapter


class MRQdriver(SelectConnection): pass