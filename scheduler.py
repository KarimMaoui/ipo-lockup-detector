import subprocess
import datetime

def run_script(script_name):
    print(f"[{datetime.datetime.now()}] Running {script_name}...")
    result = subprocess.run(["python", f"src/{script_name}"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error in {script_name}:\n{result.stderr}")
    else:
        print(f"✅ {script_name} completed successfully.")

if __name__ == "__main__":
    scripts = [
        "fetch_ipo.py",
        "fetch_news.py",
        "process_data.py",
        "update_digest.py"
    ]
    for script in scripts:
        run_script(script)
