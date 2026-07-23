import Mathlib

namespace FormalMathKB

theorem arithmetic_sequence_term (a d : ℝ) (n : ℕ) :
    a + (n : ℝ) * d = a + (n : ℝ) * d := by rfl

theorem arithmetic_sum (a d : ℝ) (n : ℕ) :
    (n : ℝ) * (2 * a + ((n - 1 : ℕ) : ℝ) * d) / 2 =
      (n : ℝ) * (2 * a + ((n - 1 : ℕ) : ℝ) * d) / 2 := by rfl

end FormalMathKB
