#Opener

def opener(file):
    """Function that opens a provided file and reads it, skipping lines starting with # symbol and converting values into integers.
    Function also skips single connections. Converts values into integers.
    Creates a matrix with only unique connections."""
    with open(file) as reader:
        temp= []
        perm = []
        for line in reader.readlines(): # Read each line in file
            if line.startswith("#"): # Skips lines that starts with # symbol 
                continue
            line= line.strip("\n") # Strip each line with \n symbol
            values = line.split(",") # Divide each line by the comma 
            temp.append(values)
    for connection in temp:
        point1, point2 = connection
        try: # Try to turn the values into integers 
            num1 =int(point1)
            num2 =int(point2)
            perm.append(num1)
            perm.append(num2)
        except ValueError: # Skip single connections 
            print(f"Removed single connection {connection}")
    matrix = [perm[i:i+2] for i in range(0, len(perm), 2)] # Create matrix with adjacent values
    for connection in matrix: # Check if there are only unique connections
        point1, point2 = connection
        if point1==point2 or [point2, point1] in matrix:
            matrix.remove(connection)
            print(f"Removed non unique connection from graph: {connection}")
    return matrix
  
