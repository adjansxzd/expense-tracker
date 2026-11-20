"""F7 probe: start N 'add' processes at once against one data file and count what survives."""
import json, os, subprocess, sys, tempfile

N, TRIALS = 20, 3
env = {**os.environ, "PYTHONPATH": os.path.join(os.path.dirname(__file__), "..", "src")}
for trial in range(1, TRIALS + 1):
    path = os.path.join(tempfile.mkdtemp(), "data.json")
    procs = [subprocess.Popen([sys.executable, "-m", "expense_tracker", "--file", path,
                               "add", "2026-11-01", "food", "1"],
                              env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
             for _ in range(N)]
    results = [(p.wait(), p.stderr.read().decode().strip().splitlines()[-1:] ) for p in procs]
    crashed = [r for r in results if r[0] != 0]
    with open(path, encoding="utf-8") as f:
        saved = json.load(f)
    errors = sorted({r[1][0].split(":")[0] for r in crashed if r[1]})
    print(f"trial {trial}: {N} processes, exit!=0: {len(crashed)}, "
          f"records saved: {len(saved)} (expected {N}), error types: {errors}")
