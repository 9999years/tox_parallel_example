import random
import sys

color = int(sys.argv[1])
reset = int(sys.argv[2])

buffered = False
if len(sys.argv) > 3:
    if sys.argv[3] == "--buffered":
        buffered = True

for _ in range(10_000):
    text = f"\x1b[{color}m" + ("#" * random.randint(0, 10)) + f"\x1b[{reset}m"
    if buffered:
        sys.stdout.write(text)
        sys.stdout.flush()
    else:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()

print()
