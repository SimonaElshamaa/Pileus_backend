import subprocess
from pathlib import Path

def main():
    project_root = Path(__file__).resolve().parents[1]

    ini_path = project_root / "configs" / "task19_run.ini"

    # Path to the Task19 repo folder (local)
    task19_repo = project_root / "external" / "T19IceLossMethod-master"
    t19_script = task19_repo / "t19_counter.py"

    subprocess.run(
        ["python", str(t19_script), str(ini_path)],
        check=True
    )

    print("Done. Check outputs/ folder.")

if __name__ == "__main__":
    main()
