import google.generativeai as genai
import os


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI API Key. Set it in your environment variables.")

genai.configure(api_key=GEMINI_API_KEY)


def analyze_code_with_gemini(code: str, language: str):
    """
    Sends the given code snippet to Google Gemini AI for analysis.
    """
    prompt = f"""
    You are an AI code reviewer. Analyze the following {language} code snippet:

    ```{language}
    {code}
    ```

    Provide a structured report including:
    1️⃣ **Time Complexity Analysis**
    2️⃣ **Quality Score (0-100%)**
    3️⃣ **Performance & Optimization Tips**
    4️⃣ **Security & Best Practices**
    5️⃣ **Issues & Warnings (if any)**
    6️⃣ **Suggestions for Improvement**

    Return a detailed but concise report.
    """

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing code: {str(e)}"


# Example: Multiple code snippets in different languages
code_samples = {
    "Palindrome Check (Python)": """
def is_palindrome(s):
    s = s.lower()
    reversed_s = ""
    for char in reversed(s):
        reversed_s += char
    return s == reversed_s
""",
    "Factorial Calculation (Java)": """
public class Factorial {
    public static int factorial(int n) {
        if (n == 0) return 1;
        return n * factorial(n - 1);
    }
}
""",
    "Sum of Array (C++)": """
#include <iostream>
using namespace std;

int sumArray(int arr[], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum;
}
"""
}

# Analyze each code snippet using Gemini AI
for title, code in code_samples.items():
    language = title.split("(")[-1].strip(")") if "(" in title else "Unknown"
    print(f"\n📊 Analyzing {title} ({language})...\n")
    analysis = analyze_code_with_gemini(code, language)
    print(analysis)
    print("=" * 50)
