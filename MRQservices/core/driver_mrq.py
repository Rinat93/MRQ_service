import copy

from pika import SelectConnection, BaseConnection, connection
from pika.adapters import IOLoop
from pika.adapters.utils import nbio_interface
from pika.adapters.utils.selector_ioloop_adapter import SelectorIOServicesAdapter


class MRQdriver(SelectConnection):

    def __init__(self,
            parameters=None,
            on_open_callback=None,
            on_open_error_callback=None,
            on_close_callback=None,
            custom_ioloop=None,
            internal_connection_workflow=True):
        """Create a new instance of the Connection object.

        :param pika.connection.Parameters parameters: Connection parameters
        :param callable on_open_callback: Method to call on connection open
        :param None | method on_open_error_callback: Called if the connection
            can't be established or connection establishment is interrupted by
            `Connection.close()`: on_open_error_callback(Connection, exception).
        :param None | method on_close_callback: Called when a previously fully
            open connection is closed:
            `on_close_callback(Connection, exception)`, where `exception` is
            either an instance of `exceptions.ConnectionClosed` if closed by
            user or broker or exception of another type that describes the cause
            of connection failure.
        :param None | IOLoop | nbio_interface.AbstractIOServices custom_ioloop:
            Provide a custom I/O Loop object.
        :param bool internal_connection_workflow: True for autonomous connection
            establishment which is default; False for externally-managed
            connection workflow via the `create_connection()` factory.
        :raises: RuntimeError

        """
        if isinstance(custom_ioloop, nbio_interface.AbstractIOServices):
            nbio = custom_ioloop
        else:
            nbio = SelectorIOServicesAdapter(custom_ioloop or IOLoop())

        super().__init__(
            parameters,
            on_open_callback,
            on_open_error_callback,
            on_close_callback,
            nbio,
            internal_connection_workflow=internal_connection_workflow)