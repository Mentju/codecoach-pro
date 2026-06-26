from flask import Flask, jsonify, request, render_template, send_from_directory
import sqlite3
import os
from pathlib import Path
from datetime import datetime
import io
import contextlib

app = Flask(__name__)
DB_PATH = Path("codecoach_pro.db")

GUIDED_LESSONS = [
  {
    "id": "python_expense_tracker",
    "language": "Python",
    "title": "Build a Python Expense Tracker",
    "description": "Walk through a complete Python script that stores expenses, calculates totals, and prints a small report.",
    "final_goal": "Create a full expense tracker script without help.",
    "steps": [
      {
        "title": "Step 1: Create expense data",
        "explanation": "Every useful program starts with data. Here, we store expenses in a list of dictionaries. Each dictionary represents one expense with a category and amount.",
        "mode": "learn",
        "code": "expenses = [\n    {'category': 'Food', 'amount': 25.50},\n    {'category': 'Gas', 'amount': 40.00},\n    {'category': 'School', 'amount': 75.25}\n]\n\nprint(expenses)",
        "check": "expenses"
      },
      {
        "title": "Step 2: Loop through the expenses",
        "explanation": "A loop lets us work with each expense one at a time. This is how programs process lists of data.",
        "mode": "learn",
        "code": "for expense in expenses:\n    print(expense['category'], expense['amount'])",
        "check": "for"
      },
      {
        "title": "Step 3: Add the total",
        "explanation": "Now we create a total variable and add each amount to it. This is a common pattern in business, finance, and data analysis scripts.",
        "mode": "guided",
        "prompt": "Fill in the missing line so each expense amount is added to total.",
        "code": "total = 0\n\nfor expense in expenses:\n    # add amount to total below\n    \n\nprint('Total spending:', total)",
        "answer_key": "total += expense['amount']",
        "hint": "Use total += expense['amount']"
      },
      {
        "title": "Step 4: Group spending by category",
        "explanation": "Real reports usually group data. A dictionary is a good way to store totals by category.",
        "mode": "guided",
        "prompt": "Complete the dictionary update so each category gets its own spending total.",
        "code": "category_totals = {}\n\nfor expense in expenses:\n    category = expense['category']\n    amount = expense['amount']\n\n    if category not in category_totals:\n        category_totals[category] = 0\n\n    # add amount to the correct category below\n    \n\nprint(category_totals)",
        "answer_key": "category_totals[category] += amount",
        "hint": "Use category_totals[category] += amount"
      },
      {
        "title": "Final Challenge: Build the complete script",
        "explanation": "Now put everything together. Create the expenses list, calculate the total, group spending by category, and print a report.",
        "mode": "final",
        "prompt": "Complete the full Python expense tracker script from scratch.",
        "code": "# Final challenge: build the full expense tracker\n# Requirements:\n# 1. Create a list named expenses\n# 2. Each expense should have category and amount\n# 3. Calculate total spending\n# 4. Calculate category totals\n# 5. Print total and category totals\n\n",
        "answer_key": "category_totals",
        "hint": "Your final script should include expenses, a for loop, total, and category_totals."
      }
    ]
  },
  {
    "id": "javascript_todo_app",
    "language": "JavaScript",
    "title": "Build a JavaScript To-Do List",
    "description": "Walk through a browser-based JavaScript script that stores tasks, adds tasks, and renders them to the page.",
    "final_goal": "Create a working mini to-do script without help.",
    "steps": [
      {
        "title": "Step 1: Create task data",
        "explanation": "A to-do app needs a place to store tasks. We use an array of objects because each task can have a title and completion status.",
        "mode": "learn",
        "code": "let tasks = [\n  { title: 'Study Python', done: false },\n  { title: 'Practice SQL', done: true }\n];\n\nconsole.log(tasks);",
        "check": "tasks"
      },
      {
        "title": "Step 2: Add a new task",
        "explanation": "The push method adds a new item to an array. This is one of the most common JavaScript patterns.",
        "mode": "guided",
        "prompt": "Add a new task object to the tasks array.",
        "code": "let tasks = [];\n\n// Add a task below\n\n\nconsole.log(tasks);",
        "answer_key": "tasks.push",
        "hint": "Use tasks.push({ title: 'Learn JavaScript', done: false });"
      },
      {
        "title": "Step 3: Render tasks as HTML",
        "explanation": "Rendering means turning data into something the user can see. map() transforms each task into an HTML string.",
        "mode": "guided",
        "prompt": "Complete the map function so each task becomes a list item.",
        "code": "let tasks = [\n  { title: 'Study Python', done: false },\n  { title: 'Practice SQL', done: true }\n];\n\nlet html = tasks.map(task => {\n  // return a list item below\n  \n}).join('');\n\nconsole.log(html);",
        "answer_key": "return",
        "hint": "Return `<li>${task.title}</li>`"
      },
      {
        "title": "Step 4: Connect JavaScript to the page",
        "explanation": "The DOM lets JavaScript change the web page. getElementById selects an element, and innerHTML places content inside it.",
        "mode": "guided",
        "prompt": "Set the innerHTML of the output element equal to the html variable.",
        "code": "let html = '<li>Study JavaScript</li>';\n\n// Put html inside the page element with id output\n\n",
        "answer_key": "innerHTML",
        "hint": "Use document.getElementById('output').innerHTML = html;"
      },
      {
        "title": "Final Challenge: Build the full to-do script",
        "explanation": "Now build the full script. Create tasks, add a new task, turn tasks into HTML, and render them to the page.",
        "mode": "final",
        "prompt": "Complete a full JavaScript to-do script from scratch.",
        "code": "// Final challenge: build the full to-do script\n// Requirements:\n// 1. Create a tasks array\n// 2. Add at least one task with push()\n// 3. Use map() to create list items\n// 4. Use innerHTML to render the list\n\n",
        "answer_key": "innerHTML",
        "hint": "Your final script should include tasks, push, map, and innerHTML."
      }
    ]
  },
  {
    "id": "sql_sales_report",
    "language": "SQL",
    "title": "Build a SQL Sales/Expense Report",
    "description": "Walk through SQL queries that select, filter, group, and summarize business data.",
    "final_goal": "Write a full business-report SQL query without help.",
    "steps": [
      {
        "title": "Step 1: Select all records",
        "explanation": "Most SQL work starts by viewing the table. SELECT * shows all columns and rows from a table.",
        "mode": "learn",
        "code": "SELECT * FROM expenses;",
        "check": "SELECT"
      },
      {
        "title": "Step 2: Select specific columns",
        "explanation": "In real work, you usually select only the columns you need. This keeps reports cleaner.",
        "mode": "guided",
        "prompt": "Select only category and amount from the expenses table.",
        "code": "-- Select category and amount below\n\n",
        "answer_key": "SELECT category, amount FROM expenses",
        "hint": "Use SELECT category, amount FROM expenses;"
      },
      {
        "title": "Step 3: Filter rows with WHERE",
        "explanation": "WHERE filters rows before grouping or sorting. It helps answer specific questions.",
        "mode": "guided",
        "prompt": "Write a query to select only Food expenses.",
        "code": "-- Select Food expenses below\n\n",
        "answer_key": "WHERE category",
        "hint": "Use WHERE category = 'Food'"
      },
      {
        "title": "Step 4: Group and summarize",
        "explanation": "GROUP BY is how SQL creates summaries. SUM(amount) totals spending for each category.",
        "mode": "guided",
        "prompt": "Complete a query that totals amount by category.",
        "code": "SELECT category, SUM(amount) AS total_spent\nFROM expenses\n-- group by category below\n\n",
        "answer_key": "GROUP BY category",
        "hint": "Add GROUP BY category;"
      },
      {
        "title": "Final Challenge: Build the full SQL report",
        "explanation": "Now write a business report query that shows total spending by category and sorts highest to lowest.",
        "mode": "final",
        "prompt": "Write a complete SQL report query from scratch.",
        "code": "-- Final challenge\n-- Requirements:\n-- 1. Select category\n-- 2. Calculate SUM(amount) as total_spent\n-- 3. Group by category\n-- 4. Order highest total first\n\n",
        "answer_key": "ORDER BY",
        "hint": "Use SELECT category, SUM(amount) AS total_spent FROM expenses GROUP BY category ORDER BY total_spent DESC;"
      }
    ]
  }
]

