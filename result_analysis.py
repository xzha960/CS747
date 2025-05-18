import json
from collections import defaultdict

def find_error_type(sample_id):
    error_types = [
        "grammarly-errors",
        "logic-errors",
        "function-design-errors",
        "conditional-judgment-errors",
        "loop-termination-condition-errors",
        "uninitialized-variable-errors",
        "type-errors",
        "calculation-errors",
        "list-indexing-errors",
        "input-output-format-errors"
    ]
    return error_types[sample_id // 427]



def analyze_results(file_path="results_test.json"):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    error_summary = defaultdict(lambda: {"total": 0, "corrected": 0, "score_sum": 0})
    sample_processed = 0
    for item in data:
        error_type = find_error_type(sample_processed)
        sample_processed += 1
        corrected = item.get("corrected", False)
        score = item.get("score", 0)
        if score is None or score == 0:# None or 0 means score failed
            score = 100
        error_summary[error_type]["total"] += 1
        error_summary[error_type]["score_sum"] += score
        if corrected:
            error_summary[error_type]["corrected"] += 1

    # 输出每个错误类型的统计信息
    print("Per Error Type Statistics:")
    for error_type, stats in error_summary.items():
        total = stats["total"]
        corrected = stats["corrected"]
        score_sum = stats["score_sum"]
        accuracy = corrected / total * 100
        avg_score = score_sum / total
        print(f"- {error_type}:")
        print(f"  Total: {total}")
        print(f"  Corrected: {corrected}")
        print(f"  Accuracy: {accuracy:.2f}%")
        print(f"  Average Score: {avg_score:.2f}")

    # 计算总体改错成功率和平均分
    total_tasks = sum(stats["total"] for stats in error_summary.values())
    total_corrected = sum(stats["corrected"] for stats in error_summary.values())
    total_score = sum(stats["score_sum"] for stats in error_summary.values())

    overall_accuracy = total_corrected / total_tasks * 100
    overall_avg_score = total_score / total_tasks

    print("\nOverall Statistics:")
    print(f"Total Tasks: {total_tasks}")
    print(f"Overall Accuracy: {overall_accuracy:.2f}%")
    print(f"Overall Average Score: {overall_avg_score:.2f}")

analyze_results("ALL.json")
analyze_results("merged_signle_results.json")
