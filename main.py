"""
Hệ Thống Quản Lý Giải Đấu Rikkei Esports
==========================================
Module chính xử lý toàn bộ nghiệp vụ quản lý trận đấu:
- Hiển thị lịch thi đấu
- Thêm trận đấu mới
- Cập nhật tỷ số
- Báo cáo thống kê
- Logging toàn diện ra file tournament_app.log
"""

import logging

# ─── CẤU HÌNH LOGGING ────────────────────────────────────────────────────────
logging.basicConfig(
    filename="tournament_app.log",
    level=logging.DEBUG,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)


# ─── DỮ LIỆU MẪU ─────────────────────────────────────────────────────────────
matches = [
    {
        "match_id": "M01",
        "team_a": "T1",
        "team_b": "GenG",
        "score_a": 2,
        "score_b": 1,
        "status": "Completed",
    },
    {
        "match_id": "M02",
        "team_a": "JDG",
        "team_b": "BLG",
        "score_a": 0,
        "score_b": 0,
        "status": "Pending",
    },
]


# ─── HÀM PHỤ TRỢ ─────────────────────────────────────────────────────────────

def determine_winner(match: dict) -> str:
    """
    Xác định đội thắng của một trận đấu đã hoàn thành.

    Args:
        match (dict): Dictionary chứa thông tin một trận đấu.
                      Phải có các key: status, team_a, team_b, score_a, score_b.

    Returns:
        str: Tên đội thắng, "Draw" nếu hòa, hoặc "Not Started" nếu chưa diễn ra.
    """
    if match["status"] == "Pending":
        return "Not Started"

    try:
        score_a = match["score_a"]
        score_b = match["score_b"]
    except KeyError as error:
        logger.error("Missing key in match dictionary: %s", error)
        return "Lỗi dữ liệu"

    if score_a > score_b:
        return match["team_a"]
    elif score_b > score_a:
        return match["team_b"]
    else:
        return "Draw"


def find_match_by_id(match_list: list, match_id: str) -> dict | None:
    """
    Tìm kiếm trận đấu trong danh sách theo mã trận.

    Args:
        match_list (list): Danh sách các dictionary trận đấu.
        match_id (str): Mã trận đấu cần tìm.

    Returns:
        dict | None: Dictionary của trận đấu nếu tìm thấy, None nếu không.
    """
    for match in match_list:
        if match["match_id"] == match_id:
            return match
    return None


def input_valid_score(prompt: str) -> int:
    """
    Yêu cầu người dùng nhập điểm số hợp lệ (số nguyên >= 0).
    Lặp lại cho đến khi nhận được giá trị đúng.

    Args:
        prompt (str): Dòng chữ hiển thị khi yêu cầu nhập.

    Returns:
        int: Điểm số hợp lệ do người dùng nhập.
    """
    while True:
        raw_input = input(prompt)
        try:
            score = int(raw_input)
            if score < 0:
                logger.error("Negative score input detected: %s", raw_input)
                print("Điểm số phải lớn hơn hoặc bằng 0.")
                continue
            return score
        except ValueError as error:
            logger.error("Invalid score input. Error: %s", error)
            print("Điểm số phải là số nguyên. Vui lòng nhập lại.")


# ─── CHỨC NĂNG 1: HIỂN THỊ LỊCH THI ĐẤU ────────────────────────────────────

def display_matches(match_list: list) -> None:
    """
    Hiển thị toàn bộ lịch thi đấu và kết quả theo định dạng cột.

    Args:
        match_list (list): Danh sách các dictionary trận đấu.

    Returns:
        None
    """
    logger.info("User viewed the match list.")

    if not match_list:
        print("Hiện chưa có trận đấu nào trong hệ thống.")
        return

    print("\n--- LỊCH THI ĐẤU & KẾT QUẢ ---")
    header = f"{'Mã trận':<10}| {'Đội A':<16}| {'Đội B':<16}| {'Tỷ số':<8}| {'Trạng thái'}"
    print(header)
    print("-" * 70)

    for match in match_list:
        try:
            score_display = f"{match['score_a']}-{match['score_b']}"
            print(
                f"{match['match_id']:<10}| "
                f"{match['team_a']:<16}| "
                f"{match['team_b']:<16}| "
                f"{score_display:<8}| "
                f"{match['status']}"
            )
        except KeyError as error:
            logger.error("Missing key when displaying match: %s", error)
            print(f"  [Lỗi hiển thị trận đấu: thiếu trường {error}]")


# ─── CHỨC NĂNG 2: THÊM TRẬN ĐẤU MỚI ────────────────────────────────────────

