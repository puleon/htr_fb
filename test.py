import requests


def test_respond():
    url = "http://0.0.0.0:8083/respond"

    request_data = {"image":"../data/75667.png",
            "min_confidence": 0.0}

    result = requests.post(url, json=request_data).json()

    print(result)

    gold_result = "Молодец"

    assert result == gold_result, f"Got\n{result}\n, but expected:\n{gold_result}"

    print("Success")
    

if __name__ == "__main__":
    test_respond()
