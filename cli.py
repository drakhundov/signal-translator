from typing import List, Type


def user_select_from_list(msg: str, select: List[str], req_type: Type):
    print(msg)
    noptions = len(select)
    for i, item in enumerate(select):
        print(f"{i}: {item}")
    raw = None
    while True:
        raw = input("Select an option: ")
        if req_type == int and not raw.isdigit():
            print("Please enter a number")
            continue
        elif int(raw) > noptions:
            print("Please enter a valid option")
        else:
            break
    return req_type(raw)
