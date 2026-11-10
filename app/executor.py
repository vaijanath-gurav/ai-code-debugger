import sys
import subprocess
import tempfile
import os

def run_python_code(code: str) -> dict:
    """
    Executes Python code in a temporary subprocess and captures stdout/stderr.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        temp_path = temp_file.name

    try:
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            "status": "success" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "stderr": "Execution timed out after 10 seconds."}
    except Exception as e:
        return {"status": "error", "stderr": str(e)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)