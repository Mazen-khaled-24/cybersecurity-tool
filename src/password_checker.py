import re

# Check if password appears in a simple wordlist
def is_in_wordlist(password):
    try:
        with open("wordlist.txt", "r") as f:
            words = f.read().splitlines()
            return password.lower() in [w.lower() for w in words]
    except FileNotFoundError:
        return False  # ignore if wordlist not found

def check_password_strength(password):
    score = 0
    suggestions = []

    # Length check
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters")

    # Numbers
    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Add numbers")

    # Symbols
    if re.search(r"[@#$%^&*?!]", password):
        score += 1
    else:
        suggestions.append("Add special characters (@#$%^&*?!)")

    # Wordlist check
    if is_in_wordlist(password):
        suggestions.append("Avoid using common or leaked passwords")
        score = max(0, score - 1)

    # Return strength result
    if score <= 2:
        strength = "Weak"
    elif score == 3 or score == 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, suggestions

def main():
    print("=== Password Strength Checker ===")
    password = input("Enter a password to check: ")

    strength, suggestions = check_password_strength(password)

    print(f"\nStrength: {strength}")
    if suggestions:
        print("\nSuggestions:")
        for s in suggestions:
            print(f"- {s}")

if __name__ == "__main__":
    main()
