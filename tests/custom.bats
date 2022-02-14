load harness

@test "custom-1" {
  check 'x := 1 + 3' '⇒ skip, {x → 4}'
}

@test "custom-2" {
  check 'skip' ''
}

@test "custom-3" {
  check 'while ¬ true do c := x * z' '⇒ skip, {}'
}

@test "custom-4" {
  check 'while x * x < L - a do skip' '⇒ skip, {}'
}

@test "custom-5" {
  check 'while 0 = a * -4 do a := -1' '⇒ a := -1; while (0=(a*-4)) do { a := -1 }, {}
⇒ skip; while (0=(a*-4)) do { a := -1 }, {a → -1}
⇒ while (0=(a*-4)) do { a := -1 }, {a → -1}
⇒ skip, {a → -1}'
}

