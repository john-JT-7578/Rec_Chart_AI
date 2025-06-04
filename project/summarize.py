import openai

SYSTEM_PROMPT_EN = (
    "Summarize the following transcript into a professional, recruiter-style note.\n"
    "Use clear section headers and bullet points. Write in full sentences. Include only information the candidate actually said."
)

SYSTEM_PROMPT_KO = (
    "다음 인터뷰 내용을 전문적인 리크루터 메모 형식으로 정리해 주세요.\n"
    "명확한 섹션 헤더와 불릿 포인트를 사용하고, 후보자가 실제로 언급한 내용만 포함하세요."
)


def summarize(transcript: str, language: str = 'English') -> str:
    prompt = SYSTEM_PROMPT_EN if language == 'English' else SYSTEM_PROMPT_KO
    prompt += '\n\nTranscript:\n' + transcript
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.3,
    )
    return response['choices'][0]['message']['content'].strip()
