#!/usr/bin/env bash
set -euo pipefail

# build vm
gcc -O2 -Wall -Wextra -std=c11 protolang/vm.c -o protolang/vm

echo "built protolang/vm"
