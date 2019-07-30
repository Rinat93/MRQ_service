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


    @classmethod
    def create_connection(cls,
                          connection_configs,
                          on_done,
                          custom_ioloop=None,
                          workflow=None):
        print('Создание')
        return super(MRQdriver, cls).create_connection(connection_configs,on_done,custom_ioloop=None,workflow=None)



    @classmethod
    def _start_connection_workflow(cls, connection_configs, connection_factory,
                                   nbio, workflow, on_done):
        print("Мудло сука ты тута?")
        """Helper function for custom implementations of `create_connection()`.

        :param sequence connection_configs: A sequence of one or more
            `pika.connection.Parameters`-based objects.
        :param callable connection_factory: A function that takes
            `pika.connection.Parameters` as its only arg and returns a brand new
            `pika.connection.Connection`-based adapter instance each time it is
            called. The factory must instantiate the connection with
            `internal_connection_workflow=False`.
        :param pika.adapters.utils.nbio_interface.AbstractIOServices nbio:
        :param connection_workflow.AbstractAMQPConnectionWorkflow | None workflow:
            Pass an instance of an implementation of the
            `connection_workflow.AbstractAMQPConnectionWorkflow` interface;
            defaults to a `connection_workflow.AMQPConnectionWorkflow` instance
            with default values for optional args.
        :param callable on_done: as defined in
            :py:meth:`connection_workflow.AbstractAMQPConnectionWorkflow.start()`.
        :returns: Connection workflow instance in use. The user should limit
            their interaction with this object only to it's `abort()` method.
        :rtype: connection_workflow.AbstractAMQPConnectionWorkflow

        """
        if workflow is None:
            workflow = cls.connection_workflow.AMQPConnectionWorkflow()
            cls.LOGGER.debug('Created default connection workflow %r', workflow)

        if isinstance(workflow, cls.connection_workflow.AMQPConnectionWorkflow):
            workflow.set_io_services(nbio)

        def create_connector():
            """`AMQPConnector` factory."""
            return cls.connection_workflow.AMQPConnector(
                lambda params: cls._StreamingProtocolShim(
                    connection_factory(params)),
                nbio)

        workflow.start(
            connection_configs=connection_configs,
            connector_factory=create_connector,
            native_loop=nbio.get_native_ioloop(),
            on_done=cls.functools.partial(cls._unshim_connection_workflow_callback,
                                      on_done))

        return workflow