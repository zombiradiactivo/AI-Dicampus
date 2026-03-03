def find_duplicates_and_count(data: list) -> dict:
    """Encuentra elementos duplicados y cuántas veces aparecen."""
    result = {}
    for i in range(len(data)):
        count = 0
        for j in range(len(data)):
            if data[i] == data[j]:
                count += 1
        if count > 1 and data[i] not in result:
            result[data[i]] = count
    return result