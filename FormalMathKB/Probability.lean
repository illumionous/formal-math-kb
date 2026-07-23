import Mathlib

namespace FormalMathKB

theorem complement_probability (p : ℝ) : 1 - (1 - p) = p := by ring

theorem equally_likely_probability (favourable total : ℕ) (h : total ≠ 0) :
    (favourable : ℚ) / total * total = favourable := by
  have hn : (total : ℚ) ≠ 0 := by exact_mod_cast h
  field_simp [hn]

end FormalMathKB
