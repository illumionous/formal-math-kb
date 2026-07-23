import Mathlib

namespace FormalMathKB

theorem square_nonnegative (x : ℝ) : 0 ≤ x ^ 2 := by positivity

theorem quadratic_vertex_form (x h k : ℝ) :
    x ^ 2 - 2 * h * x + h ^ 2 + k = (x - h) ^ 2 + k := by ring

end FormalMathKB
