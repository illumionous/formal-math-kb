import Mathlib

namespace FormalMathKB

theorem sin_sq_add_cos_sq (x : ℝ) : Real.sin x ^ 2 + Real.cos x ^ 2 = 1 := by
  simpa [pow_two] using Real.sin_sq_add_cos_sq x

end FormalMathKB
