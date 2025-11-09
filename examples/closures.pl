let make_adder = fn(x) {
    return fn(y) { x + y; };
};

let add2 = make_adder(2);
add2(3);
