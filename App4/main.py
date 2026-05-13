import io
import sys


old_stdout = sys.stdout
sys.stdout = buffer = io.StringIO()
code = """
import random
print(random.randint(1, 100))"""
#exec(code)

try:
    exec(code)
except Exception as e:
    print(f"Error: {e}")

sys.stdout = old_stdout
output = buffer.getvalue()
print("Captured output:", output)
