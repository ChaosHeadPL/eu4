import os
import json


BASE_DIR = os.path.dirname(__file__)

def laod_data():
    path = os.path.join(BASE_DIR, "eu4", "tests", "data_map.json")
    with open(path, "r") as json_file:
        data = json.load(json_file)

    return data


def show_data(data):
    header = ",".join(data[0].keys())
    print(header)
    output = []
    for row in data:
        # print(row)
        output.append(";".join(str(row[x]).replace("\n", ". ") for x in row.keys()))
    # print(data)
    # print("\n".join(output))

    return output

        
def save_to_csv(data):
    with open(os.path.join(BASE_DIR, "achievemenrs.csv"), "w") as file:
        for row in data:
            file.write(f"{row}\n")



def main():
    data = laod_data()
    output = show_data(data)
    save_to_csv(output)

    return True




if __name__ == "__main__":
    main()