PRACTICE_PROBLEMS = [
  {
    "id": 1,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Print Output",
    "prompt": "Print your name and today's learning goal.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "print(",
    "hint": "Use print()."
  },
  {
    "id": 2,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Variables",
    "prompt": "Create variables for name, age, and language, then print them.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "=",
    "hint": "Assign values with =."
  },
  {
    "id": 3,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Math Operators",
    "prompt": "Calculate total cost using price and quantity.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "*",
    "hint": "Use multiplication."
  },
  {
    "id": 4,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Comparison Operators",
    "prompt": "Check whether score is greater than or equal to 70.",
    "starter": "# Write your Python answer here\n",
    "solution_key": ">=",
    "hint": "Use >=."
  },
  {
    "id": 5,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Type Conversion",
    "prompt": "Convert a string number to an integer and add 10.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "int(",
    "hint": "Use int(value)."
  },
  {
    "id": 6,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Input Simulation",
    "prompt": "Create a variable named user_input and use it in a sentence.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "user_input",
    "hint": "Use a variable."
  },
  {
    "id": 7,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "String Formatting",
    "prompt": "Use an f-string to print a name and score.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "f\"",
    "hint": "Use f\"...{variable}...\"."
  },
  {
    "id": 8,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Boolean Logic",
    "prompt": "Use and/or to test if a user can access a system.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "and",
    "hint": "Combine conditions."
  },
  {
    "id": 9,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Modulo",
    "prompt": "Use modulo to determine if a number is even.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "%",
    "hint": "Use n % 2."
  },
  {
    "id": 10,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Comments",
    "prompt": "Write code with at least one useful comment.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "#",
    "hint": "Python comments start with #."
  },
  {
    "id": 11,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "If Else",
    "prompt": "Use if/else to print pass or fail based on a grade.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "else",
    "hint": "Use if grade >= 70."
  },
  {
    "id": 12,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Elif Ladder",
    "prompt": "Convert numeric score to letter grade.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "elif",
    "hint": "Use if, elif, else."
  },
  {
    "id": 13,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "For Loop Range",
    "prompt": "Print numbers 1 through 10.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "range",
    "hint": "Use range(1, 11)."
  },
  {
    "id": 14,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "While Loop",
    "prompt": "Use while to count down from 5.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "while",
    "hint": "Decrease counter each time."
  },
  {
    "id": 15,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Break",
    "prompt": "Loop through numbers and stop when number equals 5.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "break",
    "hint": "Use break inside if."
  },
  {
    "id": 16,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Continue",
    "prompt": "Print only odd numbers from 1 to 10.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "continue",
    "hint": "Skip even numbers."
  },
  {
    "id": 17,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Nested If",
    "prompt": "Check login only if username exists.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "if",
    "hint": "Use one if inside another."
  },
  {
    "id": 18,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Loop Sum",
    "prompt": "Sum numbers from 1 to 100.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "for",
    "hint": "Use a loop and total variable."
  },
  {
    "id": 19,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Loop Over String",
    "prompt": "Count the letter a in a word.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "for",
    "hint": "Loop through characters."
  },
  {
    "id": 20,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Menu Logic",
    "prompt": "Create a simple menu selection using if/elif.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "elif",
    "hint": "Check option values."
  },
  {
    "id": 21,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Intermediate",
    "title": "Create List",
    "prompt": "Create a list of five programming topics.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "[",
    "hint": "Use square brackets."
  },
  {
    "id": 22,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Intermediate",
    "title": "Append List",
    "prompt": "Append SQL to a skills list.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "append",
    "hint": "Use list.append()."
  },
  {
    "id": 23,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Intermediate",
    "title": "List Index",
    "prompt": "Print the first item in a list.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "[0]",
    "hint": "Indexes start at 0."
  },
  {
    "id": 24,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Intermediate",
    "title": "List Slice",
    "prompt": "Print the first three items from a list.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "[:3]",
    "hint": "Use slicing."
  },
  {
    "id": 25,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Intermediate",
    "title": "Dictionary Create",
    "prompt": "Create a student dictionary with name and grade.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "{",
    "hint": "Use key-value pairs."
  },
  {
    "id": 26,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Intermediate",
    "title": "Dictionary Access",
    "prompt": "Print the grade from a student dictionary.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "['grade']",
    "hint": "Access by key."
  },
  {
    "id": 27,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Intermediate",
    "title": "Set Unique",
    "prompt": "Remove duplicates from a list using set.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "set(",
    "hint": "Convert to set."
  },
  {
    "id": 28,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Intermediate",
    "title": "Tuple Basics",
    "prompt": "Create a tuple for coordinates.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "(",
    "hint": "Tuples use parentheses."
  },
  {
    "id": 29,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Intermediate",
    "title": "Nested List",
    "prompt": "Create a list of lists and print one nested value.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "[",
    "hint": "Use two indexes."
  },
  {
    "id": 30,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Intermediate",
    "title": "List Comprehension",
    "prompt": "Create a list of squares from 1 to 5.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "for",
    "hint": "Use [x*x for x in ...]."
  },
  {
    "id": 31,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Intermediate",
    "title": "Define Function",
    "prompt": "Define a function named greet that prints Hello.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "def greet",
    "hint": "Use def greet():."
  },
  {
    "id": 32,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Intermediate",
    "title": "Return Value",
    "prompt": "Create add(a,b) that returns the sum.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "return",
    "hint": "Use return a + b."
  },
  {
    "id": 33,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Intermediate",
    "title": "Default Argument",
    "prompt": "Create greet(name='Student').",
    "starter": "# Write your Python answer here\n",
    "solution_key": "=",
    "hint": "Default values go in parameters."
  },
  {
    "id": 34,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Intermediate",
    "title": "Keyword Arguments",
    "prompt": "Call a function using keyword arguments.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "=",
    "hint": "Use name='Brandon'."
  },
  {
    "id": 35,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Intermediate",
    "title": "Scope",
    "prompt": "Create a local variable inside a function.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "def",
    "hint": "Variables inside functions are local."
  },
  {
    "id": 36,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Intermediate",
    "title": "Multiple Returns",
    "prompt": "Return min and max from a list.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "return",
    "hint": "Return two values."
  },
  {
    "id": 37,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Intermediate",
    "title": "Lambda",
    "prompt": "Create a lambda that doubles a number.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "lambda",
    "hint": "Use lambda x: x*2."
  },
  {
    "id": 38,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Intermediate",
    "title": "Map Concept",
    "prompt": "Use map to convert strings to integers.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "map",
    "hint": "Use map(int, list)."
  },
  {
    "id": 39,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Intermediate",
    "title": "Import Math",
    "prompt": "Write code that imports math and uses sqrt.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "import math",
    "hint": "Use import math."
  },
  {
    "id": 40,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Intermediate",
    "title": "Docstring",
    "prompt": "Add a docstring to a function.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "\"\"\"",
    "hint": "Triple quotes document functions."
  },
  {
    "id": 41,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Advanced",
    "title": "Try Except",
    "prompt": "Handle ValueError when converting text to int.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "except",
    "hint": "Use try/except."
  },
  {
    "id": 42,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Advanced",
    "title": "Raise Error",
    "prompt": "Raise ValueError if age is negative.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "raise",
    "hint": "Use raise ValueError."
  },
  {
    "id": 43,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Advanced",
    "title": "Class Definition",
    "prompt": "Create a class named Student.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "class Student",
    "hint": "Use class Student:."
  },
  {
    "id": 44,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Advanced",
    "title": "Constructor",
    "prompt": "Create __init__ with name and grade.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "__init__",
    "hint": "Use def __init__(self,...)."
  },
  {
    "id": 45,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Advanced",
    "title": "Instance Method",
    "prompt": "Create method is_passing inside Student.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "self",
    "hint": "Methods use self."
  },
  {
    "id": 46,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Advanced",
    "title": "Inheritance",
    "prompt": "Create Manager class that inherits Employee.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "(",
    "hint": "class Manager(Employee)."
  },
  {
    "id": 47,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Advanced",
    "title": "Read File Pattern",
    "prompt": "Write a safe pattern for reading a file.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "with open",
    "hint": "Use with open(...) as f."
  },
  {
    "id": 48,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Advanced",
    "title": "Write File Pattern",
    "prompt": "Write a safe pattern for writing to a file.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "with open",
    "hint": "Use mode 'w'."
  },
  {
    "id": 49,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Advanced",
    "title": "JSON Concept",
    "prompt": "Convert dictionary to JSON string.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "json",
    "hint": "Use json.dumps()."
  },
  {
    "id": 50,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Advanced",
    "title": "CSV Concept",
    "prompt": "Split CSV-style text into rows and columns.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "split",
    "hint": "Use split('\\n') and split(',')."
  },
  {
    "id": 51,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Debug Syntax",
    "prompt": "Fix a missing colon in an if statement.",
    "starter": "# Write your Python answer here\n",
    "solution_key": ":",
    "hint": "If statements need colons."
  },
  {
    "id": 52,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Predict Output",
    "prompt": "Write code that shows what 3 * 'Hi' outputs.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "*",
    "hint": "Strings can repeat."
  },
  {
    "id": 53,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Truthiness",
    "prompt": "Check whether an empty list is false.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "if",
    "hint": "Empty containers are false."
  },
  {
    "id": 54,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Mutable List",
    "prompt": "Show how appending changes a list.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "append",
    "hint": "Lists are mutable."
  },
  {
    "id": 55,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Immutable String",
    "prompt": "Create a new string from an old one.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "+",
    "hint": "Strings do not change in place."
  },
  {
    "id": 56,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Nested Loop",
    "prompt": "Print a 3x3 grid of stars.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "for",
    "hint": "Use nested loops."
  },
  {
    "id": 57,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Sort Key",
    "prompt": "Sort list of dictionaries by grade.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "key",
    "hint": "Use key=lambda x."
  },
  {
    "id": 58,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Enumerate",
    "prompt": "Loop with index and value.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "enumerate",
    "hint": "Use enumerate(list)."
  },
  {
    "id": 59,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Zip",
    "prompt": "Combine names and scores using zip.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "zip",
    "hint": "Use zip(names, scores)."
  },
  {
    "id": 60,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Comprehensive Review",
    "prompt": "Build a small grade report using list, dict, loop, and function.",
    "starter": "# Write your Python answer here\n",
    "solution_key": "def",
    "hint": "Combine several concepts."
  },
  {
    "id": 61,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Console Output",
    "prompt": "Print your name using console.log.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log()."
  },
  {
    "id": 62,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Let and Const",
    "prompt": "Create const name and let score.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "const",
    "hint": "Use const for values that do not change."
  },
  {
    "id": 63,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Math Operators",
    "prompt": "Calculate subtotal from price and quantity.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "*",
    "hint": "Use multiplication."
  },
  {
    "id": 64,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Comparison",
    "prompt": "Check if score is at least 70.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": ">=",
    "hint": "Use >=."
  },
  {
    "id": 65,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Template Literals",
    "prompt": "Print a sentence with a variable using backticks.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "`${",
    "hint": "Use template literals."
  },
  {
    "id": 66,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Boolean Logic",
    "prompt": "Check if user is active and verified.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "&&",
    "hint": "Use &&."
  },
  {
    "id": 67,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Modulo",
    "prompt": "Check if number is even.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "%",
    "hint": "Use n % 2."
  },
  {
    "id": 68,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "String Length",
    "prompt": "Print length of a string.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "length",
    "hint": "Use text.length."
  },
  {
    "id": 69,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Parse Number",
    "prompt": "Convert string to number.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "Number(",
    "hint": "Use Number(value)."
  },
  {
    "id": 70,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Comments",
    "prompt": "Write a useful JavaScript comment.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "//",
    "hint": "Comments start with //."
  },
  {
    "id": 71,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "If Else",
    "prompt": "Print pass/fail based on grade.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "else",
    "hint": "Use if/else."
  },
  {
    "id": 72,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Else If",
    "prompt": "Convert score to letter grade.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "else if",
    "hint": "Use else if."
  },
  {
    "id": 73,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "For Loop",
    "prompt": "Print numbers 1 through 10.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "for",
    "hint": "Use for loop."
  },
  {
    "id": 74,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "While Loop",
    "prompt": "Count down from 5.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "while",
    "hint": "Use while."
  },
  {
    "id": 75,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Break",
    "prompt": "Stop loop when value is 5.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "break",
    "hint": "Use break."
  },
  {
    "id": 76,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Continue",
    "prompt": "Skip even numbers.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "continue",
    "hint": "Use continue."
  },
  {
    "id": 77,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Switch",
    "prompt": "Use switch for menu option.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "switch",
    "hint": "Use switch(option)."
  },
  {
    "id": 78,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Ternary",
    "prompt": "Use ternary to assign pass/fail.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "?",
    "hint": "condition ? a : b."
  },
  {
    "id": 79,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Nested If",
    "prompt": "Check login conditions.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "if",
    "hint": "Use nested if or &&."
  },
  {
    "id": 80,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Beginner",
    "title": "Loop Sum",
    "prompt": "Sum numbers from 1 to 100.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "for",
    "hint": "Use total variable."
  },
  {
    "id": 81,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Intermediate",
    "title": "Create Array",
    "prompt": "Create an array of skills.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "[",
    "hint": "Use square brackets."
  },
  {
    "id": 82,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Intermediate",
    "title": "Push",
    "prompt": "Add SQL to an array.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "push",
    "hint": "Use push()."
  },
  {
    "id": 83,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Intermediate",
    "title": "Index",
    "prompt": "Print first array item.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "[0]",
    "hint": "Indexes start at 0."
  },
  {
    "id": 84,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Intermediate",
    "title": "Object Create",
    "prompt": "Create object with name and grade.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "{",
    "hint": "Objects use key-value pairs."
  },
  {
    "id": 85,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Intermediate",
    "title": "Object Access",
    "prompt": "Print the grade from an object.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": ".grade",
    "hint": "Use dot notation."
  },
  {
    "id": 86,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Intermediate",
    "title": "Array Map",
    "prompt": "Square numbers using map.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "map",
    "hint": "Use array.map()."
  },
  {
    "id": 87,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Intermediate",
    "title": "Array Filter",
    "prompt": "Filter scores >= 80.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "filter",
    "hint": "Use array.filter()."
  },
  {
    "id": 88,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Intermediate",
    "title": "Array Reduce",
    "prompt": "Sum prices with reduce.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "reduce",
    "hint": "Use reduce()."
  },
  {
    "id": 89,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Intermediate",
    "title": "Find",
    "prompt": "Find user with id 2.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "find",
    "hint": "Use find()."
  },
  {
    "id": 90,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Intermediate",
    "title": "Destructure",
    "prompt": "Destructure name from object.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "{ name }",
    "hint": "Use const { name } = obj."
  },
  {
    "id": 91,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Intermediate",
    "title": "Get Element",
    "prompt": "Select element by id.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "getElementById",
    "hint": "Use document.getElementById."
  },
  {
    "id": 92,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Intermediate",
    "title": "Text Content",
    "prompt": "Change element text.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "textContent",
    "hint": "Assign textContent."
  },
  {
    "id": 93,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Intermediate",
    "title": "Event Listener",
    "prompt": "Add click event listener.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "addEventListener",
    "hint": "Use addEventListener."
  },
  {
    "id": 94,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Intermediate",
    "title": "Create Element",
    "prompt": "Create a paragraph element.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "createElement",
    "hint": "Use document.createElement."
  },
  {
    "id": 95,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Intermediate",
    "title": "Append Child",
    "prompt": "Append element to container.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "appendChild",
    "hint": "Use appendChild."
  },
  {
    "id": 96,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Intermediate",
    "title": "Input Value",
    "prompt": "Read value from input.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "value",
    "hint": "Use input.value."
  },
  {
    "id": 97,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Intermediate",
    "title": "Class Toggle",
    "prompt": "Toggle a CSS class.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "classList",
    "hint": "Use classList.toggle."
  },
  {
    "id": 98,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Intermediate",
    "title": "Local Storage Save",
    "prompt": "Save value to localStorage.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "localStorage.setItem",
    "hint": "Use setItem."
  },
  {
    "id": 99,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Intermediate",
    "title": "Local Storage Read",
    "prompt": "Read value from localStorage.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "localStorage.getItem",
    "hint": "Use getItem."
  },
  {
    "id": 100,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Intermediate",
    "title": "Render List",
    "prompt": "Render array as HTML list.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "innerHTML",
    "hint": "Use map and join."
  },
  {
    "id": 101,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Advanced",
    "title": "Fetch",
    "prompt": "Fetch data from /api/stats.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "fetch",
    "hint": "Use fetch()."
  },
  {
    "id": 102,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Advanced",
    "title": "Async Await",
    "prompt": "Create async function loadData.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "async",
    "hint": "Use async function."
  },
  {
    "id": 103,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Advanced",
    "title": "Try Catch",
    "prompt": "Handle fetch error.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "catch",
    "hint": "Use try/catch."
  },
  {
    "id": 104,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Advanced",
    "title": "JSON Parse",
    "prompt": "Parse JSON string.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "JSON.parse",
    "hint": "Use JSON.parse."
  },
  {
    "id": 105,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Advanced",
    "title": "JSON Stringify",
    "prompt": "Convert object to JSON.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "JSON.stringify",
    "hint": "Use JSON.stringify."
  },
  {
    "id": 106,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Advanced",
    "title": "Spread Array",
    "prompt": "Copy array using spread.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "...",
    "hint": "Use [...arr]."
  },
  {
    "id": 107,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Advanced",
    "title": "Spread Object",
    "prompt": "Copy object using spread.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "...",
    "hint": "Use {...obj}."
  },
  {
    "id": 108,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Advanced",
    "title": "Arrow Function",
    "prompt": "Create arrow function double.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "=>",
    "hint": "Use const f = x =>."
  },
  {
    "id": 109,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Advanced",
    "title": "Class",
    "prompt": "Create class Student.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "class Student",
    "hint": "Use class."
  },
  {
    "id": 110,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Advanced",
    "title": "Promise Concept",
    "prompt": "Create a simple Promise.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "Promise",
    "hint": "Use new Promise."
  },
  {
    "id": 111,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Hoisting Concept",
    "prompt": "Show let variable declared before use.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "let",
    "hint": "Avoid var confusion."
  },
  {
    "id": 112,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Strict Equality",
    "prompt": "Use strict equality comparison.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "===",
    "hint": "Use ===."
  },
  {
    "id": 113,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Falsy Values",
    "prompt": "Check if empty string is falsy.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "if",
    "hint": "Use if (!value)."
  },
  {
    "id": 114,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Array Includes",
    "prompt": "Check if array includes Python.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "includes",
    "hint": "Use includes()."
  },
  {
    "id": 115,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Object Keys",
    "prompt": "Get keys from object.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "Object.keys",
    "hint": "Use Object.keys()."
  },
  {
    "id": 116,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Date",
    "prompt": "Create current date.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "new Date",
    "hint": "Use new Date()."
  },
  {
    "id": 117,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Set Timeout",
    "prompt": "Run function after 1 second.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "setTimeout",
    "hint": "Use setTimeout."
  },
  {
    "id": 118,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Form Validation",
    "prompt": "Validate empty input.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "trim",
    "hint": "Use trim()."
  },
  {
    "id": 119,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Mini Todo",
    "prompt": "Add task object to array.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "push",
    "hint": "Push object."
  },
  {
    "id": 120,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "API Render",
    "prompt": "Fetch stats and render total problems.",
    "starter": "// Write your JavaScript answer here\n",
    "solution_key": "fetch",
    "hint": "Combine fetch and DOM."
  },
  {
    "id": 121,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Select All",
    "prompt": "Select all students.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "SELECT *",
    "hint": "Use SELECT * FROM students;"
  },
  {
    "id": 122,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Select Columns",
    "prompt": "Select name and grade only.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "SELECT name",
    "hint": "Choose columns after SELECT."
  },
  {
    "id": 123,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Where Equals",
    "prompt": "Find Python students.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "WHERE",
    "hint": "Use WHERE language = 'Python'."
  },
  {
    "id": 124,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Where Comparison",
    "prompt": "Find grades >= 85.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": ">=",
    "hint": "Use WHERE grade >= 85."
  },
  {
    "id": 125,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Order By",
    "prompt": "Order students by grade.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "ORDER BY",
    "hint": "Use ORDER BY grade DESC."
  },
  {
    "id": 126,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Limit",
    "prompt": "Return first 3 rows.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "LIMIT",
    "hint": "Use LIMIT 3."
  },
  {
    "id": 127,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Distinct",
    "prompt": "Show unique languages.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "DISTINCT",
    "hint": "Use SELECT DISTINCT."
  },
  {
    "id": 128,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Like",
    "prompt": "Find names starting with A.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "LIKE",
    "hint": "Use LIKE 'A%'."
  },
  {
    "id": 129,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Between",
    "prompt": "Find grades between 80 and 95.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "BETWEEN",
    "hint": "Use BETWEEN."
  },
  {
    "id": 130,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "In",
    "prompt": "Find Python or SQL students.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "IN",
    "hint": "Use IN ('Python','SQL')."
  },
  {
    "id": 131,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Beginner",
    "title": "Count",
    "prompt": "Count all students.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "COUNT",
    "hint": "Use COUNT(*)."
  },
  {
    "id": 132,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Beginner",
    "title": "Average",
    "prompt": "Average grade.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "AVG",
    "hint": "Use AVG(grade)."
  },
  {
    "id": 133,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Beginner",
    "title": "Max",
    "prompt": "Highest grade.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "MAX",
    "hint": "Use MAX(grade)."
  },
  {
    "id": 134,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Beginner",
    "title": "Min",
    "prompt": "Lowest grade.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "MIN",
    "hint": "Use MIN(grade)."
  },
  {
    "id": 135,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Beginner",
    "title": "Sum",
    "prompt": "Total expenses.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "SUM",
    "hint": "Use SUM(amount)."
  },
  {
    "id": 136,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Beginner",
    "title": "Group By",
    "prompt": "Average grade by language.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "GROUP BY",
    "hint": "Use GROUP BY language."
  },
  {
    "id": 137,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Beginner",
    "title": "Having",
    "prompt": "Languages with avg grade > 85.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "HAVING",
    "hint": "Use HAVING AVG(grade)>85."
  },
  {
    "id": 138,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Beginner",
    "title": "Round",
    "prompt": "Round average grade.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "ROUND",
    "hint": "Use ROUND(AVG(...),1)."
  },
  {
    "id": 139,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Beginner",
    "title": "Alias",
    "prompt": "Alias avg grade as average_grade.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "AS",
    "hint": "Use AS."
  },
  {
    "id": 140,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Beginner",
    "title": "Order Aggregate",
    "prompt": "Order categories by total spending.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "ORDER BY",
    "hint": "Use ORDER BY SUM(amount) DESC."
  },
  {
    "id": 141,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Intermediate",
    "title": "Insert",
    "prompt": "Insert a new student.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "INSERT INTO",
    "hint": "Use INSERT INTO."
  },
  {
    "id": 142,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Intermediate",
    "title": "Update",
    "prompt": "Update a student's grade.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "UPDATE",
    "hint": "Use UPDATE ... SET ... WHERE."
  },
  {
    "id": 143,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Intermediate",
    "title": "Delete",
    "prompt": "Delete an expense by id.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "DELETE FROM",
    "hint": "Use DELETE FROM ... WHERE."
  },
  {
    "id": 144,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Intermediate",
    "title": "Create Table",
    "prompt": "Create projects table.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "CREATE TABLE",
    "hint": "Use CREATE TABLE."
  },
  {
    "id": 145,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Intermediate",
    "title": "Alter Concept",
    "prompt": "Explain adding a column to a table.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "ALTER TABLE",
    "hint": "Use ALTER TABLE concept."
  },
  {
    "id": 146,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Intermediate",
    "title": "Not Null",
    "prompt": "Create column that cannot be null.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "NOT NULL",
    "hint": "Use NOT NULL."
  },
  {
    "id": 147,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Intermediate",
    "title": "Primary Key",
    "prompt": "Create id primary key.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "PRIMARY KEY",
    "hint": "Use PRIMARY KEY."
  },
  {
    "id": 148,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Intermediate",
    "title": "Default Value",
    "prompt": "Create status default Idea.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "DEFAULT",
    "hint": "Use DEFAULT."
  },
  {
    "id": 149,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Intermediate",
    "title": "Check Constraint",
    "prompt": "Require grade >= 0.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "CHECK",
    "hint": "Use CHECK."
  },
  {
    "id": 150,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Intermediate",
    "title": "Transaction Concept",
    "prompt": "Show begin/commit idea.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "COMMIT",
    "hint": "Use COMMIT."
  },
  {
    "id": 151,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Intermediate",
    "title": "Inner Join",
    "prompt": "Write an INNER JOIN example.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "JOIN",
    "hint": "Use JOIN ON."
  },
  {
    "id": 152,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Intermediate",
    "title": "Left Join",
    "prompt": "Write a LEFT JOIN example.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "LEFT JOIN",
    "hint": "Use LEFT JOIN."
  },
  {
    "id": 153,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Intermediate",
    "title": "Foreign Key Concept",
    "prompt": "Explain foreign key relationship.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "FOREIGN KEY",
    "hint": "Use FOREIGN KEY."
  },
  {
    "id": 154,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Intermediate",
    "title": "Join Filter",
    "prompt": "Join and filter by grade.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "JOIN",
    "hint": "Use JOIN plus WHERE."
  },
  {
    "id": 155,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Intermediate",
    "title": "Join Aggregate",
    "prompt": "Count sessions by student.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "COUNT",
    "hint": "Use JOIN plus GROUP BY."
  },
  {
    "id": 156,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Intermediate",
    "title": "Self Join Concept",
    "prompt": "Write self join pattern.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "JOIN",
    "hint": "Use table aliases."
  },
  {
    "id": 157,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Intermediate",
    "title": "Many to Many",
    "prompt": "Describe junction table.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "junction",
    "hint": "Use a linking table."
  },
  {
    "id": 158,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Intermediate",
    "title": "Union",
    "prompt": "Combine two select results.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "UNION",
    "hint": "Use UNION."
  },
  {
    "id": 159,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Intermediate",
    "title": "Subquery",
    "prompt": "Students above average grade.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "SELECT AVG",
    "hint": "Use subquery."
  },
  {
    "id": 160,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Intermediate",
    "title": "Exists",
    "prompt": "Use EXISTS in a query.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "EXISTS",
    "hint": "Use WHERE EXISTS."
  },
  {
    "id": 161,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Advanced",
    "title": "Case",
    "prompt": "Create pass/fail column.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "CASE",
    "hint": "Use CASE WHEN."
  },
  {
    "id": 162,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Advanced",
    "title": "Coalesce",
    "prompt": "Replace null with zero.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "COALESCE",
    "hint": "Use COALESCE."
  },
  {
    "id": 163,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Advanced",
    "title": "Cast",
    "prompt": "Convert value type.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "CAST",
    "hint": "Use CAST."
  },
  {
    "id": 164,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Advanced",
    "title": "Date Query",
    "prompt": "Filter by created_at date.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "created_at",
    "hint": "Use date column."
  },
  {
    "id": 165,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Advanced",
    "title": "Window Rank",
    "prompt": "Rank students by grade.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "RANK",
    "hint": "Use RANK() OVER."
  },
  {
    "id": 166,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Advanced",
    "title": "Row Number",
    "prompt": "Add row numbers.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "ROW_NUMBER",
    "hint": "Use ROW_NUMBER() OVER."
  },
  {
    "id": 167,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Advanced",
    "title": "CTE",
    "prompt": "Use WITH query.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "WITH",
    "hint": "Use WITH cte AS."
  },
  {
    "id": 168,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Advanced",
    "title": "Nested Aggregation",
    "prompt": "Find category above avg spending.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "AVG",
    "hint": "Use subquery."
  },
  {
    "id": 169,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Advanced",
    "title": "Performance Index",
    "prompt": "Create index on grade.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "INDEX",
    "hint": "Use CREATE INDEX."
  },
  {
    "id": 170,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Advanced",
    "title": "Explain Plan Concept",
    "prompt": "Explain checking query performance.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "EXPLAIN",
    "hint": "Use EXPLAIN concept."
  },
  {
    "id": 171,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Syntax Fix",
    "prompt": "Fix missing FROM in SELECT.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "FROM",
    "hint": "SELECT needs FROM."
  },
  {
    "id": 172,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Null Logic",
    "prompt": "Find rows where value is null.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "IS NULL",
    "hint": "Use IS NULL."
  },
  {
    "id": 173,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Not Equal",
    "prompt": "Find grades not equal to 95.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "!=",
    "hint": "Use != or <>."
  },
  {
    "id": 174,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Multiple Conditions",
    "prompt": "Use AND and OR correctly.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "AND",
    "hint": "Group conditions."
  },
  {
    "id": 175,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Business Report",
    "prompt": "Total and average expenses by category.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "GROUP BY",
    "hint": "Aggregate by category."
  },
  {
    "id": 176,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Top Student",
    "prompt": "Find student with highest grade.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "ORDER BY",
    "hint": "Order desc limit 1."
  },
  {
    "id": 177,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Data Quality",
    "prompt": "Find duplicate names.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "GROUP BY",
    "hint": "Group and count."
  },
  {
    "id": 178,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Safe Delete",
    "prompt": "Delete using WHERE condition.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "WHERE",
    "hint": "Never delete without WHERE."
  },
  {
    "id": 179,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Schema Design",
    "prompt": "Design students table.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "CREATE TABLE",
    "hint": "Use columns and types."
  },
  {
    "id": 180,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Certification Review",
    "prompt": "Write query using SELECT, WHERE, GROUP BY, HAVING, ORDER BY.",
    "starter": "-- Write your SQL answer here\n",
    "solution_key": "HAVING",
    "hint": "Combine clauses."
  },
  {
    "id": 181,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review Python #1",
    "prompt": "Complete a certification-style Python task using syntax and fundamentals concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 182,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #2",
    "prompt": "Complete a certification-style Python task using control flow concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 183,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Advanced",
    "title": "Exam Review Python #3",
    "prompt": "Complete a certification-style Python task using data structures concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 184,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Beginner",
    "title": "Exam Review Python #4",
    "prompt": "Complete a certification-style Python task using functions and modules concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 185,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #5",
    "prompt": "Complete a certification-style Python task using files, exceptions, oop concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 186,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review Python #6",
    "prompt": "Complete a certification-style Python task using exam style mixed concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 187,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review Python #7",
    "prompt": "Complete a certification-style Python task using syntax and fundamentals concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 188,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #8",
    "prompt": "Complete a certification-style Python task using control flow concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 189,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Advanced",
    "title": "Exam Review Python #9",
    "prompt": "Complete a certification-style Python task using data structures concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 190,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Beginner",
    "title": "Exam Review Python #10",
    "prompt": "Complete a certification-style Python task using functions and modules concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 191,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #11",
    "prompt": "Complete a certification-style Python task using files, exceptions, oop concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 192,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review Python #12",
    "prompt": "Complete a certification-style Python task using exam style mixed concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 193,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review Python #13",
    "prompt": "Complete a certification-style Python task using syntax and fundamentals concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 194,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #14",
    "prompt": "Complete a certification-style Python task using control flow concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 195,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Advanced",
    "title": "Exam Review Python #15",
    "prompt": "Complete a certification-style Python task using data structures concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 196,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Beginner",
    "title": "Exam Review Python #16",
    "prompt": "Complete a certification-style Python task using functions and modules concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 197,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #17",
    "prompt": "Complete a certification-style Python task using files, exceptions, oop concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 198,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review Python #18",
    "prompt": "Complete a certification-style Python task using exam style mixed concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 199,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review Python #19",
    "prompt": "Complete a certification-style Python task using syntax and fundamentals concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 200,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #20",
    "prompt": "Complete a certification-style Python task using control flow concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 201,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Advanced",
    "title": "Exam Review Python #21",
    "prompt": "Complete a certification-style Python task using data structures concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 202,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Beginner",
    "title": "Exam Review Python #22",
    "prompt": "Complete a certification-style Python task using functions and modules concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 203,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #23",
    "prompt": "Complete a certification-style Python task using files, exceptions, oop concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 204,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review Python #24",
    "prompt": "Complete a certification-style Python task using exam style mixed concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 205,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review Python #25",
    "prompt": "Complete a certification-style Python task using syntax and fundamentals concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 206,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #26",
    "prompt": "Complete a certification-style Python task using control flow concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 207,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Advanced",
    "title": "Exam Review Python #27",
    "prompt": "Complete a certification-style Python task using data structures concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 208,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Beginner",
    "title": "Exam Review Python #28",
    "prompt": "Complete a certification-style Python task using functions and modules concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 209,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #29",
    "prompt": "Complete a certification-style Python task using files, exceptions, oop concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 210,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review Python #30",
    "prompt": "Complete a certification-style Python task using exam style mixed concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 211,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review Python #31",
    "prompt": "Complete a certification-style Python task using syntax and fundamentals concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 212,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #32",
    "prompt": "Complete a certification-style Python task using control flow concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 213,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Advanced",
    "title": "Exam Review Python #33",
    "prompt": "Complete a certification-style Python task using data structures concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 214,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Beginner",
    "title": "Exam Review Python #34",
    "prompt": "Complete a certification-style Python task using functions and modules concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 215,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #35",
    "prompt": "Complete a certification-style Python task using files, exceptions, oop concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 216,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review Python #36",
    "prompt": "Complete a certification-style Python task using exam style mixed concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 217,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review Python #37",
    "prompt": "Complete a certification-style Python task using syntax and fundamentals concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 218,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #38",
    "prompt": "Complete a certification-style Python task using control flow concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 219,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Advanced",
    "title": "Exam Review Python #39",
    "prompt": "Complete a certification-style Python task using data structures concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 220,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Beginner",
    "title": "Exam Review Python #40",
    "prompt": "Complete a certification-style Python task using functions and modules concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 221,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #41",
    "prompt": "Complete a certification-style Python task using files, exceptions, oop concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 222,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review Python #42",
    "prompt": "Complete a certification-style Python task using exam style mixed concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 223,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review Python #43",
    "prompt": "Complete a certification-style Python task using syntax and fundamentals concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 224,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #44",
    "prompt": "Complete a certification-style Python task using control flow concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 225,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Advanced",
    "title": "Exam Review Python #45",
    "prompt": "Complete a certification-style Python task using data structures concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 226,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Beginner",
    "title": "Exam Review Python #46",
    "prompt": "Complete a certification-style Python task using functions and modules concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 227,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #47",
    "prompt": "Complete a certification-style Python task using files, exceptions, oop concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 228,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review Python #48",
    "prompt": "Complete a certification-style Python task using exam style mixed concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 229,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review Python #49",
    "prompt": "Complete a certification-style Python task using syntax and fundamentals concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 230,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #50",
    "prompt": "Complete a certification-style Python task using control flow concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 231,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Advanced",
    "title": "Exam Review Python #51",
    "prompt": "Complete a certification-style Python task using data structures concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 232,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Beginner",
    "title": "Exam Review Python #52",
    "prompt": "Complete a certification-style Python task using functions and modules concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 233,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #53",
    "prompt": "Complete a certification-style Python task using files, exceptions, oop concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 234,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review Python #54",
    "prompt": "Complete a certification-style Python task using exam style mixed concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 235,
    "language": "Python",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review Python #55",
    "prompt": "Complete a certification-style Python task using syntax and fundamentals concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 236,
    "language": "Python",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #56",
    "prompt": "Complete a certification-style Python task using control flow concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 237,
    "language": "Python",
    "domain": "Data Structures",
    "difficulty": "Advanced",
    "title": "Exam Review Python #57",
    "prompt": "Complete a certification-style Python task using data structures concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 238,
    "language": "Python",
    "domain": "Functions and Modules",
    "difficulty": "Beginner",
    "title": "Exam Review Python #58",
    "prompt": "Complete a certification-style Python task using functions and modules concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 239,
    "language": "Python",
    "domain": "Files, Exceptions, OOP",
    "difficulty": "Intermediate",
    "title": "Exam Review Python #59",
    "prompt": "Complete a certification-style Python task using files, exceptions, oop concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 240,
    "language": "Python",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review Python #60",
    "prompt": "Complete a certification-style Python task using exam style mixed concepts. Include working code and at least one clear output.",
    "starter": "# Write your Python certification review answer here\n",
    "solution_key": "print",
    "hint": "Most certification-style Python answers should show output with print()."
  },
  {
    "id": 241,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #1",
    "prompt": "Complete a certification-style JavaScript task using syntax and fundamentals concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 242,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #2",
    "prompt": "Complete a certification-style JavaScript task using control flow concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 243,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #3",
    "prompt": "Complete a certification-style JavaScript task using arrays and objects concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 244,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #4",
    "prompt": "Complete a certification-style JavaScript task using dom and browser concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 245,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #5",
    "prompt": "Complete a certification-style JavaScript task using async and modern js concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 246,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #6",
    "prompt": "Complete a certification-style JavaScript task using exam style mixed concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 247,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #7",
    "prompt": "Complete a certification-style JavaScript task using syntax and fundamentals concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 248,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #8",
    "prompt": "Complete a certification-style JavaScript task using control flow concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 249,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #9",
    "prompt": "Complete a certification-style JavaScript task using arrays and objects concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 250,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #10",
    "prompt": "Complete a certification-style JavaScript task using dom and browser concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 251,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #11",
    "prompt": "Complete a certification-style JavaScript task using async and modern js concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 252,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #12",
    "prompt": "Complete a certification-style JavaScript task using exam style mixed concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 253,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #13",
    "prompt": "Complete a certification-style JavaScript task using syntax and fundamentals concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 254,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #14",
    "prompt": "Complete a certification-style JavaScript task using control flow concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 255,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #15",
    "prompt": "Complete a certification-style JavaScript task using arrays and objects concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 256,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #16",
    "prompt": "Complete a certification-style JavaScript task using dom and browser concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 257,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #17",
    "prompt": "Complete a certification-style JavaScript task using async and modern js concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 258,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #18",
    "prompt": "Complete a certification-style JavaScript task using exam style mixed concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 259,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #19",
    "prompt": "Complete a certification-style JavaScript task using syntax and fundamentals concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 260,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #20",
    "prompt": "Complete a certification-style JavaScript task using control flow concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 261,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #21",
    "prompt": "Complete a certification-style JavaScript task using arrays and objects concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 262,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #22",
    "prompt": "Complete a certification-style JavaScript task using dom and browser concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 263,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #23",
    "prompt": "Complete a certification-style JavaScript task using async and modern js concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 264,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #24",
    "prompt": "Complete a certification-style JavaScript task using exam style mixed concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 265,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #25",
    "prompt": "Complete a certification-style JavaScript task using syntax and fundamentals concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 266,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #26",
    "prompt": "Complete a certification-style JavaScript task using control flow concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 267,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #27",
    "prompt": "Complete a certification-style JavaScript task using arrays and objects concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 268,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #28",
    "prompt": "Complete a certification-style JavaScript task using dom and browser concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 269,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #29",
    "prompt": "Complete a certification-style JavaScript task using async and modern js concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 270,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #30",
    "prompt": "Complete a certification-style JavaScript task using exam style mixed concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 271,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #31",
    "prompt": "Complete a certification-style JavaScript task using syntax and fundamentals concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 272,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #32",
    "prompt": "Complete a certification-style JavaScript task using control flow concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 273,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #33",
    "prompt": "Complete a certification-style JavaScript task using arrays and objects concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 274,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #34",
    "prompt": "Complete a certification-style JavaScript task using dom and browser concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 275,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #35",
    "prompt": "Complete a certification-style JavaScript task using async and modern js concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 276,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #36",
    "prompt": "Complete a certification-style JavaScript task using exam style mixed concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 277,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #37",
    "prompt": "Complete a certification-style JavaScript task using syntax and fundamentals concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 278,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #38",
    "prompt": "Complete a certification-style JavaScript task using control flow concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 279,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #39",
    "prompt": "Complete a certification-style JavaScript task using arrays and objects concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 280,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #40",
    "prompt": "Complete a certification-style JavaScript task using dom and browser concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 281,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #41",
    "prompt": "Complete a certification-style JavaScript task using async and modern js concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 282,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #42",
    "prompt": "Complete a certification-style JavaScript task using exam style mixed concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 283,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #43",
    "prompt": "Complete a certification-style JavaScript task using syntax and fundamentals concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 284,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #44",
    "prompt": "Complete a certification-style JavaScript task using control flow concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 285,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #45",
    "prompt": "Complete a certification-style JavaScript task using arrays and objects concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 286,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #46",
    "prompt": "Complete a certification-style JavaScript task using dom and browser concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 287,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #47",
    "prompt": "Complete a certification-style JavaScript task using async and modern js concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 288,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #48",
    "prompt": "Complete a certification-style JavaScript task using exam style mixed concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 289,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #49",
    "prompt": "Complete a certification-style JavaScript task using syntax and fundamentals concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 290,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #50",
    "prompt": "Complete a certification-style JavaScript task using control flow concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 291,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #51",
    "prompt": "Complete a certification-style JavaScript task using arrays and objects concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 292,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #52",
    "prompt": "Complete a certification-style JavaScript task using dom and browser concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 293,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #53",
    "prompt": "Complete a certification-style JavaScript task using async and modern js concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 294,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #54",
    "prompt": "Complete a certification-style JavaScript task using exam style mixed concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 295,
    "language": "JavaScript",
    "domain": "Syntax and Fundamentals",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #55",
    "prompt": "Complete a certification-style JavaScript task using syntax and fundamentals concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 296,
    "language": "JavaScript",
    "domain": "Control Flow",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #56",
    "prompt": "Complete a certification-style JavaScript task using control flow concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 297,
    "language": "JavaScript",
    "domain": "Arrays and Objects",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #57",
    "prompt": "Complete a certification-style JavaScript task using arrays and objects concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 298,
    "language": "JavaScript",
    "domain": "DOM and Browser",
    "difficulty": "Beginner",
    "title": "Exam Review JavaScript #58",
    "prompt": "Complete a certification-style JavaScript task using dom and browser concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 299,
    "language": "JavaScript",
    "domain": "Async and Modern JS",
    "difficulty": "Intermediate",
    "title": "Exam Review JavaScript #59",
    "prompt": "Complete a certification-style JavaScript task using async and modern js concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 300,
    "language": "JavaScript",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review JavaScript #60",
    "prompt": "Complete a certification-style JavaScript task using exam style mixed concepts. Include working code.",
    "starter": "// Write your JavaScript certification review answer here\n",
    "solution_key": "console.log",
    "hint": "Use console.log() to show your result."
  },
  {
    "id": 301,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #1",
    "prompt": "Complete a certification-style SQL task using basic select concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 302,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #2",
    "prompt": "Complete a certification-style SQL task using aggregation concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 303,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #3",
    "prompt": "Complete a certification-style SQL task using data modification concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 304,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #4",
    "prompt": "Complete a certification-style SQL task using joins and relationships concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 305,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #5",
    "prompt": "Complete a certification-style SQL task using advanced querying concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 306,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #6",
    "prompt": "Complete a certification-style SQL task using exam style mixed concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 307,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #7",
    "prompt": "Complete a certification-style SQL task using basic select concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 308,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #8",
    "prompt": "Complete a certification-style SQL task using aggregation concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 309,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #9",
    "prompt": "Complete a certification-style SQL task using data modification concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 310,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #10",
    "prompt": "Complete a certification-style SQL task using joins and relationships concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 311,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #11",
    "prompt": "Complete a certification-style SQL task using advanced querying concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 312,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #12",
    "prompt": "Complete a certification-style SQL task using exam style mixed concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 313,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #13",
    "prompt": "Complete a certification-style SQL task using basic select concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 314,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #14",
    "prompt": "Complete a certification-style SQL task using aggregation concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 315,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #15",
    "prompt": "Complete a certification-style SQL task using data modification concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 316,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #16",
    "prompt": "Complete a certification-style SQL task using joins and relationships concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 317,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #17",
    "prompt": "Complete a certification-style SQL task using advanced querying concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 318,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #18",
    "prompt": "Complete a certification-style SQL task using exam style mixed concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 319,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #19",
    "prompt": "Complete a certification-style SQL task using basic select concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 320,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #20",
    "prompt": "Complete a certification-style SQL task using aggregation concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 321,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #21",
    "prompt": "Complete a certification-style SQL task using data modification concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 322,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #22",
    "prompt": "Complete a certification-style SQL task using joins and relationships concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 323,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #23",
    "prompt": "Complete a certification-style SQL task using advanced querying concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 324,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #24",
    "prompt": "Complete a certification-style SQL task using exam style mixed concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 325,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #25",
    "prompt": "Complete a certification-style SQL task using basic select concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 326,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #26",
    "prompt": "Complete a certification-style SQL task using aggregation concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 327,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #27",
    "prompt": "Complete a certification-style SQL task using data modification concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 328,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #28",
    "prompt": "Complete a certification-style SQL task using joins and relationships concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 329,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #29",
    "prompt": "Complete a certification-style SQL task using advanced querying concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 330,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #30",
    "prompt": "Complete a certification-style SQL task using exam style mixed concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 331,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #31",
    "prompt": "Complete a certification-style SQL task using basic select concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 332,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #32",
    "prompt": "Complete a certification-style SQL task using aggregation concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 333,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #33",
    "prompt": "Complete a certification-style SQL task using data modification concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 334,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #34",
    "prompt": "Complete a certification-style SQL task using joins and relationships concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 335,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #35",
    "prompt": "Complete a certification-style SQL task using advanced querying concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 336,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #36",
    "prompt": "Complete a certification-style SQL task using exam style mixed concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 337,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #37",
    "prompt": "Complete a certification-style SQL task using basic select concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 338,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #38",
    "prompt": "Complete a certification-style SQL task using aggregation concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 339,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #39",
    "prompt": "Complete a certification-style SQL task using data modification concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 340,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #40",
    "prompt": "Complete a certification-style SQL task using joins and relationships concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 341,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #41",
    "prompt": "Complete a certification-style SQL task using advanced querying concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 342,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #42",
    "prompt": "Complete a certification-style SQL task using exam style mixed concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 343,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #43",
    "prompt": "Complete a certification-style SQL task using basic select concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 344,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #44",
    "prompt": "Complete a certification-style SQL task using aggregation concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 345,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #45",
    "prompt": "Complete a certification-style SQL task using data modification concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 346,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #46",
    "prompt": "Complete a certification-style SQL task using joins and relationships concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 347,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #47",
    "prompt": "Complete a certification-style SQL task using advanced querying concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 348,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #48",
    "prompt": "Complete a certification-style SQL task using exam style mixed concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 349,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #49",
    "prompt": "Complete a certification-style SQL task using basic select concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 350,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #50",
    "prompt": "Complete a certification-style SQL task using aggregation concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 351,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #51",
    "prompt": "Complete a certification-style SQL task using data modification concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 352,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #52",
    "prompt": "Complete a certification-style SQL task using joins and relationships concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 353,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #53",
    "prompt": "Complete a certification-style SQL task using advanced querying concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 354,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #54",
    "prompt": "Complete a certification-style SQL task using exam style mixed concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 355,
    "language": "SQL",
    "domain": "Basic SELECT",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #55",
    "prompt": "Complete a certification-style SQL task using basic select concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 356,
    "language": "SQL",
    "domain": "Aggregation",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #56",
    "prompt": "Complete a certification-style SQL task using aggregation concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 357,
    "language": "SQL",
    "domain": "Data Modification",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #57",
    "prompt": "Complete a certification-style SQL task using data modification concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 358,
    "language": "SQL",
    "domain": "Joins and Relationships",
    "difficulty": "Beginner",
    "title": "Exam Review SQL #58",
    "prompt": "Complete a certification-style SQL task using joins and relationships concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 359,
    "language": "SQL",
    "domain": "Advanced Querying",
    "difficulty": "Intermediate",
    "title": "Exam Review SQL #59",
    "prompt": "Complete a certification-style SQL task using advanced querying concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  },
  {
    "id": 360,
    "language": "SQL",
    "domain": "Exam Style Mixed",
    "difficulty": "Advanced",
    "title": "Exam Review SQL #60",
    "prompt": "Complete a certification-style SQL task using exam style mixed concepts. Write a valid query.",
    "starter": "-- Write your SQL certification review answer here\n",
    "solution_key": "SELECT",
    "hint": "Most SQL exam queries begin with SELECT."
  }
]

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language TEXT NOT NULL,
        topic TEXT NOT NULL,
        minutes INTEGER NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS problem_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER NOT NULL,
        language TEXT NOT NULL,
        domain TEXT,
        difficulty TEXT NOT NULL,
        completed_at TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        language TEXT NOT NULL,
        grade INTEGER NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        amount REAL NOT NULL
    )""")
    cur.execute("SELECT COUNT(*) AS count FROM students")
    if cur.fetchone()["count"] == 0:
        cur.executemany("INSERT INTO students (name, language, grade) VALUES (?, ?, ?)", [
            ("Brandon", "Python", 95), ("Alex", "JavaScript", 88), ("Mia", "SQL", 91),
            ("Jordan", "Python", 78), ("Taylor", "JavaScript", 84)
        ])
    cur.execute("SELECT COUNT(*) AS count FROM expenses")
    if cur.fetchone()["count"] == 0:
        cur.executemany("INSERT INTO expenses (category, amount) VALUES (?, ?)", [
            ("Food", 45.25), ("Food", 18.10), ("Gas", 52.00),
            ("School", 80.00), ("Subscriptions", 15.99), ("Subscriptions", 12.99)
        ])
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("static", "service-worker.js")


@app.route("/api/guided-lessons")
def guided_lessons():
    language = request.args.get("language", "").strip()
    lessons = GUIDED_LESSONS
    if language:
        lessons = [lesson for lesson in lessons if lesson["language"].lower() == language.lower()]
    return jsonify(lessons)

@app.route("/api/check-guided-step", methods=["POST"])
def check_guided_step():
    data = request.get_json()
    lesson_id = data.get("lesson_id", "")
    step_index = int(data.get("step_index", 0))
    answer = data.get("answer", "")

    lesson = next((item for item in GUIDED_LESSONS if item["id"] == lesson_id), None)
    if not lesson:
        return jsonify({"ok": False, "message": "Lesson not found."}), 404

    if step_index < 0 or step_index >= len(lesson["steps"]):
        return jsonify({"ok": False, "message": "Step not found."}), 404

    step = lesson["steps"][step_index]
    key = step.get("answer_key") or step.get("check") or ""

    if key.lower() in answer.lower():
        return jsonify({"ok": True, "message": "Correct. Move to the next step."})

    return jsonify({"ok": False, "message": "Not quite. " + step.get("hint", "Review the explanation and try again.")})

@app.route("/api/domains")
def get_domains():
    language = request.args.get("language", "")
    domains = sorted(set(p["domain"] for p in PRACTICE_PROBLEMS if not language or p["language"].lower() == language.lower()))
    return jsonify(domains)

@app.route("/api/practice")
def get_practice():
    language = request.args.get("language", "").strip()
    difficulty = request.args.get("difficulty", "").strip()
    domain = request.args.get("domain", "").strip()
    results = PRACTICE_PROBLEMS
    if language:
        results = [p for p in results if p["language"].lower() == language.lower()]
    if difficulty and difficulty != "All":
        results = [p for p in results if p["difficulty"].lower() == difficulty.lower()]
    if domain and domain != "All":
        results = [p for p in results if p["domain"].lower() == domain.lower()]
    return jsonify(results)

@app.route("/api/check-practice", methods=["POST"])
def check_practice():
    data = request.get_json()
    problem_id = int(data.get("problem_id", 0))
    answer = data.get("answer", "")
    problem = next((p for p in PRACTICE_PROBLEMS if p["id"] == problem_id), None)
    if not problem:
        return jsonify({"ok": False, "message": "Problem not found."}), 404
    if problem["solution_key"].lower() in answer.lower():
        conn = get_connection()
        conn.execute("INSERT INTO problem_progress (problem_id, language, domain, difficulty, completed_at) VALUES (?, ?, ?, ?, ?)",
                     (problem["id"], problem["language"], problem["domain"], problem["difficulty"], datetime.now().isoformat(timespec="seconds")))
        conn.commit()
        conn.close()
        return jsonify({"ok": True, "message": "Correct enough to move forward. Nice work."})
    return jsonify({"ok": False, "message": "Not quite. Hint: " + problem["hint"]})

@app.route("/api/stats")
def stats():
    conn = get_connection()
    total_minutes = conn.execute("SELECT COALESCE(SUM(minutes), 0) AS total FROM sessions").fetchone()["total"]
    completed = conn.execute("SELECT COUNT(DISTINCT problem_id) AS count FROM problem_progress").fetchone()["count"]
    by_language = conn.execute("SELECT language, COUNT(DISTINCT problem_id) AS completed FROM problem_progress GROUP BY language ORDER BY completed DESC").fetchall()
    by_domain = conn.execute("SELECT language, domain, COUNT(DISTINCT problem_id) AS completed FROM problem_progress GROUP BY language, domain ORDER BY language, domain").fetchall()
    conn.close()
    return jsonify({
        "total_minutes": total_minutes,
        "completed_problems": completed,
        "total_problems": len(PRACTICE_PROBLEMS),
        "by_language": [dict(row) for row in by_language],
        "by_domain": [dict(row) for row in by_domain]
    })

@app.route("/api/sessions", methods=["GET", "POST"])
def sessions():
    conn = get_connection()
    if request.method == "POST":
        data = request.get_json()
        language = data.get("language", "").strip()
        topic = data.get("topic", "").strip()
        notes = data.get("notes", "").strip()
        try:
            minutes = int(data.get("minutes", 0))
        except ValueError:
            conn.close()
            return jsonify({"error": "Minutes must be a number"}), 400
        if not language or not topic or minutes <= 0:
            conn.close()
            return jsonify({"error": "Language, topic, and positive minutes are required"}), 400
        conn.execute("INSERT INTO sessions (language, topic, minutes, notes, created_at) VALUES (?, ?, ?, ?, ?)",
                     (language, topic, minutes, notes, datetime.now().isoformat(timespec="seconds")))
        conn.commit()
        conn.close()
        return jsonify({"message": "Session saved"}), 201
    rows = conn.execute("SELECT * FROM sessions ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/run-python", methods=["POST"])
def run_python():
    data = request.get_json()
    code = data.get("code", "")
    blocked = ["open(", "exec(", "eval(", "__", "os.", "subprocess", "socket", "shutil", "pathlib"]
    for word in blocked:
        if word in code.lower():
            return jsonify({"ok": False, "output": f"Blocked for safety: avoid using {word}."})
    output = io.StringIO()
    safe_globals = {"__builtins__": {
        "print": print, "range": range, "len": len, "sum": sum, "min": min, "max": max,
        "round": round, "str": str, "int": int, "float": float, "list": list,
        "dict": dict, "set": set, "enumerate": enumerate, "sorted": sorted, "zip": zip, "map": map
    }}
    try:
        with contextlib.redirect_stdout(output):
            exec(code, safe_globals, {})
        return jsonify({"ok": True, "output": output.getvalue() or "Code ran with no printed output."})
    except Exception as e:
        return jsonify({"ok": False, "output": f"{type(e).__name__}: {e}"})

@app.route("/api/run-sql", methods=["POST"])
def run_sql():
    data = request.get_json()
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"ok": False, "error": "Enter a SQL query."}), 400
    lowered = query.lower()
    if any(word in lowered for word in ["drop", "attach", "detach", "pragma"]):
        return jsonify({"ok": False, "error": "That SQL command is blocked."}), 400
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query)
        if lowered.startswith("select") or lowered.startswith("with") or lowered.startswith("explain"):
            rows = cur.fetchall()
            columns = [d[0] for d in cur.description] if cur.description else []
            conn.close()
            return jsonify({"ok": True, "columns": columns, "rows": [list(row) for row in rows], "message": f"{len(rows)} row(s) returned."})
        conn.commit()
        affected = cur.rowcount
        conn.close()
        return jsonify({"ok": True, "columns": [], "rows": [], "message": f"Query ran successfully. Rows affected: {affected}"})
    except Exception as e:
        conn.close()
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {e}"}), 400

@app.route("/api/ask", methods=["POST"])
def ask_tutor():
    data = request.get_json()
    question = data.get("question", "").strip()
    context = data.get("context", "").strip()

    if not question:
        return jsonify({"answer": "Ask me a Python, JavaScript, SQL, or app-building question."})

    q = question.lower()

    python_topics = ["python", "def ", "function", "list", "dictionary", "loop", "if", "class", "exception", "try", "except"]
    js_topics = ["javascript", "js", "console.log", "dom", "event", "array", "object", "fetch", "async", "promise"]
    sql_topics = ["sql", "select", "where", "join", "group by", "order by", "insert", "update", "delete", "table"]

    if any(word in q for word in sql_topics):
        answer = (
            "For SQL, think in this order: SELECT the columns, FROM the table, WHERE filters rows, "
            "GROUP BY summarizes rows, HAVING filters groups, and ORDER BY sorts the final result. "
            "Example: SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC;"
        )
    elif any(word in q for word in js_topics):
        answer = (
            "For JavaScript, focus on variables, functions, arrays/objects, DOM events, and async fetch. "
            "If your code is not working, check the browser console first. A basic pattern is: "
            "const button = document.getElementById('btn'); button.addEventListener('click', () => { console.log('clicked'); });"
        )
    elif any(word in q for word in python_topics):
        answer = (
            "For Python, break the problem into inputs, processing, and output. Use print() to test each step. "
            "A function pattern is: def add(a, b): return a + b. For loops, start simple: for item in items: print(item)."
        )
    elif "error" in q or "bug" in q or "not working" in q:
        answer = (
            "Debugging checklist: 1) read the exact error message, 2) find the line number, "
            "3) check spelling/capitalization, 4) print or log values before the error, "
            "5) test one small piece at a time."
        )
    elif "certification" in q or "exam" in q:
        answer = (
            "For certification prep, complete every beginner, intermediate, and advanced domain. "
            "Then redo missed problems without hints. You should also take timed practice exams that match the official exam objectives."
        )
    else:
        answer = (
            "I can help with Python, JavaScript, SQL, debugging, and certification prep. "
            "Try asking something specific like: 'How do I use GROUP BY in SQL?' or 'How does a JavaScript event listener work?'"
        )

    if context:
        answer += " Based on the context you included, compare your code to the pattern above and check the key syntax carefully."

    return jsonify({"answer": answer})

init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
