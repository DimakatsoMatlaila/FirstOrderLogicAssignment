import os
import subprocess
import sys
from pathlib import Path

# Color formatting
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
ENDC = '\033[0m'

def run_question_tests(question, root_path):
    base_dir = root_path / "Submissions" / "A"
    test_dir = base_dir / f"Assignment2PartA/Q{question}"
    script_path = base_dir / f"q{question}.py"
    
    print(f"\n{YELLOW}=== Testing Question {question} ==={ENDC}")
    
    if not test_dir.exists():
        print(f"{RED}Test directory missing for Q{question}{ENDC}")
        return 0, 0
        
    if not script_path.exists():
        print(f"{RED}Script missing for Q{question}{ENDC}")
        return 0, 0

    input_files = sorted(test_dir.glob("sample*_in.txt"))
    if not input_files:
        print(f"{YELLOW}No test cases found for Q{question}{ENDC}")
        return 0, 0

    passed = 0
    total = len(input_files)

    for input_file in input_files:
        test_name = input_file.stem.replace("_in", "")
        output_file = test_dir / f"{test_name}_out.txt"
        
        print(f"\nTesting {test_name}...")
        
        try:
            # Run from the root directory to maintain relative paths
            with open(input_file, 'r') as f_in:
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    stdin=f_in,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=root_path  # Run from project root
                )

            if result.stderr:
                print(f"{RED}Runtime error:{ENDC}")
                print(result.stderr)
                continue

            # Compare outputs
            with open(output_file, 'r') as f_exp:
                expected = f_exp.read().strip().splitlines()
                actual = result.stdout.strip().splitlines()

                if len(expected) != len(actual):
                    print(f"{RED}Line count mismatch{ENDC}")
                    continue

                all_match = True
                for i, (exp_line, act_line) in enumerate(zip(expected, actual)):
                    if exp_line.strip() != act_line.strip():
                        print(f"{RED}Mismatch line {i+1}:{ENDC}")
                        print(f"Expected: {exp_line}")
                        print(f"Actual:   {act_line}")
                        all_match = False

                if all_match:
                    print(f"{GREEN}Test passed!{ENDC}")
                    passed += 1
                else:
                    print(f"{RED}Test failed!{ENDC}")

        except Exception as e:
            print(f"{RED}Error: {str(e)}{ENDC}")

    return passed, total

def main():
    root_path = Path(__file__).parent
    print(f"{YELLOW}🚀 Starting test suite...{ENDC}")
    
    results = {}
    for q in [1, 2, 3, 4]:
        passed, total = run_question_tests(q, root_path)
        results[q] = (passed, total)
    
    print(f"\n{YELLOW}📊 Final Results:{ENDC}")
    all_passed = True
    for q in [1, 2, 3, 4]:
        passed, total = results[q]
        if passed < total:
            all_passed = False
            color = RED
        else:
            color = GREEN
            
        print(f"Q{q}: {color}{passed}/{total} passed{ENDC}")
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()