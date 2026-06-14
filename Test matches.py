import unittest
from main import determine_winner


class TestDetermineWinner(unittest.TestCase):
    """Test suite cho hàm determine_winner."""

    # ── Test Case 1: Đội A thắng ──────────────────────────────────────────────
    def test_team_a_wins(self):
        """Trả về tên Đội A khi Đội A có điểm cao hơn."""
        match = {
            "match_id": "M01",
            "team_a": "T1",
            "team_b": "GenG",
            "score_a": 2,
            "score_b": 0,
            "status": "Completed",
        }
        result = determine_winner(match)
        self.assertEqual(result, "T1")

    # ── Test Case 2: Đội B thắng ──────────────────────────────────────────────
    def test_team_b_wins(self):
        """Trả về tên Đội B khi Đội B có điểm cao hơn."""
        match = {
            "match_id": "M02",
            "team_a": "JDG",
            "team_b": "BLG",
            "score_a": 0,
            "score_b": 3,
            "status": "Completed",
        }
        result = determine_winner(match)
        self.assertEqual(result, "BLG")

    # ── Test Case 3: Hòa ──────────────────────────────────────────────────────
    def test_draw(self):
        """Trả về 'Draw' khi hai đội có điểm bằng nhau."""
        match = {
            "match_id": "M03",
            "team_a": "G2",
            "team_b": "FNC",
            "score_a": 1,
            "score_b": 1,
            "status": "Completed",
        }
        result = determine_winner(match)
        self.assertEqual(result, "Draw")

    # ── Test Case 4: Trận chưa diễn ra (Pending) ──────────────────────────────
    def test_pending_match(self):
        """Trả về 'Not Started' khi trận đấu có status là 'Pending'."""
        match = {
            "match_id": "M04",
            "team_a": "C9",
            "team_b": "100T",
            "score_a": 0,
            "score_b": 0,
            "status": "Pending",
        }
        result = determine_winner(match)
        self.assertEqual(result, "Not Started")

    # ── Test Case 5: Hòa 0-0 đã xác nhận Completed ───────────────────────────
    def test_completed_draw_zero_zero(self):
        """Trả về 'Draw' khi tỷ số 0-0 nhưng trọng tài đã xác nhận Completed."""
        match = {
            "match_id": "M05",
            "team_a": "NRG",
            "team_b": "EG",
            "score_a": 0,
            "score_b": 0,
            "status": "Completed",
        }
        result = determine_winner(match)
        self.assertEqual(result, "Draw")

    # ── Test Case 6: Bẫy 3 — Thiếu key score_a / score_b ────────────────────
    def test_missing_score_key_returns_error_string(self):
        """Trả về chuỗi báo lỗi khi dictionary thiếu key score_a hoặc score_b."""
        match = {
            "match_id": "M06",
            "team_a": "TSM",
            "team_b": "CLG",
            # score_a và score_b bị thiếu — mô phỏng API trả về dữ liệu lỗi
            "status": "Completed",
        }
        result = determine_winner(match)
        self.assertEqual(result, "Lỗi dữ liệu")


if __name__ == "__main__":
    unittest.main(verbosity=2)