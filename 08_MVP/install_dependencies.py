"""
Silver Trust MVP — dependency installer
Run this once before starting the app or notebook:

    python install_dependencies.py
"""

import subprocess
import sys


PACKAGES = [
    # Core AI
    "openai",
    "langchain",
    "langchain-openai",
    "langchain-core",
    "langsmith",
    # Frontend
    "gradio",
    # Utilities
    "numpy",
    "python-dotenv",
]


def install(packages: list[str]) -> None:
    print("=" * 55)
    print("  Silver Trust MVP — installing dependencies")
    print("=" * 55)

    failed = []

    for pkg in packages:
        print(f"\n  ▶ {pkg}...", end=" ", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "--quiet", pkg],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("✅")
        else:
            print("❌  FAILED")
            print(f"     {result.stderr.strip()}")
            failed.append(pkg)

    print("\n" + "=" * 55)
    if failed:
        print(f"  ⚠️  {len(failed)} package(s) failed to install:")
        for pkg in failed:
            print(f"     • {pkg}")
        print("\n  Try installing them manually:")
        print(f"  pip install {' '.join(failed)}")
        sys.exit(1)
    else:
        print(f"  ✅  All {len(packages)} packages installed successfully.")
        print("\n  You're ready to run:")
        print("    python silver_trust_app.py")
        print("  or open:")
        print("    silver_trust_mvp.ipynb")
    print("=" * 55)


if __name__ == "__main__":
    install(PACKAGES)
