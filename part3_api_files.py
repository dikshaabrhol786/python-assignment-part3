# ---------------- TASK 1: FILE HANDLING ----------------

# Writing to file
with open("python_notes.txt", "w", encoding="utf-8") as f:
    f.write("Topic 1: Variables store data. Python is dynamically typed.\n")
    f.write("Topic 2: Lists are ordered and mutable.\n")
    f.write("Topic 3: Dictionaries store key-value pairs.\n")
    f.write("Topic 4: Loops automate repetitive tasks.\n")
    f.write("Topic 5: Exception handling prevents crashes.\n")

print("File written successfully.")

# Appending extra lines
with open("python_notes.txt", "a", encoding="utf-8") as f:
    f.write("Topic 6: Functions help reuse code.\n")
    f.write("Topic 7: APIs allow communication between systems.\n")

print("Lines appended.")

# Reading file
with open("python_notes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("\nFile Content:")
for i, line in enumerate(lines, start=1):
    print(f"{i}. {line.strip()}")

print("\nTotal lines:", len(lines))

# Search keyword
keyword = input("\nEnter keyword to search: ").lower()
found = False

for line in lines:
    if keyword in line.lower():
        print(line.strip())
        found = True

if not found:
    print("No matching lines found.")


# ---------------- TASK 2: API ----------------

import requests

BASE_URL = "https://dummyjson.com/products"

# Fetch products
try:
    res = requests.get(f"{BASE_URL}?limit=20", timeout=5)
    data = res.json()

    products = data["products"]

    print("\nProducts List:")
    print("ID | Title | Category | Price | Rating")

    for p in products:
        print(p["id"], "|", p["title"], "|", p["category"], "|", p["price"], "|", p["rating"])

except Exception as e:
    print("Error fetching products:", e)


# Filter rating >= 4.5 and sort by price desc
filtered = [p for p in products if p["rating"] >= 4.5]
filtered.sort(key=lambda x: x["price"], reverse=True)

print("\nFiltered & Sorted Products:")
for p in filtered:
    print(p["title"], "-", p["price"], "-", p["rating"])


# Category search
try:
    res = requests.get(f"{BASE_URL}/category/laptops", timeout=5)
    laptops = res.json()["products"]

    print("\nLaptops:")
    for l in laptops:
        print(l["title"], "-", l["price"])

except Exception as e:
    print("Error fetching laptops:", e)


# POST request
try:
    new_product = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }

    res = requests.post(f"{BASE_URL}/add", json=new_product, timeout=5)
    print("\nPOST Response:", res.json())

except Exception as e:
    print("Error in POST:", e)


# ---------------- TASK 3: EXCEPTION HANDLING ----------------

# Safe divide
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print("\nSafe Divide Tests:")
print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))


# Safe file read
def read_file_safe(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")

print("\nReading files:")
print(read_file_safe("python_notes.txt"))
print(read_file_safe("ghost_file.txt"))


# Robust API with error handling
def fetch_product(product_id):
    try:
        res = requests.get(f"{BASE_URL}/{product_id}", timeout=5)

        if res.status_code == 404:
            print("Product not found.")
        else:
            data = res.json()
            print(data["title"], "-", data["price"])

    except requests.exceptions.ConnectionError:
        print("Connection failed.")
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except Exception as e:
        print("Error:", e)


# Input loop
while True:
    user_input = input("\nEnter product ID (1–100) or 'quit': ")

    if user_input.lower() == "quit":
        break

    if not user_input.isdigit():
        print("Invalid input. Enter a number.")
        continue

    pid = int(user_input)

    if pid < 1 or pid > 100:
        print("ID must be between 1 and 100.")
        continue

    fetch_product(pid)


# ---------------- TASK 4: LOGGING ----------------

from datetime import datetime

def log_error(message):
    with open("error_log.txt", "a") as f:
        time = datetime.now()
        f.write(f"[{time}] ERROR: {message}\n")


# Trigger ConnectionError
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except Exception as e:
    log_error(f"ConnectionError - {e}")


# Trigger 404
try:
    res = requests.get(f"{BASE_URL}/999", timeout=5)
    if res.status_code != 200:
        log_error("HTTPError - 404 Not Found for product ID 999")
except Exception as e:
    log_error(str(e))


# Print logs
print("\nError Logs:")
with open("error_log.txt", "r") as f:
    print(f.read())