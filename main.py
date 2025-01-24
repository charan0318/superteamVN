import json

# Load the database
def load_database(file_path):
    """
    Load the JSON database file and return it as a dictionary.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not a valid JSON file.")
        return None

# Parse the query into keywords
def parse_query(query):
    """
    Extract meaningful keywords from the user query.
    """
    # Split query into words and convert to lowercase
    return query.lower().split()

# Match members based on the query
def find_matching_members(query_keywords, database):
    """
    Match query keywords with members in the database.
    """
    matches = []

    for member in database["members"]:
        # Check if the member has matching skills
        matched_skills = [skill for skill in member["skills"] if skill.lower() in query_keywords]

        if matched_skills and member["availability"]:
            # Add member to matches with the number of matching skills
            matches.append({
                "member": member,
                "matches": len(matched_skills),
                "matched_skills": matched_skills
            })

    # Sort matches by the number of matching skills (highest first)
    matches.sort(key=lambda x: x["matches"], reverse=True)

    return matches

# Main function to handle the process
def main():
    # Load the JSON database
    database = load_database("members.json")
    if not database:
        return

    # Example user query
    query = input("Enter your query: ")  # e.g., "I want to find a RUST developer to build a DEFI project with Twitter integration."
    
    # Parse the query
    query_keywords = parse_query(query)
    
    # Find matching members
    matches = find_matching_members(query_keywords, database)
    
    # Output results
    if matches:
        print("\nMatched Members:")
        for match in matches:
            member = match["member"]
            print(f"- {member['name']} ({member['experience_years']} years): {member['bio']}")
            print(f"  Matched Skills: {', '.join(match['matched_skills'])}")
    else:
        print("NO relevant match found.")

# Run the main function
if __name__ == "__main__":
    main()
