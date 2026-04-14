import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python target_script.py <int>")
        sys.exit(1)
        
    try:
        x = int(sys.argv[1])
        y = 2 * x + 3
        print(y)
    except ValueError:
        print("Error: Input must be an integer")
        sys.exit(1)

if __name__ == "__main__":
    main()
