import os
import sys

def main():

    if os.environ.get("ENV") == "pi":
        #add directories
        sys.path.append(os.environ.get("DOORA_PATH") + '/raspberry')
        
        from loop import loop
        print("Starting Doora - Config for Raspberry Pi")
        loop()
        

if __name__ == "__main__":
    # Set environment variables depending on target platform
    args = sys.argv[1:]
    if not len(args) >= 1:
        print("Insufficient arguments provided. Please specify the environment with --pi.")
        sys.exit(1)

    env_file_path = ""
    if args[0] == "--pi":
        env_file_path = ".env.raspberry_pi.txt"
    if args[0] == "--mac":
        env_file_path = ".env.macintosh.txt"
        import keyboard

    with open(env_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                var_name, var_value = line.split('=')
                os.environ[var_name] = var_value

    main()
