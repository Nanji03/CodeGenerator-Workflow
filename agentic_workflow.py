# -------------------------
# Dynamic Agentic Coding Workflow (LLM-powered)
# -------------------------

import os
import re
import openai

openai.api_key = ""

# -------------------------
# Utility: Extract Python code from LLM response
# -------------------------
def extract_code(llm_response: str) -> str:
    """Extract the first Python code block from LLM output."""
    code_blocks = re.findall(r"```(?:python)?\n(.*?)```", llm_response, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    else:
        return llm_response.strip()

# -------------------------
# Coder Agent
# -------------------------
class CoderAgent:
    def generate_code(self, spec, feedback=None):
        """Generate or refine code using LLM."""
        prompt = f"Write Python code for the following function specification:\n{spec}\n"
        if feedback:
            prompt += f"\nFix the following issues in your code:\n{feedback}"
        prompt += "\nOnly provide valid Python code, no explanations."

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        raw_code = response.choices[0].message.content
        return extract_code(raw_code)

# -------------------------
# Tester Agent
# -------------------------
class TesterAgent:
    def generate_tests(self, spec):
        """Ask LLM to suggest simple test cases for the function."""
        prompt = f"Provide 2-3 Python assert statements to test the function described as:\n{spec}\n"
        prompt += "Do not include any explanations, only assert statements."
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        raw_tests = response.choices[0].message.content
        return extract_code(raw_tests)

    def test_code(self, code, test_code):
        """Execute the generated function and unit tests."""
        local_env = {}
        try:
            exec(code, {}, local_env)       # function definition
            exec(test_code, {}, local_env)  # unit tests
            return {"success": True, "output": "All tests passed!"}
        except Exception as e:
            return {"success": False, "error": str(e)}

# -------------------------
# Decision Agent
# -------------------------
class DecisionAgent:
    def decide(self, test_results):
        return "accept" if test_results["success"] else "revise"

# -------------------------
# Workflow
# -------------------------
def run_dynamic_workflow():
    print("Enter your function specification (e.g., 'reverse_string(s) returns reversed string'):")
    spec = input(">>> ")

    feedback = None
    max_iterations = 5

    coder = CoderAgent()
    tester = TesterAgent()
    decision = DecisionAgent()

    #print("Using OpenAI API Key:", os.environ.get("OPENAI_API_KEY", "not set"))

    # Generate unit tests first
    test_code = tester.generate_tests(spec)
    print("\nGenerated Test Cases:\n", test_code)

    for i in range(max_iterations):
        print(f"\n--- Iteration {i+1} ---")
        code = coder.generate_code(spec, feedback)
        print("Generated Code:\n", code)

        results = tester.test_code(code, test_code)
        print("Test Results:", results)

        action = decision.decide(results)
        if action == "accept":
            print("\n✅ Final code accepted:\n", code)
            break
        else:
            print("\n⚠️ Code needs revision, sending feedback...")
            feedback = results.get("error", "Code did not pass tests")

if __name__ == "__main__":
    run_dynamic_workflow()
