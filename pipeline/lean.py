from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LeanResult:
    accepted: bool
    diagnostics: str


class LeanVerifier:
    def __init__(self, project_root: Path, mode: str = "auto") -> None:
        if mode not in {"auto", "required", "skip"}:
            raise ValueError(f"unknown Lean mode: {mode}")
        self.project_root = project_root.resolve()
        self.lake = shutil.which("lake")
        self.enabled = mode != "skip" and self.lake is not None
        if mode == "required" and self.lake is None:
            raise RuntimeError("Lean verification was required, but `lake` is not available")

    def check(self, declaration: str) -> LeanResult:
        if not self.enabled:
            return LeanResult(False, "Lean verification skipped: `lake` is unavailable or disabled")
        source = "import Mathlib\n\n" + declaration.strip() + "\n"
        with tempfile.NamedTemporaryFile("w", suffix=".lean", encoding="utf-8", delete=False) as handle:
            handle.write(source)
            path = Path(handle.name)
        try:
            process = subprocess.run(
                [self.lake, "env", "lean", str(path)],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            diagnostics = (process.stdout + process.stderr).strip()
            return LeanResult(process.returncode == 0, diagnostics)
        except subprocess.TimeoutExpired:
            return LeanResult(False, "Lean verification timed out after 60 seconds")
        finally:
            path.unlink(missing_ok=True)
