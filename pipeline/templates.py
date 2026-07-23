from __future__ import annotations

import random
from collections.abc import Callable

from .models import SFTExample

Generator = Callable[[random.Random], SFTExample]


def _lean_int(value: int) -> str:
    return f"({value} : ℤ)" if value < 0 else str(value)


def linear_equation(rng: random.Random) -> SFTExample:
    coefficient = rng.choice([n for n in range(-9, 10) if n != 0])
    solution = rng.randint(-12, 12)
    offset = rng.randint(-20, 20)
    result = coefficient * solution + offset
    a, b, c, x = map(_lean_int, (coefficient, offset, result, solution))
    return SFTExample(
        instruction=f"Solve the equation {coefficient}x + {offset} = {result} over the integers.",
        reasoning=(
            f"Subtract {offset} from both sides to obtain {coefficient}x = {result - offset}. "
            f"Divide by the nonzero coefficient {coefficient}, giving x = {solution}."
        ),
        answer=f"x = {solution}",
        kb_ids=["alg.linear.solve"],
        formal_proof=f"example (y : ℤ) (h : {a} * y + {b} = {c}) : y = {x} := by omega",
        difficulty=1,
    )


def arithmetic_sequence(rng: random.Random) -> SFTExample:
    first = rng.randint(-10, 15)
    difference = rng.choice([n for n in range(-7, 8) if n != 0])
    index = rng.randint(3, 20)
    value = first + (index - 1) * difference
    return SFTExample(
        instruction=(
            f"An arithmetic sequence has first term {first} and common difference {difference}. "
            f"Find its {index}th term."
        ),
        reasoning=f"Use a_n = a_1 + (n-1)d. Thus a_{index} = {first} + {index - 1}({difference}) = {value}.",
        answer=str(value),
        kb_ids=["seq.arithmetic.term"],
        formal_proof=(
            f"example : ({_lean_int(first)}) + ({index} - 1) * ({_lean_int(difference)}) = "
            f"{_lean_int(value)} := by norm_num"
        ),
        difficulty=1,
    )


def quadratic_roots(rng: random.Random) -> SFTExample:
    first_root = rng.randint(-8, 8)
    second_root = rng.randint(-8, 8)
    linear = -(first_root + second_root)
    constant = first_root * second_root
    root_sum = first_root + second_root
    return SFTExample(
        instruction=f"Find the sum of the roots of x^2 + ({linear})x + ({constant}) = 0.",
        reasoning=f"For x^2 + bx + c = 0, Vieta's formula gives r_1+r_2=-b. Hence the sum is {-linear}.",
        answer=str(root_sum),
        kb_ids=["alg.identity.difference_squares", "alg.quadratic.vieta"],
        formal_proof=(
            f"example : -({_lean_int(linear)}) = {_lean_int(root_sum)} ∧ "
            f"({_lean_int(first_root)}) * ({_lean_int(second_root)}) = {_lean_int(constant)} := by norm_num"
        ),
        difficulty=2,
    )


def pythagorean_triple(rng: random.Random) -> SFTExample:
    scale = rng.randint(1, 10)
    first, second, hypotenuse = 3 * scale, 4 * scale, 5 * scale
    return SFTExample(
        instruction=f"A right triangle has legs {first} and {second}. Find the hypotenuse.",
        reasoning=f"By the Pythagorean theorem, c^2={first}^2+{second}^2={hypotenuse ** 2}, so c={hypotenuse}.",
        answer=str(hypotenuse),
        kb_ids=["geom.right_triangle.pythagorean"],
        formal_proof=f"example : ({first} : ℕ)^2 + {second}^2 = {hypotenuse}^2 := by norm_num",
        difficulty=1,
    )


def complementary_probability(rng: random.Random) -> SFTExample:
    denominator = rng.choice([4, 5, 8, 10, 20])
    numerator = rng.randint(1, denominator - 1)
    complement = denominator - numerator
    return SFTExample(
        instruction=f"If P(A) = {numerator}/{denominator}, find P(A^c).",
        reasoning=f"A complementary event has probability 1-P(A), so P(A^c)=1-{numerator}/{denominator}={complement}/{denominator}.",
        answer=f"{complement}/{denominator}",
        kb_ids=["prob.event.complement"],
        formal_proof=(
            f"example : 1 - ({numerator} : ℚ) / {denominator} = {complement} / {denominator} := by norm_num"
        ),
        difficulty=1,
    )


GENERATORS: tuple[Generator, ...] = (
    linear_equation,
    arithmetic_sequence,
    quadratic_roots,
    pythagorean_triple,
    complementary_probability,
)
