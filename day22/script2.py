from day22.script1 import parse

DECK_SIZE = 119315717514047
SHUFFLES = 101741582076661


def find_coef(techniques):
    # after each technique : original_pos = a * final_pos + b
    (a, b) = (1, 0)
    for technique in techniques:
        if technique.name == "new stack":
            a = - a
            b = - b - 1
        elif technique.name == "cut":
            b = b + technique.count
        else:
            # final_pos = original_pos * count  [DECK_SIZE]
            # Since DECK_SIZE is prime, we use the modular inverse :  inv_count * count = 1 [DECK_SIZE]
            # This gives : original_pos = final_pos * inv_count [DECK_SIZE]
            # inv_count is given by Fermat's little theorem :
            #             count^DECK_SIZE       = count  [DECK_SIZE]
            #  =>         count^(DECK_SIZE - 1) = 1      [DECK_SIZE]
            #  => count * count^(DECK_SIZE - 2) = 1      [DECK_SIZE]
            #  => inv_count = count^(DECK_SIZE - 2)
            inv_count = pow(technique.count, DECK_SIZE - 2, DECK_SIZE)
            a = a * inv_count
            b = b * inv_count
    return a % DECK_SIZE, b % DECK_SIZE


def polynom_power(a, b, p):
    # We need to apply a linear function p times in a row
    # f(x) = ax + b
    # f2(x) = f(f(x)) = a(ax + b) + b = aax + ab + b
    # This means that at each step, the coefs of f(Ax + B) will be (a * A, a * B + b)
    #
    # Since SHUFFLES is very big, we need to optimize it a bit
    # We use "Exponentiation by squaring" :
    #  - if p is odd, apply the above rule
    #  - if p is even, use f^2k(x) = fk(f2(x)) = fk(aax + ab + b)
    #    This gives us a log complexity instead of linear

    if p == 1:
        return a, b
    if p % 2 == 0:
        # Exponentiation by squaring
        a1 = (a * a) % DECK_SIZE
        b1 = (b + a * b) % DECK_SIZE
        return polynom_power(a1, b1, p // 2)
    else:
        a2, b2 = polynom_power(a, b, p-1)
        a1 = (a * a2) % DECK_SIZE
        b1 = (b + a * b2) % DECK_SIZE
        return a1, b1


def solve(techniques):

    # This time we want to find the original position of the card in with final position 2020
    # We want to find a function f so that :  original_pos = f(final_pos)
    #
    # All 3 types of techniques are just linear operations
    # We reverse techniques from last to first to find a and b so that :  original_pos = a * final_pos + b

    techniques = reversed(techniques)
    (a, b) = find_coef(techniques)

    # Now we need to apply this linear function SHUFFLES times
    a_final, b_final = polynom_power(a, b, SHUFFLES)
    return (a_final * 2020 + b_final) % DECK_SIZE


if __name__ == '__main__':
    print(solve(parse("data.txt")))
