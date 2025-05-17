import os
import glob
import json
import traceback
from pathlib import Path

# Use the new OpenAI v1 client
import openai
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = ""

# LangChain imports (if still used for the explanation agent)
from langchain_openai import ChatOpenAI  # requires langchain-openai package
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.chains import RetrievalQA

# Configuration
MODEL = "gpt-4.1-nano"
INPUT_DIR = "datas"  # Directory containing JSON files
OUTPUT_FILE = "results_signle_1-1859.json"

# Initialize OpenAI client (reads OPENAI_API_KEY from env)
client = OpenAI()


def single_agent(task):
    prompt = (
        "provide a corrected version of the function. Respond with valid Python code only.(WITH ```python \{ write code here \} ```)\n\n"
        "and then give a explanation of the mistake, the fix. (with ```explain\{write explaination here\}```)\n"
        f"Code:\n{task['incorrect_code']}\n"
        f"question: {task['prompt']}\n"
        f"Test cases:\n{task['test_list']}\n"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content.strip()
    code_str = content.split("```python")[1].split("```")[0].strip()
    explanation = content.split("```explain")[1].split("```")[0].strip()
    return code_str, explanation

def classify_error(task):
    prompt = (
        f"Identify the type of error in the following Python code. "
        f"Respond with a concise label.\n\n"
        f"Code:\n{task['incorrect_code']}\n"
        f"question: {task['prompt']}\n"
        f"Test cases:\n{task['test_list']}\n"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def correct_code(task, error_type):
    prompt = (
        f"Given the following Python function and its error type '{error_type}', "
        f"provide a corrected version of the function. Respond with valid Python code only.(WITHOUT ```python ```)\n\n"
        f"Original Code:\n{task['incorrect_code']}\n"
        f"Task Description: {task['prompt']}\n"
        f"Test cases:\n{task['test_list']}\n"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def run_tests(code_str, tests):
    namespace = {}
    try:
        exec(code_str, namespace)
        for test in tests:
            exec(test, namespace)
        return True, None
    except AssertionError as ae:
        return False, str(ae)
    except Exception as e:
        return False, traceback.format_exc()


def generate_explanation(task, fixed_code, error_type, rag_query):
    prompt = (
        f"You are an educational AI assistant. "
        f"A student wrote this function:\n{task.get('incorrect_code')}\n"
        f"It was incorrect and classified as '{error_type}'. "
        f"The corrected function is:\n{fixed_code}\n"
        f"Provide a clear explanation of the mistake, the fix, "
        f"and the underlying learning theory in plain English."
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def score_fix(task, explanation, success):
    prompt = (
        f"You are a code review bot. "
        f"Original code:\n{task.get('incorrect_code')}\n"
        f"Fix explanation:\n{explanation}\n"
        f"Was the fix successful? {'Yes' if success else 'No'}. "
        f"Rate the fix quality on a scale from 1 to 100. "
        f"YOU NEED ONLY RETURN AN INT BETWEEN 1 AND 100.\n"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content.strip()
    try:
        return int(content)
    except ValueError:
        print(f"Invalid score response: {content}")
        return None


def process_task(task):
    fixed_code, explanation = single_agent(task)

    # 3. Run tests
    success, _ = run_tests(fixed_code, task.get('test_list', []))
    # 5. Score the fix
    score = score_fix(task, explanation, success)

    # Build result with original prompt, codes, explanation, and existing metrics
    result = {
        "task_id": task.get("task_id"),
        "prompt": task.get("prompt"),
        "incorrect_code": task.get("incorrect_code"),
        "fixed_code": fixed_code,
        "error_type": None,
        "real_error_type": task.get("error_type"),
        "corrected": success,
        "explanation": explanation,
        "score": score
    }
    return result
def format_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02}"



import time
def main():
    begin_time = time.time()
    results = []
    json_files = glob.glob(os.path.join(INPUT_DIR, "*.json"))

    # Count total tasks
    total_tasks = 0
    for jf in json_files:
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
                total_tasks += len(tasks)
        except Exception:
            continue

    print(f"Found {total_tasks} tasks across {len(json_files)} files.")
    processed = 0

    for jf in json_files:
        with open(jf, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        for task in tasks:
            processed += 1
            try:
                res = process_task(task)
                results.append(res)
                # Save after each task
                with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
                    json.dump(results, out, ensure_ascii=False, indent=2)
                now_time = time.time()
                past_time = now_time - begin_time
                avg_time = past_time / (processed)
                guess_time = avg_time * (total_tasks - processed)
                print(f"Processed {processed}/{total_tasks} tasks. Now cost {format_seconds(past_time)}, Estimated time left: {format_seconds(guess_time)}")
            except Exception as e:
                print(f"[{processed}/{total_tasks}] Task processing failed: {e}")

    print("Processing complete.")


if __name__ == "__main__":
    main()
