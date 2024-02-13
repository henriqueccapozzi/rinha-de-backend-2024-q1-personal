import bjoern
import os, signal


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
app = get_wsgi_application()

NUM_WORKERS = int(os.environ.get("NUM_WORKERS", 8))
PORT = int(os.environ.get("PORT", 8000))
worker_pids = []

print("Starting bjoern with %d workers on port: %d" % (NUM_WORKERS, PORT))
bjoern.listen(app, "0.0.0.0", PORT)
for _ in range(NUM_WORKERS):
    pid = os.fork()
    if pid > 0:
        # in master
        worker_pids.append(pid)
    elif pid == 0:
        # in worker
        try:
            bjoern.run()
        except KeyboardInterrupt:
            pass
        exit()
try:
    # Wait for the first worker to exit. They should never exit!
    # Once first is dead, kill the others and exit with error code.
    pid, xx = os.wait()
    worker_pids.remove(pid)
finally:
    for pid in worker_pids:
        os.kill(pid, signal.SIGINT)
        exit(1)
