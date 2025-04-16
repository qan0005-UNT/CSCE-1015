def validate_length(euid: str) -> bool:
    """
    Validate the length of the EUID.
    
    Args:
        euid: A string representing the EUID.

    Returns:
        bool: True if the length is valid, False otherwise.
        
    Rules:
    - Must be exactly 6 or 7 characters long.
    """
    
    return True 

def validate_contents(euid: str) -> bool:
    """
    Validate the structure and contents of the EUID.
    
    Args:
        euid: A string representing the EUID.

    Returns:
        bool: True if the contents are valid, False otherwise.
        
    Rules:
    - Starts with 2-3 lowercase letters.
    - Ends with exactly 4 digits.
    - Contains no special characters or uppercase letters.
    """
   
    return True

def validate(euid: str) -> bool:
    return validate_length(euid) and validate_contents(euid)

if __name__ == "__main__":
    # Prompt the user for their EUID,
    euid = input("Please enter your EUID: ").strip()

    if validate(euid):
        print(f"'{euid}' is a valid EUID")
    else:
        print(f"'{euid}' is NOT a valid EUID")