def add_match(match_list: list) -> None:
    """
    Thu thập thông tin từ người dùng và thêm trận đấu mới vào danh sách.
    Kiểm tra trùng mã trận và tên đội rỗng.

    Args:
        match_list (list): Danh sách các dictionary trận đấu (được cập nhật trực tiếp).

    Returns:
        None
    """
    print("\n--- THÊM TRẬN ĐẤU MỚI ---")

    match_id = input("Nhập mã trận đấu: ").strip()
    if not match_id:
        print("Mã trận đấu không được để trống.")
        logger.warning("User tried to add a match with empty match ID.")
        return

    if find_match_by_id(match_list, match_id):
        print(f"Lỗi: Mã trận đấu {match_id} đã tồn tại.")
        logger.warning("Match ID %s already exists.", match_id)
        return

    team_a = input("Nhập tên Đội A: ").strip()
    if not team_a:
        print("Tên đội không được để trống.")
        logger.warning("User tried to add a match with empty team name.")
        return

    team_b = input("Nhập tên Đội B: ").strip()
    if not team_b:
        print("Tên đội không được để trống.")
        logger.warning("User tried to add a match with empty team name.")
        return

    new_match = {
        "match_id": match_id,
        "team_a": team_a,
        "team_b": team_b,
        "score_a": 0,
        "score_b": 0,
        "status": "Pending",
    }
    match_list.append(new_match)

    print(f"\nThành công: Đã thêm trận đấu {match_id}.")
    logger.info("Match %s added successfully", match_id)


# ─── CHỨC NĂNG 3: CẬP NHẬT TỶ SỐ ───────────────────────────────────────────

def update_score(match_list: list) -> None:
    """
    Cập nhật tỷ số cho một trận đấu theo mã trận.
    Bẫy lỗi nhập chữ và điểm âm. Xác nhận thủ công nếu tỷ số là 0-0.

    Args:
        match_list (list): Danh sách các dictionary trận đấu (được cập nhật trực tiếp).

    Returns:
        None
    """
    print("\n--- CẬP NHẬT TỶ SỐ TRẬN ĐẤU ---")

    match_id = input("Nhập mã trận đấu cần cập nhật: ").strip()
    target_match = find_match_by_id(match_list, match_id)

    if not target_match:
        print(f"Không tìm thấy trận đấu mang mã {match_id}.")
        logger.warning("User tried to update non-existing match %s", match_id)
        return

    print(
        f"\nTrận đấu: {target_match['team_a']} vs "
        f"{target_match['team_b']} ({target_match['status']})"
    )

    score_a = input_valid_score(f"Nhập điểm {target_match['team_a']}: ")
    score_b = input_valid_score(f"Nhập điểm {target_match['team_b']}: ")

    # ── Edge Case: Tỷ số 0-0 cần trọng tài xác nhận (Bẫy 1) ──
    if score_a == 0 and score_b == 0:
        confirmation = input(
            "\nTỷ số đang là 0-0. Trọng tài có xác nhận trận đã hoàn thành không? (y/n): "
        ).strip().lower()
        new_status = "Completed" if confirmation == "y" else "Pending"
    else:
        new_status = "Completed"

    target_match["score_a"] = score_a
    target_match["score_b"] = score_b
    target_match["status"] = new_status

    print(f"\nThành công: Đã cập nhật tỷ số trận đấu {match_id}.")
    logger.info("Match %s score updated successfully", match_id)


# ─── CHỨC NĂNG 4: BÁO CÁO THỐNG KÊ ─────────────────────────────────────────

def generate_report(match_list: list) -> None:
    """
    Tạo báo cáo thống kê các trận đấu đã hoàn thành và kết quả thắng/thua/hòa.

    Args:
        match_list (list): Danh sách các dictionary trận đấu.

    Returns:
        None
    """
    logger.info("User generated tournament report.")
    print("\n--- BÁO CÁO THỐNG KÊ GIẢI ĐẤU ---")

    completed_matches = [m for m in match_list if m["status"] == "Completed"]

    if not completed_matches:
        print("Chưa có trận đấu nào hoàn thành.")
        print("Tổng số trận đã hoàn thành: 0")
        return

    for match in completed_matches:
        winner = determine_winner(match)
        print(
            f"{match['match_id']}: {match['team_a']} "
            f"{match['score_a']}-{match['score_b']} "
            f"{match['team_b']} | Kết quả: {winner}"
        )

    print(f"\nTổng số trận đã hoàn thành: {len(completed_matches)}")


# ─── VÒNG LẶP MENU CHÍNH ─────────────────────────────────────────────────────

def show_menu() -> None:
    """In ra menu chính của hệ thống."""
    print("\n===== HỆ THỐNG QUẢN LÝ GIẢI ĐẤU RIKKEI ESPORTS =====")
    print("1. Hiển thị lịch thi đấu & Kết quả")
    print("2. Thêm trận đấu mới")
    print("3. Cập nhật tỷ số trận đấu")
    print("4. Báo cáo thống kê")
    print("5. Thoát chương trình")
    print("=" * 50)


def run_application() -> None:
    """
    Vòng lặp chính của ứng dụng. Hiển thị menu và điều phối
    các chức năng dựa trên lựa chọn của người dùng.

    Returns:
        None
    """
    logger.info("Tournament management system started.")

    while True:
        show_menu()
        user_choice = input("Chọn chức năng (1-5): ").strip()

        if user_choice == "1":
            display_matches(matches)

        elif user_choice == "2":
            add_match(matches)

        elif user_choice == "3":
            update_score(matches)

        elif user_choice == "4":
            generate_report(matches)

        elif user_choice == "5":
            print("Đang thoát hệ thống. Tạm biệt!")
            logger.info("Tournament management system closed by user.")
            break

        else:
            # Bẫy 2: Lựa chọn ngoài phạm vi 1-5
            print("Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 5.")
            logger.warning("Invalid menu choice selected: '%s'", user_choice)


# ─── ĐIỂM KHỞI CHẠY ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_application()