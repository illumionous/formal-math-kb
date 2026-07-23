import Mathlib

namespace FormalMathKB

theorem pythagorean_triple_3_4_5 : (3 : ℝ) ^ 2 + 4 ^ 2 = 5 ^ 2 := by norm_num

theorem triangle_angle_sum (a b c : ℝ) (h : a + b + c = 180) : a + b = 180 - c := by linarith

end FormalMathKB
