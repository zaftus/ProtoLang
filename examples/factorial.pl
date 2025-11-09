# factorial.pl  (ProtoLang examples use .pl extension)
let fact = fn(n) {
    if (n) {
        if (n == 0) { return 1; }
        return n * fact(n - 1);
    } else {
        return 1;
    }
};

fact(5);
