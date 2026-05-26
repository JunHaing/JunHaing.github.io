"""Claude API를 사용해 SEO 최적화 블로그 포스트를 생성합니다."""
import os
import re
from datetime import datetime

import anthropic


def generate_post(keyword: str) -> tuple[str, str]:
    """
    keyword를 받아 Jekyll front matter가 포함된 마크다운 포스트를 반환합니다.
    Returns: (markdown_content, title)
    """
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    prompt = f"""당신은 한국 SEO 전문 블로그 작성자입니다. 아래 키워드로 실용적인 블로그 포스트를 작성해주세요.

키워드: {keyword}

요구사항:
- 제목: 숫자나 연도 포함, 클릭하고 싶은 제목 (60자 이내)
- 분량: 1,500~2,000자
- 구조: 도입부(2~3문장) → H2 소제목 3~5개 → 핵심 정리
- 키워드를 제목, 소제목, 본문에 자연스럽게 포함
- 표, 목록을 적극 활용해 읽기 쉽게 구성
- 독자가 바로 행동할 수 있는 구체적인 정보 위주
- categories는 [재테크], [정부지원금], [건강], [IT정보], [생활법률] 중 가장 적합한 1개
- tags는 관련 키워드 5개 (쉼표로 구분)
- description은 160자 이내 SEO 메타 설명

반드시 아래 형식으로만 출력하세요 (다른 말 없이):

---
layout: post
title: "제목"
date: {now} +0900
categories: [카테고리]
tags: [태그1, 태그2, 태그3, 태그4, 태그5]
description: "SEO 설명"
---

[본문 내용]
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    content = message.content[0].text.strip()

    title = ""
    for line in content.split("\n"):
        if line.startswith("title:"):
            title = line.replace("title:", "").strip().strip('"')
            break

    return content, title


def make_slug(keyword: str) -> str:
    """키워드를 URL 슬러그로 변환합니다."""
    slug = keyword.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = slug.strip("-")
    if not slug:
        slug = datetime.now().strftime("%H%M%S")
    return slug


if __name__ == "__main__":
    from dotenv import load_dotenv
    from pathlib import Path

    load_dotenv(Path(__file__).parent.parent / ".env")

    test_keyword = "실업급여 신청 조건과 방법"
    print(f"테스트 키워드: {test_keyword}")
    content, title = generate_post(test_keyword)
    print(f"생성된 제목: {title}")
    print("---")
    print(content[:500])
