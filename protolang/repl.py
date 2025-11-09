# repl.py — read-eval-print for protolang
import sys
from protolang.lexer import Lexer
from protolang.parser import Parser
from protolang.compiler import Compiler
import os
import subprocess

PROMPT = 'pl> '

VM_PATH = os.path.join(os.path.dirname(__file__), 'vm')

def _write_instructions(path, instructions: bytes):
    with open(path, 'wb') as f:
        f.write(instructions)

def _write_constants(path, consts):
    # write as 32-bit signed big-endian ints
    with open(path, 'wb') as f:
        for c in consts:
            f.write(int(c).to_bytes(4,'big',signed=True))

def _run_vm(instr_path, consts_path):
    if not os.path.exists(VM_PATH):
        print('VM not built. Run `make build` or build with gcc protolang/vm.c')
        return
    # VM expects two args: instructions_file constants_file
    proc = subprocess.run([VM_PATH, instr_path, consts_path], capture_output=True, text=True)
    print(proc.stdout, end='')
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)

def start():
    print('ProtoLang REPL (type .exit to quit)')
    while True:
        try:
            line = input(PROMPT)
        except EOFError:
            break
        if not line: continue
        if line.strip() == '.exit': break
        lexer = Lexer(line)
        parser = Parser(lexer)
        program = parser.parse_program()
        comp = Compiler(); comp.compile(program)
        instructions, consts = comp.bytecode()
        instr_path = '/tmp/pl_instructions.bin'
        consts_path = '/tmp/pl_consts.bin'
        _write_instructions(instr_path, instructions)
        _write_constants(consts_path, consts)
        _run_vm(instr_path, consts_path)

if __name__ == '__main__':
    start()
