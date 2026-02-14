"""
Simple training runner for FD-XIDS.

This script provides a lightweight CLI wrapper to run the training scripts
already present in `backend/models/`.

Usage examples (from project root):
    python backend/models/run_train.py --runner pipeline
    python backend/models/run_train.py --runner model --tune

Options:
- runner: 'pipeline' (runs `train_pipeline_fd_xids.py`) or 'model' (runs `train_model.py`)
- --tune: when used with 'model', enables GridSearch tuning in `train_model.py`

This avoids import-time issues and executes the existing training scripts
as separate processes so their console output is preserved.
"""

import os
import argparse
import subprocess
import sys


def _project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))


def run_pipeline():
    root = _project_root()
    script = os.path.join(root, "backend", "models", "train_pipeline_fd_xids.py")
    if not os.path.exists(script):
        print(f"Pipeline script not found: {script}")
        sys.exit(2)

    cmd = [sys.executable, script]
    print("Running FD-XIDS pipeline:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def run_model(tune: bool = False):
    root = _project_root()
    script = os.path.join(root, "backend", "models", "train_model.py")
    if not os.path.exists(script):
        print(f"Model training script not found: {script}")
        sys.exit(2)

    cmd = [sys.executable, script, "--data", os.path.join("backend", "data", "processed", "train_processed.csv")]
    if tune:
        cmd.append("--tune")

    print("Running model trainer:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description="Run FD-XIDS training scripts")
    parser.add_argument("--runner", choices=["pipeline", "model"], default="pipeline")
    parser.add_argument("--tune", action="store_true", help="Enable GridSearch when using --runner model")
    args = parser.parse_args()

    try:
        if args.runner == "pipeline":
            run_pipeline()
        else:
            run_model(tune=args.tune)
    except subprocess.CalledProcessError as e:
        print(f"Training process failed with exit code {e.returncode}")
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
