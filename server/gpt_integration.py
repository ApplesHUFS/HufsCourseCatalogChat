from typing import List, Dict, Any
from openai import OpenAI
import os
from search import hybrid_search
from utils import MAX_CONTEXT_LENGTH
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT_TEMPLATE = """
You are an intelligent assistant who helps users with their questions about university course information.
Strictly use ONLY the following pieces of context to answer the question at the end. Think step-by-step and then answer in Korean. Extract and analyze the relevant passages from the context before answering the query, but do not return your analysis process to the user—only return the final answer. Make sure your answers are as explanatory as possible. If the answer can be supplemented with additional details, add "더 필요한 정보가 있나요?" at the end of your response. If the answer to the question cannot be determined from the context alone state "그 질문에 대한 답은 드릴 수 없습니다."
At the end of your response, list the relevant page numbers in the format: "관련 페이지: {page_numbers}". But, if you answered "그 질문에 대한 답은 드릴 수 없습니다.", please don't print out the related page!

If the query is a general greeting or a question about your identity, respond appropriately without using the provided context.

The following examples are provided as a reference for the ideal answer style. Do NOT use the content of these examples in your actual answers. They are only meant to show the structure and style of your responses:

Example 1:
Query: 2015학번 이후 ELLT학과 재학생의 졸업 요건을 알려줘.
Answer: 2015학번 이후 ELLT학과에 재학하고 있는 한국외국어대학교 학생의 졸업 요건은 다음과 같습니다:
졸업에 필요한 총 학점 이상 취득.
영역별 (1전공, 이중(부)전공, 교양 등) 최소 이수학점 이상 취득.
전체 평점 평균이 2.00 이상.
필수과목(전공, 교양) 이수 조건을 충족.
1전공, 이중전공의 졸업시험(졸업논문)을 통과하거나 외국어인증제 통과.
ELLT학과 재학생의 전공 필수 과목은 영어학개론(1), 고급영어문법(1),(2), Critical Writing(1),(2)이며, 공인 영어 시험 최소 점수 요건은 FLEX 610점, TOEIC 805점, TOEFL IBT 94점, IELTS 6.5점 이상입니다. 더 필요한 정보는 학과 사이트를 참고하시거나, 추가적인 질문을 해주세요!
관련 페이지: 12, 34

Example 2:
Query: 융합전공에 대해 설명해줘.
Answer: 융합전공이란 2개 이상의 전공을 융복합하여 이수하는 제도입니다. 융합전공의 이수학점은 이중전공 및 부전공 이수학점과 동일하며, 제1전공 및 융합(이중·부)전공의 졸업요건이 모두 충족되었을 경우에 제 1전공·융합(이중·부) 전공이 병행 표기된 학위를 수여합니다. 현재 한국외국어대학교에 개설된 일반융합전공은 다음과 같습니다:

BRICs(브릭스)전공
EU(유럽연합)전공
동북아외교통상전공
문화콘텐츠학전공
국가리더전공
세계문화예술경영전공
디지털인문한국학전공
AI융합전공
데이터사이언스전공
상담·UX심리전공
각 전공에 대한 자세한 정보는 학교 사이트를 참고하시거나, 추가적인 질문을 해주세요!
관련 페이지: 56, 78

Example 3:
Query: 우리 집 전공에 대해 설명해줘.
Answer: 그 질문에 대한 답은 드릴 수 없습니다.

Example 4:
Query: 안녕?
Answer: 안녕하세요!

Remember, these examples are only for reference. Your answers should be based solely on the provided context and query.

Context: {context}

User query: {query}

Your detailed answer:
"""

def generate_prompt(query: str, chunks: List[Dict[str, Any]], k: int = 5) -> str:
    relevant_chunks = hybrid_search(query, chunks, k)

    context = ""
    total_length = 0
    page_numbers = set()

    for chunk in relevant_chunks:
        chunk_text = f"[{chunk['header']}]\n{chunk['chunk']}\n\n"
        chunk_length = len(chunk_text)

        if total_length + chunk_length > MAX_CONTEXT_LENGTH:
            break

        context += chunk_text
        total_length += chunk_length
        page_numbers.add(chunk['page_number'])

    sorted_page_numbers = sorted(list(page_numbers))
    page_numbers_str = ', '.join(map(str, sorted_page_numbers))

    return PROMPT_TEMPLATE.format(context=context.strip(), query=query, page_numbers=page_numbers_str)

def classify_and_contextualize_query(query: str) -> Dict[str, Any]:
    prompt = f"""Given the following query, please provide the following information:
    1. Is this query related to Hankuk University of Foreign Studies' course catalog? (Yes/No)
    2. If yes, which specific aspect of the course catalog does it relate to?
    3. What is the core part of the query?
    4. What is the overall context of the query?

    Query: {query}

    Please format your response as follows:
    Related: [Yes/No]
    Aspect: [Specific aspect if related, or "N/A" if not related]
    Core: [Core part of the query]
    Context: [Overall context of the query]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes queries related to university course information."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.3,
        )
        result = response.choices[0].message.content.strip()
        
        lines = result.split('\n')
        parsed_result = {}
        for line in lines:
            key, value = line.split(': ', 1)
            parsed_result[key.lower()] = value.strip('[]')
        
        return parsed_result
    except Exception as e:
        print(f"Error in classifying and contextualizing query: {e}")
        return {"related": "Yes", "aspect": "N/A", "core": query, "context": "General inquiry"}

def query_rewriting(original_query: str) -> str:
    analysis = classify_and_contextualize_query(original_query)
    
    if analysis['related'].lower() == 'no':
        return f"{original_query} [Context: {analysis['context']}]"

    prompt = f"""Given the following context about Hankuk University of Foreign Studies' course catalog and the analysis of the original query, please rewrite the query to make it more specific and relevant. The rewritten query should be in Korean.

    Context:
    - 수강신청 일정 및 지침
    - 졸업 이수학점 및 졸업요건 안내
    - 교과영역 및 교과목 안내
    - 수업관련 학사제도 안내
    - 교직과정
    - 외국어특기생 이수 면제 교과목 현황
    - 전공필수 교과목 현황
    - 전공 교류(인정) 교과목 현황
    - 학과(전공)별 수강금지 교양 교과목 현황
    - 중복수강 금지 교과목 현황
    - 동일 교과목 현황(교양 및 기타)
    - 수강유의교과목

    Original Query: {original_query}
    Related Aspect: {analysis['aspect']}
    Core Part: {analysis['core']}
    Overall Context: {analysis['context']}

    Rewritten Query:"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that helps rewrite queries to make them more specific and relevant for searching university course information."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            n=1,
            stop=None,
            temperature=0.3,
        )
        rewritten_query = response.choices[0].message.content.strip()
        return f"{rewritten_query} [Context: {analysis['context']}]"
    except Exception as e:
        print(f"Error in rewriting query: {e}")
        return f"{original_query} [Context: {analysis['context']}]"

def generate_answer(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions about university course information."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in generating answer: {e}")
        return "죄송합니다. 답변을 생성하는 중에 오류가 발생했습니다."

def get_gpt_answer(query: str, processed_data: List[Dict[str, Any]]) -> str:
    original_query = query
    rewritten_query = query_rewriting(query)
    
    combined_query = f"Original Query: {original_query}\nRewritten Query: {rewritten_query}"
    
    prompt = generate_prompt(combined_query, processed_data, k=20)
    answer = generate_answer(prompt)

    print("\n생성된 프롬프트:")
    print(prompt)
    
    return answer