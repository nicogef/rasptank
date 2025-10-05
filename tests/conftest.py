import os
import sys
import threading
import traceback

import pytest

# We import classes to detect and stop leaked threads.
# These modules do not start hardware by themselves; controllers are injected by tests.
try:
    from src.controllers.servo import ServoCtrlThread  # type: ignore
except ImportError:  # pragma: no cover - controller module not available in some envs
    ServoCtrlThread = None  # type: ignore
try:
    from src.controllers.leds import LedCtrl  # type: ignore
except ImportError:  # pragma: no cover - controller module not available in some envs
    LedCtrl = None  # type: ignore


DEBUG_THREADS = os.environ.get("DEBUG_THREADS", "0") not in (
    "",
    "0",
    "false",
    "False",
    None,
)


def _describe_threads():
    infos = []
    current_frames = sys._current_frames()  # type: ignore[attr-defined]  # pylint: disable=protected-access
    for t in threading.enumerate():
        if t is threading.current_thread():
            continue
        tid = getattr(t, "ident", None)
        frame = current_frames.get(tid)
        stack = "".join(traceback.format_stack(frame)) if frame else "<no stack>\n"
        infos.append((t, stack))
    return infos


def _stop_known_thread_if_needed(t):
    try:
        if ServoCtrlThread is not None and isinstance(t, ServoCtrlThread):
            stop = getattr(t, "stop_thread", None)
            if callable(stop):
                stop()
            return

        if LedCtrl is not None and isinstance(t, LedCtrl):
            # Prefer graceful stop() if available; fall back to stop_thread()
            stop = getattr(t, "stop", None)
            if callable(stop):
                stop()
                return
            stop_thread = getattr(t, "stop_thread", None)
            if callable(stop_thread):
                stop_thread()
    except (RuntimeError, AttributeError):
        # Do not fail the test because of cleanup diagnostics
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_teardown(item):  # pylint: disable=unused-argument
    # Run the actual teardown first
    yield

    # After each test, attempt to stop any leaked known controller threads
    for t in list(threading.enumerate()):
        _stop_known_thread_if_needed(t)

    if DEBUG_THREADS:
        _debug_print_leaked_threads()


def _debug_print_leaked_threads():
    leaked = [t for t in threading.enumerate() if t is not threading.current_thread()]
    if not leaked:
        return
    print("\n[DEBUG] Alive threads after test:")
    for t, stack in _describe_threads():
        print(f" - {t.name} (daemon={t.daemon}) -> {t}")
        print(stack)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):  # pylint: disable=unused-argument
    # Final pass: ensure no known controller threads are left running
    for t in list(threading.enumerate()):
        _stop_known_thread_if_needed(t)

    leaked = [t for t in threading.enumerate() if t is not threading.current_thread()]
    if leaked:
        print("\n[TEST SESSION DIAGNOSTICS] Threads still alive at session finish:")
        for t, stack in _describe_threads():
            print(f" - {t.name} (daemon={t.daemon}) -> {t}")
            print(stack)
        print(
            "[HINT] If these are from async executors or hardware mocks, ensure proper "
            "shutdown in tearDown/fixture finalizers."
        )
