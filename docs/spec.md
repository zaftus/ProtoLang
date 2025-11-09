# ProtoLang Language Specification (short)

## Types
- int
- bool
- string
- function
- array
- hash

## Expressions
- literals: `1`, `"hi"`, `true`
- identifiers
- function literals: `fn(x,y) { ... }`
- call expressions: `f(1,2)`
- if expressions: `if (cond) { ... } else { ... }`

## Statements
- `let` bindings: `let x = 5;`
- `return` statements

## Semantics
Small-step semantics; function calls create closures and capture lexical environment.
