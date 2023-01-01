import os
import sys

ROOT_PATH = os.path.abspath(os.path.join(__file__, "../../.."))
assert os.path.exists(ROOT_PATH), f"does not exist: {ROOT_PATH}"
sys.path.append(ROOT_PATH)
