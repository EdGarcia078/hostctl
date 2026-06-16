import subprocess
from pathlib import Path
import os

def run_detached(cmd, cwd=None):
    cwd = str(Path(cwd).expanduser().resolve()) if cwd else None

    print(f"[hostctl] EXEC: {' '.join(cmd)}")

    process = subprocess.Popen(
        cmd,
        cwd=cwd,
        env=os.environ.copy()  # 👈 CRÍTICO
    )

    return process
