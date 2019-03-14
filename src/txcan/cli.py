import logging

import altwistendpy
import click
import can
import twisted.internet.defer
import twisted.internet.task

import txcan

logger = logging.getLogger(__name__)


@click.command()
def main():
    root_logger = logging.getLogger()
    log_level = logging.DEBUG

    stderr_handler = logging.StreamHandler()
    root_logger.addHandler(stderr_handler)

    root_logger.setLevel(log_level)
    stderr_handler.setLevel(log_level)

    root_logger.debug('red green blue')

    react_inline_callbacks(inline_callbacks_main)


def react_inline_callbacks_helper(reactor, f, args, kwargs):
    return f(reactor, *args, **kwargs)


def react_inline_callbacks(f, *args, **kwargs):
    twisted.internet.task.react(
        react_inline_callbacks_helper,
        (f, args, kwargs),
    )


@twisted.internet.defer.inlineCallbacks
def inline_callbacks_main(reactor):
    can_bus = can.interface.Bus(bustype='socketcan', channel='can0')

    txcan_bus = txcan.Bus.build(bus=can_bus, reactor=reactor)

    with txcan_bus.linked():
        yield altwistendpy.sleep(.2)

        import time
        start = time.time()

        logger.debug('starting loop')

        while time.time() - start < 1:
            message = yield txcan_bus.receive_queue.get()
            import threading
            logging.debug(
                'inline_callbacks_main %s %s',
                threading.get_ident() == threading.main_thread().ident,
                message,
            )
