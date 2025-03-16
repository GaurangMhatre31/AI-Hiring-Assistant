def generate_strings(n):
    
    result = []

    
    for i in range(1, n + 1):
        
        if i % 4 == 0 and i % 6 == 0:
            result.append("QuadHex")
        elif i % 4 == 0:
            result.append("Quad")
        elif i % 6 == 0:
            result.append("Hex")
        else:
            result.append(str(i))

    return result

# Example usage:
if __name__ == "__main__":
    n = int(input("Enter a positive integer n: "))
    print(generate_strings(n))