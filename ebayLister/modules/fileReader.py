def fileReader():
    file = open("../barcodes.txt", "r") # Open
    read = file.read() # Read
    fileList = read.splitlines() # Convert
    search_terms = list(dict.fromkeys(fileList)) # Remove duplicates

    return search_terms