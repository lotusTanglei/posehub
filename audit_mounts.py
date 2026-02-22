import os
import re

def audit_bind_mounts(root_dir):
    print("Auditing Bind Mounts in docker-compose.yml files...")
    print("-----------------------------------------------------")
    
    issues_found = 0
    checked_files = 0
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == "docker-compose.yml":
                checked_files += 1
                file_path = os.path.join(root, file)
                #print(f"Checking {file_path}")
                
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                # Regex to find volumes:
                # Matches:
                # - ./path:/container/path
                # - ../path:/container/path
                # - /abs/path:/container/path (less common in portable compose)
                # Note: This is a heuristic. It might miss complex YAML or catch comments.
                # We specifically look for lines starting with whitespace + - + space + path:path
                
                # Pattern: Any line with "- ./...:..." or "- /...:..." inside a volumes block context is hard without a parser.
                # Simplified: Find any string that looks like a bind mount path.
                
                # Looking for: "- ./foo:/bar"
                volumes = re.findall(r'-\s+(\./[^:]+):', content)
                
                for vol in volumes:
                    # Clean up path (remove trailing spaces if any)
                    vol_path = vol.strip()
                    
                    # Resolve path relative to the compose file
                    abs_vol_path = os.path.abspath(os.path.join(root, vol_path))
                    
                    if not os.path.exists(abs_vol_path):
                        print(f"❌ MISSING FILE/DIR: {file_path}")
                        print(f"   Reference: {vol_path}")
                        print(f"   Resolved:  {abs_vol_path}")
                        issues_found += 1
                    else:
                        # print(f"✅ Found: {vol_path}")
                        pass

    print("-----------------------------------------------------")
    print(f"Audit Complete.")
    print(f"Files Checked: {checked_files}")
    print(f"Issues Found:  {issues_found}")
    
    if issues_found > 0:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    audit_bind_mounts(".")
