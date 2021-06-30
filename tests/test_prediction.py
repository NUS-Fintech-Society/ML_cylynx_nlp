from cryptonews.prediction import predict #TODO: Change this to package import
import pandas as pd
import pytest
import time


@pytest.fixture()
def test_data_path():
    return "./tests/test_data.csv"


def test_prediction_output_single():
    text = "SpaceChain to Deploy Commercial Blockchain Tech With SpaceX Launches in June,The blockchain infrastructure provider said having an Ethereum node in space brings physical security when transacting in crypto assets"
    output = predict(text)
    assert isinstance(output, dict),"Output should be a dictionary"
    assert "ner" in output, "Output should contain ner_output"
    assert "risk" in output, "Output should contain risk scores"
    


def test_prediction_batch(test_data_path):
    df = pd.read_csv(test_data_path)
    df["title"].fillna("", inplace=True)
    df["excerpt"].fillna("", inplace=True)
    df["text"] = df["title"] + " " + df["excerpt"]
    docs = df["text"].tolist()
    start = time.time()
    output = predict(docs)
    end = time.time()
    print(
        f"Inference Time: {end-start} seconds to analyze {len(output)} documents ")
    assert isinstance(output, dict),"Batch output should be a list"
    assert "ner" in output.keys(),"Batch Output should contain ner output"
    assert "risk" in output.keys(),"Batch Output should contain risk scores"

