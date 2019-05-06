import logging

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
    deferred = f(reactor, *args, **kwargs)

    def cancel():
        deferred.cancel()
        return deferred

    reactor.addSystemEventTrigger('before', 'shutdown', cancel)

    return deferred


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
        yield twisted.internet.task.deferLater(reactor, 0.2, lambda: None)

        start = reactor.seconds()

        logger.debug('starting loop')

        end = start + 2

        while reactor.seconds() < end:
            deferred = txcan_bus.receive_queue.get()
            deferred.addTimeout(timeout=end - reactor.seconds(), clock=reactor)
            try:
                message = yield deferred
            except twisted.internet.defer.TimeoutError:
                continue

            import threading
            logging.debug(
                'inline_callbacks_main %s %s',
                threading.get_ident() == threading.main_thread().ident,
                message,
            )
