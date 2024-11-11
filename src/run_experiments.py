import os
import subprocess

alpha_values = [1, 0.5, 0]
fitness_functions = ["distance", "similarity", "blended"]

for alpha in alpha_values:
    for fit in fitness_functions:
        print(f"Running with alpha={alpha} and fitness function={fit}")

        result = subprocess.run(
            [
                "python3", "run.py",
                "--alpha", str(alpha),
                "--with-fit", fit,
                "--gens", "1",
                "--runs", "5",
                "--cleanup"
            ],
            capture_output=True,
            text=True
        )

        print(result.stdout)
        print(result.stderr)

        if result.returncode != 0:
            print(f"Run failed with alpha={alpha} and fitness function={fit}")
