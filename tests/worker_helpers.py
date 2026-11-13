from concurrent.futures import ThreadPoolExecutor


def on_worker(function, *args, **kwargs):
    """Call a desktop worker on its own thread, as the application does."""
    with ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(function, *args, **kwargs).result(timeout=10)
