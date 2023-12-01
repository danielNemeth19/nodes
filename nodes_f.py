def create_test_list() -> list:
    test_data = [
            {"job_name": "root", "level": 0},
            {"job_name": "A", "level": 1},
            {"job_name": "A1", "level": 2},
            {"job_name": "A2", "level": 2},
            {"job_name": "B", "level": 1},
            {"job_name": "B1", "level": 2},
            {"job_name": "BB1", "level": 3},
            {"job_name": "BB2", "level": 3},
            {"job_name": "C", "level": 1}
    ]

    for i, data in enumerate(test_data):
        data['index'] = i
    return test_data


def add_parent(data: list) -> list:
    def _find_parent(level, index):
        if level == 0:
            return None, None
        level_needed = level - 1
        for node in reversed(data[:index]):
            if node["level"] == level_needed:
                return node["job_name"], node["index"]
        return None, None

    for node in data[:]:
        level, index = node["level"], node["index"]
        parent_name, parent_index = _find_parent(level, index)
        node["parent_name"] = parent_name
        node["parent_id"] = parent_index
    return data


def main():
    data = create_test_list()

    for node in add_parent(data):
        print(node)
    print("--"*10)


if __name__ == '__main__':
    main()
