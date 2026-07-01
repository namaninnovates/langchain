import os
import time
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI

@tool
def attendance_calculator(total_classes: int, attended_classes: int) -> str:
    """Calculate attendance % and determine exam eligibility."""
    if total_classes <= 0:
        return "Total classes must be greater than zero."
    if attended_classes < 0 or attended_classes > total_classes:
        return "Attended classes must be between 0 and total classes."

    percentage = (attended_classes / total_classes) * 100
    eligibility = "Eligible for Exam" if percentage >= 75 else "Not Eligible for Exam"

    return f"Attendance: {percentage:.2f}%. Status: {eligibility}"

@tool
def result_calculator(subject1: float, subject2: float, subject3: float, subject4: float, subject5: float) -> str:
    """Calculate the average marks, grade, and pass/fail status from marks of 5 subjects."""
    marks = [subject1, subject2, subject3, subject4, subject5]
    average = sum(marks) / len(marks)

    if average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    elif average >= 60:
        grade = "C"
    else:
        grade = "D"

    status = "Pass" if average >= 50 else "Fail"

    return f"Average: {average:.2f}, Grade: {grade}, Status: {status}"

@tool
def fee_balance_calculator(total_fee: float, amount_paid: float) -> str:
    """Calculate the pending fee balance."""
    if total_fee < 0 or amount_paid < 0:
        return "Fee amounts cannot be negative."
    if amount_paid > total_fee:
        return f"Overpaid by ₹{amount_paid - total_fee:.2f}."

    pending = total_fee - amount_paid
    return f"Pending Fee: ₹{pending:.2f}"

@tool
def library_fine_calculator(delayed_days: int) -> str:
    """Calculate the library fine for late book returns."""
    if delayed_days < 0:
        return "Delayed days cannot be negative."
    fine = 5 * delayed_days
    return f"Total Fine: ₹{fine}"

@tool
def hostel_fee_calculator(monthly_fee: float, months_stayed: int) -> str:
    """Calculate the total hostel fee."""
    if monthly_fee < 0 or months_stayed < 0:
        return "Values cannot be negative."
    total = monthly_fee * months_stayed
    return f"Total Hostel Fee: ₹{total:.2f}"

STUDENT_DATABASE = {
    "S001": {"name": "Aarav Sharma", "branch": "Computer Science", "semester": 5, "email": "aarav.sharma@college.edu", "phone": "9876543210", "cgpa": 8.7},
    "S002": {"name": "Priya Patel", "branch": "Electronics", "semester": 3, "email": "priya.patel@college.edu", "phone": "9876543211", "cgpa": 9.2},
    "S003": {"name": "Rohan Gupta", "branch": "Mechanical", "semester": 7, "email": "rohan.gupta@college.edu", "phone": "9876543212", "cgpa": 7.5},
    "S004": {"name": "Sneha Reddy", "branch": "Civil Engineering", "semester": 4, "email": "sneha.reddy@college.edu", "phone": "9876543213", "cgpa": 8.1},
    "S005": {"name": "Naman Gupta", "branch": "Information Technology", "semester": 6, "email": "naman.gupta@college.edu", "phone": "9876543214", "cgpa": 9.0},
}

@tool
def student_info(student_id: str) -> str:
    """Retrieve student details using their Student ID."""
    student_id = student_id.upper().strip()
    student = STUDENT_DATABASE.get(student_id)

    if not student:
        return f"Student ID '{student_id}' not found."

    return (
        f"Name: {student['name']}, Branch: {student['branch']}, "
        f"Semester: {student['semester']}, Email: {student['email']}, "
        f"Phone: {student['phone']}, CGPA: {student['cgpa']}"
    )

tools = [
    attendance_calculator,
    result_calculator,
    fee_balance_calculator,
    library_fine_calculator,
    hostel_fee_calculator,
    student_info,
]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a friendly and helpful College Assistant AI. "
            "Help students with their queries using the provided tools. "
            "Give direct, conversational answers without sounding robotic. "
            "If they ask for multiple things, use all the necessary tools and summarize nicely. "
            "Available tools: attendance_calculator, result_calculator, fee_balance_calculator, library_fine_calculator, hostel_fee_calculator, student_info"
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    api_key = input("Please enter your OpenRouter API key: ").strip()

llm = ChatOpenAI(
    model="google/gemini-2.5-flash-lite",
    temperature=0,
    max_tokens=1024,
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
)

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=8,
    handle_tool_error=True,
    handle_parsing_errors=True,
)

def run_query_with_retry(executor, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return executor.invoke({"input": query})
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "rate" in error_msg.lower():
                time.sleep(30 * (attempt + 1))
            else:
                return {"output": f"Oops, something went wrong: {e}"}
    return {"output": "Sorry, I'm getting rate limited right now."}

if __name__ == "__main__":
    test_queries = [
        "I attended 72 classes out of 90. Am I eligible for exams?",
        "My marks are 95, 90, 88, 91 and 87. What is my grade?",
        "My course fee is 50000 and I have paid 35000. How much fee is pending?",
        "I returned a library book 8 days late. What is the fine amount?",
        "Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.",
        "I attended 80 classes out of 100. My marks are 90, 85, 88, 92 and 95. My course fee is 60000 and I paid 45000. Provide: 1. Attendance Status 2. Grade 3. Pending Fee",
        "Get me the details of student S002.",
    ]

    for query in test_queries:
        print(f"\nUser: {query}")
        result = run_query_with_retry(agent_executor, query)
        print(f"Assistant: {result['output']}\n")
        time.sleep(5)
