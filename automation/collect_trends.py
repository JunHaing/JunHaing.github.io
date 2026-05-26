"""날짜 기반으로 주제를 순환하면서 키워드를 반환합니다."""
from datetime import date


KEYWORD_POOL = {
    "재테크": [
        "2026 청년도약계좌 신청방법",
        "월배당 ETF 추천 2026",
        "주식 초보 시작하는법",
        "ISA 계좌 개설 방법과 혜택",
        "적금 금리 비교 2026",
        "개인연금 IRP 가입 방법",
        "코인 세금 신고 방법",
    ],
    "정부지원금": [
        "2026 청년 월세 지원금 신청 방법",
        "에너지바우처 신청 방법",
        "소상공인 지원금 2026",
        "실업급여 신청 조건과 방법",
        "국민내일배움카드 신청방법",
        "근로장려금 신청 대상",
        "청년 전세자금대출 조건",
    ],
    "건강": [
        "혈당 낮추는 음식 추천",
        "고혈압 낮추는 생활 습관",
        "다이어트 식단 1주일 계획",
        "수면의 질 높이는 방법",
        "피로 회복에 좋은 음식",
        "허리 디스크 스트레칭",
        "콜레스테롤 낮추는 방법",
    ],
    "IT정보": [
        "ChatGPT 활용법 초보 가이드",
        "유용한 앱 추천 2026",
        "스마트폰 배터리 오래쓰는 법",
        "구글 드라이브 100% 활용법",
        "무료로 쓸 수 있는 OTT",
        "유튜브 프리미엄 저렴하게 이용하는 법",
        "스마트폰 저장공간 확보 방법",
    ],
    "생활법률세금": [
        "퇴직금 계산 방법과 지급 기준",
        "전세 계약 주의사항 체크리스트",
        "연말정산 환급 많이 받는 법",
        "종합소득세 신고 방법 쉽게",
        "실손보험 청구 방법",
        "임대차 계약 갱신 거절 조건",
        "중고차 구매 시 주의사항",
    ],
}


def get_keyword() -> str:
    """날짜 기반으로 카테고리와 키워드를 자동 순환합니다."""
    today = date.today()
    day_of_year = today.timetuple().tm_yday

    categories = list(KEYWORD_POOL.keys())
    category = categories[day_of_year % len(categories)]
    keywords = KEYWORD_POOL[category]
    keyword = keywords[(day_of_year // len(categories)) % len(keywords)]

    return keyword


def get_trending_keywords() -> list[str]:
    """메인 키워드와 같은 카테고리 키워드를 반환합니다."""
    today = date.today()
    day_of_year = today.timetuple().tm_yday

    categories = list(KEYWORD_POOL.keys())
    category = categories[day_of_year % len(categories)]
    keywords = KEYWORD_POOL[category]

    main_idx = (day_of_year // len(categories)) % len(keywords)
    main_keyword = keywords[main_idx]
    backups = [k for i, k in enumerate(keywords) if i != main_idx]

    return [main_keyword] + backups[:3]


if __name__ == "__main__":
    keywords = get_trending_keywords()
    print(f"오늘의 키워드: {keywords[0]}")
    print(f"백업 키워드: {keywords[1:]}")
