#!/usr/bin/env python3
"""
Beluga CLI 모듈
설문 문항 생성 및 관리 라이브러리의 명령줄 인터페이스
"""

import sys
import argparse
from . import __version__

def main():
    """Beluga CLI 메인 함수"""
    parser = argparse.ArgumentParser(
        description="Beluga - 설문 문항 생성 및 관리 라이브러리",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  beluga version          # 버전 정보 출력
  beluga help            # 도움말 출력
  beluga info            # 라이브러리 정보 출력
        """
    )

    parser.add_argument(
        'command',
        nargs='?',
        default='help',
        choices=['version', 'help', 'info'],
        help='실행할 명령어'
    )

    args = parser.parse_args()

    if args.command == "version":
        print(f"Beluga v{__version__}")
    elif args.command == "help":
        parser.print_help()
    elif args.command == "info":
        print("Beluga - 설문 문항 생성 및 관리 라이브러리")
        print(f"버전: {__version__}")
        print("기능:")
        print("  - 다양한 유형의 설문 문항 생성")
        print("  - DataFrame 기반 문항 관리")
        print("  - Excel 파일로 내보내기")
        print("  - 조건부 로직 및 파이핑 지원")
    else:
        print(f"알 수 없는 명령어: {args.command}")
        sys.exit(1)

if __name__ == "__main__":
    main()