import Mathlib

namespace FormalMathKB

theorem linear_equation_solution (a b c x : ℝ) (ha : a ≠ 0)
    (h : a * x + b = c) : x = (c - b) / a := by
  field_simp [ha]
  linarith

theorem vieta_sum (r s : ℝ) :
    let a := 1
    let b := -(r + s)
    let c := r * s
    r + s = -b := by
  simp

theorem difference_of_squares (x y : ℝ) :
    (x - y) * (x + y) = x ^ 2 - y ^ 2 := by ring

end FormalMathKB
