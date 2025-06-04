# Tasks
- [x] 프로젝트 기본 구조 생성 및 모듈 작성
- [x] 실시간 오디오 스트림 개선 및 자동 요약 주기적 실행 기능 개발
- [x] UI 한국어/영어 선택 고도화 및 추가 기능 구현

# Updates
- 초기 코드 및 requirements.txt 추가
- 실시간 스트리밍 및 UI 개선 완료
- 의존성 미설치로 실시간 테스트 진행 불가
- OpenAI Whisper 패키지명을 `openai-whisper`로 수정해 잘못된 의존성 오류 해결

# Error
- 환경에 sounddevice, openai 등 라이브러리가 없어 실시간 전사 및 요약 테스트 실패
- whisper 패키지 충돌로 실행 오류 발생 (해결: `openai-whisper`로 교체)