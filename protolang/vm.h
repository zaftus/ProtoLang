// vm.h — simple stack machine API
#ifndef PROTOLANG_VM_H
#define PROTOLANG_VM_H

#include <stdint.h>

typedef struct VM VM;
VM *vm_new(const int *constants, int n_constants);
void vm_free(VM *vm);
int vm_run(VM *vm, const uint8_t *instructions, int instr_len);

#endif // PROTOLANG_VM_H
