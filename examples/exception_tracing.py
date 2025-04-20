from contextlib import ExitStack

from fundi import from_, scan, inject, injection_trace


def require_random_animal() -> str:
    raise ConnectionRefusedError("Failed to connect to server :<")
    return random.choice(["cat", "dog", "chicken", "horse", "platypus", "cow"])


def application(
    animal: str = from_(require_random_animal),
):
    print("Animal:", animal)


with ExitStack() as stack:
    try:
        inject({}, scan(application), stack)
    except Exception as e:
        print(injection_trace(e))
