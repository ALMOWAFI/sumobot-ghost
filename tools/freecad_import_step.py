from __future__ import annotations

from pathlib import Path
import shutil
import sys
import tempfile


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: FreeCADCmd.exe freecad_import_step.py <input.step> <output.FCStd>")
        return 1

    step_path = Path(sys.argv[1]).resolve()
    fcstd_path = Path(sys.argv[2]).resolve()

    if not step_path.exists():
        print(f"STEP file not found: {step_path}")
        return 2

    fcstd_path.parent.mkdir(parents=True, exist_ok=True)

    import FreeCAD as App
    import Import

    doc = App.newDocument("SumoBotChassis")
    try:
        Import.insert(str(step_path), doc.Name)
        doc.recompute()
        temp_fcstd = Path(tempfile.gettempdir()) / fcstd_path.name
        if temp_fcstd.exists():
            temp_fcstd.unlink()
        doc.saveAs(str(temp_fcstd))
        shutil.copy2(temp_fcstd, fcstd_path)
        print(f"Imported STEP into FreeCAD document: {fcstd_path}")
    finally:
        App.closeDocument(doc.Name)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
