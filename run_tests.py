import os
import subprocess
import json
import time
import sys

# Constants
PLAN_FILE = "test_status.json"
WAIT_TIME = 15  # Seconds to wait for service initialization
ROOT_DIR = "."
IS_CI = os.environ.get("CI", "false").lower() == "true" or "--ci" in sys.argv

if IS_CI:
    WAIT_TIME = 30  # Double wait time for CI/Emulation environments
    print("🤖 CI Mode Detected: Increased wait time to 30s")

def run_command(command, cwd="."):
    """Run a shell command and return its exit code and output."""
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=True, 
            check=False, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True
        )
        return result.returncode, result.stdout
    except Exception as e:
        return 1, str(e)

def load_status():
    """Load the test status from JSON file."""
    if os.path.exists(PLAN_FILE):
        try:
            with open(PLAN_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_status(status):
    """Save the test status to JSON file."""
    with open(PLAN_FILE, "w") as f:
        json.dump(status, f, indent=4)

def find_compose_files(root_dir):
    """Find all docker-compose.yml files recursively."""
    compose_files = []
    for root, dirs, files in os.walk(root_dir):
        if "docker-compose.yml" in files:
            # Store relative path for portability
            rel_path = os.path.relpath(os.path.join(root, "docker-compose.yml"), root_dir)
            compose_files.append(rel_path)
    # Sort for deterministic order
    return sorted(compose_files)

def cleanup_service(file_path):
    """Force cleanup of a service (docker-compose down)."""
    dir_path = os.path.dirname(file_path)
    cmd = f"docker-compose -f docker-compose.yml down -v"
    code, output = run_command(cmd, cwd=dir_path)
    return code == 0

def test_service(file_path):
    """Run the validation lifecycle for a single service."""
    dir_path = os.path.dirname(file_path)
    print(f"\n🔍 Testing: {dir_path}")

    # 1. Pre-cleanup (Critical for idempotency)
    print("  🧹 Pre-flight cleanup...")
    cleanup_service(file_path)

    # 2. Start Service
    print("  🚀 Starting service...")
    cmd_up = "docker-compose -f docker-compose.yml up -d"
    code, output = run_command(cmd_up, cwd=dir_path)
    
    if code != 0:
        print(f"  ❌ Start Failed:\n{output}")
        # Always cleanup even if start failed
        cleanup_service(file_path)
        return False

    # 3. Wait
    print(f"  ⏳ Waiting {WAIT_TIME}s for initialization...")
    time.sleep(WAIT_TIME)

    # 4. Verify
    print("  🩺 Verifying status...")
    cmd_ps = "docker-compose -f docker-compose.yml ps"
    code, output = run_command(cmd_ps, cwd=dir_path)
    
    is_healthy = True
    if "Exit 1" in output or "Restarting" in output:
        print(f"  ❌ Health Check Failed:\n{output}")
        print("\n  📜 Container Logs (Tail 20 lines):")
        cmd_logs = "docker-compose -f docker-compose.yml logs --tail 20"
        _, logs = run_command(cmd_logs, cwd=dir_path)
        print(logs)
        is_healthy = False
    else:
        print("  ✅ Service appears healthy.")

    # 5. Post-cleanup (Always run!)
    print("  🧹 Post-test cleanup...")
    cleanup_service(file_path)

    return is_healthy

def main():
    # 0. Initialize or Load Plan
    status_map = load_status()
    all_files = find_compose_files(ROOT_DIR)
    
    # Check for --reset flag
    if "--reset" in sys.argv:
        print("🔄 Resetting test plan...")
        status_map = {}
        save_status({})

    # Sync found files with status map (add new ones)
    for f in all_files:
        if f not in status_map:
            status_map[f] = "pending"
    
    # Save updated map
    save_status(status_map)

    # Count stats
    total = len(all_files)
    passed = sum(1 for s in status_map.values() if s == "passed")
    failed = sum(1 for s in status_map.values() if s == "failed")
    pending = total - passed - failed

    print(f"📊 Test Plan Status: Total {total} | Passed {passed} | Failed {failed} | Pending {pending}")
    print("---------------------------------------------------")

    # 1. Execution Loop
    for file_path in all_files:
        current_status = status_map.get(file_path, "pending")
        
        if current_status == "passed":
            print(f"⏭️  Skipping passed: {os.path.dirname(file_path)}")
            continue
            
        # Run test
        success = test_service(file_path)
        
        if success:
            status_map[file_path] = "passed"
            save_status(status_map)
            print(f"🎉 PASSED: {os.path.dirname(file_path)}")
        else:
            status_map[file_path] = "failed"
            save_status(status_map)
            print(f"⛔️ FAILED: {os.path.dirname(file_path)}")
            # print("\n⚠️  Stopping execution. Please fix the issue above and run the script again.")
            # exit(1)
            print("⚠️  Continuing to next service...")

    print("\n✅ All tests completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔️ Script interrupted by user.")
        exit(1)
