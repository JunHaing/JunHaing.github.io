"""
메인 자동화 스크립트.

실행 방법:
  python auto_post.py              # 오늘 키워드로 자동 선택
  python auto_post.py "키워드"     # 직접 키워드 지정
"""
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# .env 로드 (프로젝트 루트)
ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

from collect_trends import get_trending_keywords
from generate_post import generate_post, make_slug


POSTS_DIR = ROOT / "_posts"


def git_push(file_path: Path, title: str) -> bool:
    """새 포스트를 git commit 후 push합니다."""
    commands = [
        ["git", "-C", str(ROOT), "add", str(file_path)],
        ["git", "-C", str(ROOT), "commit", "-m", f"post: {title}"],
        ["git", "-C", str(ROOT), "push"],
    ]
    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[오류] {' '.join(cmd)}\n{result.stderr}")
            return False
    return True


def already_posted_today() -> bool:
    """오늘 날짜 파일이 이미 있으면 True."""
    today = datetime.now().strftime("%Y-%m-%d")
    return any(POSTS_DIR.glob(f"{today}-*.md"))


def main():
    print(f"\n{'='*50}")
    print(f"자동 포스팅 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    # 중복 방지 (하루 1개)
    if already_posted_today() and "--force" not in sys.argv:
        print("오늘은 이미 포스팅했습니다. 강제 실행: --force 옵션 사용")
        sys.exit(0)

    # 키워드 결정
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        keyword = sys.argv[1]
        print(f"지정 키워드: {keyword}")
    else:
        keywords = get_trending_keywords()
        keyword = keywords[0]
        print(f"자동 선택 키워드: {keyword}")

    # 글 생성
    print("\n Claude API로 글 생성 중...")
    content, title = generate_post(keyword)
    if not content:
        print("[오류] 글 생성 실패")
        sys.exit(1)
    print(f"제목: {title}")

    # 파일 저장
    POSTS_DIR.mkdir(exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = make_slug(keyword)
    filename = f"{date_str}-{slug}.md"
    file_path = POSTS_DIR / filename

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"파일 저장: {file_path.name}")

    # Git push
    print("\n GitHub에 업로드 중...")
    if git_push(file_path, title):
        print(f"\n완료! 약 2~5분 후 아래 주소에서 확인하세요:")
        print(f"https://JunHaing.github.io/{date_str.replace('-', '/')}/{slug}/")
    else:
        print(f"\n[주의] Git push 실패. 파일은 저장됨: {file_path}")
        print("수동으로 push 해주세요: git push")

    print(f"\n{'='*50}\n")


if __name__ == "__main__":
    main()
