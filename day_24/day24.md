# Day 24: Arithmetic Logic Unit

The entire `puzzle_input` is this repeated 13 times (where `[a]`, `[b]`, and `[c]` are values that change each of the 13 times):

```
inp w
mul x 0
add x z
mod x 26
div z [a]
add x [b]
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y [c]
mul y x
add z y
```

We observe the following from the source code:

- Each series of instructions resets the values of w, x, and y. z's value persists across the 14 instructions groupings.
- `[a]` is either 1 or 26, determined by whether `[b]` is positive or negative, respectively.
- When `[b]` is positive, its value is always greater than 9.
- 7 of the repetitions have a positive value of `[b]` (type A), while the other 7 have a negative value (type B).
- The instruction sets with a positive `[b]` value (type A) have an `[a]` value of 1 and the sets with a negative `[b]` value (type B) have an `[a]` value of 26.

This is the decomplied Python version of puzzle code:

```python
w = int(input())
x = int((z % 26) + b == w)
x = int(x == 0)
z //= a
y = 25 * x + 1
z *= y
y += (w + c) * x
z += y
```

This is a simplified decompiled version:

```python
w = int(input())
x = int((z % 26) + b != w)
z //= a
z *= 25 * x + 1
z += (w + c) * x
```

In the type A instruction sets, `[b]` is always between 10 and 16. The line `z //= a` does nothing in type A instruction sets because `z / 1 = z`. Furthermore, the expression `(z % 26) + b != w` will always be true for type A since `z % 26` is not negative, `b > 10`, and submarine model numbers consist only of digits 1 through 9 (so w is between 1 and 9, inclusive). Thus, the value of `x` will always be 1. So, for the type A repetitions, the decompiled code simplifies further to:

```python
w = int(input())
z *= 26
z += w + c
```

All of the operations on `z` involve multiplying, dividing, or modding by 26. Thus, we can think of `z` as being a stack of digits in a base-26 number.

Type B instruction sets (`a` is 26 and `b` is negative) will pop a digit off the stack if the expression `(z % 26) + b != w` is false (so `x` is 0). If `x` is 0 then the code simplifies to:

```python
w = int(input())
z //= 26
```

However, for type B is `x` is 1, then a value will still be popped from the stack but a different value will also be pushed to the stack, similarly to type A.

Thus, the simplified code snippets for type A and B can be interpreted as so:

1. If the segment is type A (`[a]` is 1 and `[b]` is positive), push `input + offset` (`w + c`) onto the stack.
2. If the segment is type B (`[a]` is 26 and `[b]` is negative), pop from the stack. If the popped value plus `[b]` does not equal the input, then push (input + `[c]`) onto the stack. In other words, the previously added value (`p`) plus `[b]` must equal the new input (`w_new`) in order for a push to not execute. Rearranging, we get that `p = w_new - b`, where `p = w_old + c`. So, `w_old + c = w_new - b` must be true for a push to not occur.
3. After all pushes and pops are completed, the submarine model number is valid if the stack is empty.

There are the same number of type A and B instruction sets, so we have the same number of push and pop instructions. If we want our number to be valid, then the stack needs to be empty when the program finishes execution.

The values of `[b]` and `[c]` for the 14 instruction sets in my problem input are:

```
11, 16
12, 11
13, 12
-5, 12
-3, 12
14, 2
15, 11
-16, 4
14, 12
15, 9
-7, 10
-11, 11
-6, 6
-11, 15
```

Translated into the interpretation above, these numbers mean the following:

```
PUSH input[0] + 16
PUSH input[1] + 11
PUSH input[2] + 12
POP. Must have input[3] == popped_value - 5
POP. Must have input[4] == popped_value - 3
PUSH input[5] + 2
PUSH input[6] + 11
POP. Must have input[7] == popped_value - 16
PUSH input[8] + 12
PUSH input[9] + 9
POP. Must have input[10] == popped_value - 7
POP. Must have input[11] == popped_value - 11
POP. Must have input[12] == popped_value - 6
POP. Must have input[13] == popped_value - 11
```

Since `popped_value` is simply the previous pushed input value plus `c` (`popped_value = input[idx-1] + c`), we can formulate the following set of requirements:

```
input[3] == input[2] + 7
input[4] == input[1] + 8
input[7] == input[6] - 5
input[10] == input[9] + 2
input[11] == input[8] + 1
input[12] == input[5] - 4
input[13] == input[0] + 5
```

From this point it is easy to compute the largest and smallest possible number that satisfies these requirements. For example, to find the largest number, the first rule, `input[3] == input[2] + 7`, means that the 3rd digit should be a 9 (the largest allowable digit) and the 2nd digit should be `9 - 7 = 2` (0-indexed). The third rule, `input[7] == input[6] - 5`, means that the 6th digit should be a 9 and the 7th should be `9 - 5 = 4`. When finding the smallest value, simply work in the opposite direction. For instance, the first rule, `input[3] == input[2] + 7`, when finding the smallest number, means that the 2nd digit is a 1 (the smallest allowable digit) and the 3rd is `1 + 7 = 8`.

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|----|----|----|----|
| 4 | 1 | 2 | 9 | 9 | 9 | 9 | 4 | 8 | 7 | 9  | 9  | 5  | 9  |

The **largest** model number accepted by MONAD is as follows: `41299994879959`

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|----|----|----|----|
| 1 | 1 | 1 | 8 | 9 | 5 | 6 | 1 | 1 | 1 | 3  | 2  | 1  | 6  |

The **smallest** model number accepted by MONAD is as follows: `11189561113216`

For more information or if you still do not understand, try following [this guide](https://github.com/dphilipson/advent-of-code-2021/blob/master/src/days/day24.rs).
