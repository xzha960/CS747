# Eudfix: Automated Code Repair and Pedagogical Feedback System

**Eudfix** is an intelligent repair and feedback system designed for novice Python programming education. It supports automatic error detection, correction, and explanation generation. The system uses a multi-agent architecture and retrieval-augmented generation (RAG) to simulate real instructional feedback and enhance learners’ conceptual understanding of programming errors.

---

## 1. Project Structure

```
.
├── datas/                               # Input data directory (error-annotated tasks)
├── sanitized-mbpp-with-*.json           # Ten input files with different error types
├── ALL.json                             # Merged multi-agent result output
├── merged_signle_results.json           # Single-agent output
├── muti-agent.py                        # Multi-agent pipeline (detection, correction, explanation)
├── single-agent.py                      # Unified prompt baseline pipeline
├── rag.py                               # Educational knowledge retrieval module (based on *How People Learn*)
├── merge.py                             # Utility for merging JSON result files
├── result_analysis.py                   # Script for analyzing repair outcomes
├── data_calculate.py                    # Accuracy and score computation
├── draw.py                              # Plotting script for visual comparison
├── README.md                            # This documentation file
```

---

## 2. System Architecture and Workflow

Eudfix consists of three primary agents:

- **Error Detection Agent**: Identifies the type of bug (e.g., conditional errors, type mismatches).
- **Repair Agent**: Applies minimal edits using an LLM and verifies correctness using test cases.
- **Explanation Agent**: Retrieves teaching concepts via RAG and generates clear, educational feedback.

The system also includes a single-agent baseline pipeline that directly produces repaired code and explanation from a unified prompt, enabling comparison between both designs across various error types.

---

## 3. Error Type Definition

The system supports ten common error types frequently made by novice programmers, based on prior educational research and simulated via large language models:

1. Grammarly errors  
2. Logic errors  
3. Function design errors  
4. Conditional judgment errors  
5. Loop termination errors  
6. Uninitialized variable errors  
7. Type mismatch errors  
8. Computation errors  
9. Array access errors  
10. Input/output formatting errors  

Each category includes prompts, correct code, test cases, and corresponding buggy versions.

---

## 4. Dataset Construction and Quality Control

The dataset contains over 11,000 annotated erroneous code instances, covering errors from the syntax level to the design level. We ensured:

- Each buggy version fails at least one test case;
- Each task includes multiple representative erroneous variants;
- All samples are structured in JSON format for ease of access and evaluation.

---

## 5. Evaluation Metrics and Usage

Eudfix adopts the following evaluation metrics:

- **Corrected**: Whether the repaired code passes all test cases.
- **Accuracy**: Proportion of successfully repaired tasks.
- **Average Score**: AI-generated score (0–100) evaluating the clarity and pedagogical value of the explanation.

To evaluate, run:

```bash
python result_analysis.py
```

Use `draw.py` to generate accuracy and score comparison plots across error types.

---

## 6. RAG-Based Explanation Retrieval

The Explanation Agent retrieves educational content from a vector index built on *How People Learn*, generating explanations aligned with learning science. For example:

> “Using `=` instead of `==` is a typical beginner mistake reflecting confusion between assignment and logical comparison.”

This improves explanation relevance, clarity, and consistency.

---

## 7. Environment Setup

Recommended: Python ≥ 3.8. Required dependencies:

```bash
pip install openai langchain faiss-cpu pymupdf
```