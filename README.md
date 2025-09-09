# CodeGenerator Workflow

## Overview

This project demonstrates an **agentic coding workflow** powered by an LLM (OpenAI GPT-4o-mini). The workflow is designed to automatically generate, test, and refine Python code from **any function specification** provided by the user.

It consists of three agents working together:

1. **CoderAgent**: Generates or refines Python code based on the function specification and feedback.
2. **TesterAgent**: Automatically generates unit tests and validates the generated code.
3. **DecisionAgent**: Determines if the generated code passes all tests and whether it should be accepted or revised.

The workflow iteratively refines the code until it passes all tests or reaches the maximum iteration limit.

---

## Features

* **Dynamic function specifications**: Users can input any Python function description.
* **Automatic test generation**: The workflow prompts the LLM to create simple unit tests based on the spec.
* **Iterative refinement**: If tests fail, the LLM refines the code using feedback.
* **Clean execution**: Only valid Python code is executed, avoiding syntax errors from explanations or markdown.
* **Minimal setup**: Runs locally with Python 3.13+ and OpenAI API access.

---

## Installation

1. Clone or download this repository.
2. Install dependencies:

```bash
pip install openai
```

3. Set your OpenAI API key:

## Usage

Run the workflow script:

```bash
python dynamic_agentic_workflow.py
```

1. Enter your function specification when prompted, for example:

```
reverse_string(s) that returns the reversed string
```

2. The workflow will:

   * Generate unit tests.
   * Generate the function code using the LLM.
   * Run tests and provide feedback.
   * Refine the code iteratively until all tests pass.

3. Upon success, the workflow prints the **final accepted code**.

---

## File Structure

```
agentic_workflow.py   # Main script with the workflow and agents
README.md                    
```

---

## Dependencies

* Python 3.13+
* OpenAI Python SDK (`pip install openai`)
* Internet connection for LLM API calls

---

## Notes

* Ensure your OpenAI API key is valid and set correctly.
* The workflow currently supports functions that can be validated with simple Python `assert` statements.
* For more complex functions, you may need to modify the `TesterAgent` to handle advanced test cases.

---

## License

This project is for educational purposes and personal use.

