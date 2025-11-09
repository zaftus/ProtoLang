// vm.c — small register/stack VM implementation (updated to accept files)
#include "vm.h"
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

struct VM { 
    int *constants;
    int n_constants;
    int *stack;
    int sp;
};

VM *vm_new(const int *constants, int n_constants) {
    VM *vm = malloc(sizeof(VM));
    vm->constants = malloc(sizeof(int)*n_constants);
    for (int i=0;i<n_constants;i++) vm->constants[i]=constants[i];
    vm->n_constants = n_constants;
    vm->stack = malloc(sizeof(int)*2048);
    vm->sp = 0;
    return vm;
}

void vm_free(VM *vm) {
    free(vm->constants);
    free(vm->stack);
    free(vm);
}

int vm_run(VM *vm, const uint8_t *instructions, int instr_len) {
    int ip = 0;
    while (ip < instr_len) {
        uint8_t op = instructions[ip++];
        switch (op) {
            case 1: { // CONST
                int idx = (instructions[ip] << 8) | instructions[ip+1]; ip += 2;
                vm->stack[vm->sp++] = vm->constants[idx];
                break;
            }
            case 6: { // POP
                vm->sp--; break;
            }
            case 8: { // RETURN
                int val = vm->stack[--vm->sp];
                printf("<< return %d >>\n", val);
                return 0;
            }
            default:
                fprintf(stderr, "unknown opcode %d\n", op);
                return 1;
        }
    }
    return 0;
}

// helper to read constants from file (32-bit big-endian ints)
static int *read_constants(const char *path, int *out_n) {
    FILE *f = fopen(path, "rb");
    if (!f) return NULL;
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    int n = sz / 4;
    int *arr = malloc(sizeof(int)*n);
    for (int i=0;i<n;i++) {
        unsigned char buf[4];
        fread(buf,1,4,f);
        int v = (buf[0]<<24)|(buf[1]<<16)|(buf[2]<<8)|buf[3];
        arr[i] = v;
    }
    fclose(f);
    *out_n = n;
    return arr;
}

static uint8_t *read_instructions(const char *path, int *out_sz) {
    FILE *f = fopen(path, "rb");
    if (!f) return NULL;
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    uint8_t *buf = malloc(sz);
    fread(buf,1,sz,f);
    fclose(f);
    *out_sz = (int)sz;
    return buf;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <instructions.bin> <constants.bin>\n", argv[0]);
        return 2;
    }
    int n_consts = 0;
    int *consts = read_constants(argv[2], &n_consts);
    if (!consts) { fprintf(stderr, "failed to read constants\n"); return 2; }
    int instr_len = 0;
    uint8_t *instr = read_instructions(argv[1], &instr_len);
    if (!instr) { fprintf(stderr, "failed to read instructions\n"); free(consts); return 2; }

    VM *vm = vm_new(consts, n_consts);
    int res = vm_run(vm, instr, instr_len);
    vm_free(vm);
    free(instr);
    free(consts);
    return res;
}
