from flair.data import Sentence
from flair.models import SequenceTagger
from simpletransformers.classification import ClassificationModel, ClassificationArgs
from scipy.special import softmax
import yaml


class Predictor(object):

    def __init__(self,):

        config = self.load_model_params()
        ner_model_path = config.get("ner_model_path", "")
        sent_model_path = config.get("sent_model_path", "")
        self.ner_model = self.load_ner_model(ner_model_path)
        self.sent_model = self.load_sent_model(sent_model_path)

    def load_ner_model(self, path):
        model = SequenceTagger.load(path)
        return model

    def load_sent_model(self, path):

        # TODO: Put Model Arguments into the config file
        args = ClassificationArgs()
        args.dynamic_quantize = True  # Using Dynamic Quantization to facilitate model speedup
        model = ClassificationModel(model_type="roberta", model_name=path,
                                    use_cuda=False, args=args)
        return model

    def parse_ner_output(self, ner_output):
        return [{"name": i["text"],
                 "type":i["labels"][0].value,
                 "confidence":i["labels"][0].score}
                for i in ner_output["entities"]]

    def predict_single(self, text):
        """
        Perform prediction on a single text entry
        Returns:
            output: dict
            output["ner"] - NER output
            output["risk"] - Risk score in %
        """
        output = {}

        # NER Inference
        sentence = Sentence(text)
        self.ner_model.predict(sentence)
        ner_output = sentence.to_dict(tag_type="ner")
        output["ner"] = self.parse_ner_output(ner_output)

        # Risk Analysis Inference
        assert isinstance(text, str)
        # Need to wrap text in a list else it will perform inference on characters
        pred, sent_output = self.sent_model.predict([text])
        prob = softmax(sent_output, axis=1)
        prob_risk = [x[1] for x in prob]
        pred_risk = [100*i for i in prob_risk]

        # Assume single entry
        output["risk"] = pred_risk[0]
        return output

    def predict_batch(self, docs):
        """
        Roberta Model can be parallelized rather well. More efficient to perform inference as a batch
        Parameters:
            docs: List[str]
        Returns:
            outputs: List[Dict]
        """
        sentences = [Sentence(i) for i in docs]
        self.ner_model.predict(sentences)
        ner_output = [self.parse_ner_output(sentence.to_dict(
            tag_type="ner")) for sentence in sentences]

        pred, sent_output = self.sent_model.predict(docs)
        prob = softmax(sent_output, axis=1)
        prob_risk = [x[1] for x in prob]
        pred_risk = [100*i for i in prob_risk]
        print(ner_output)
        output = [{"ner":ner_out, "risk": i}
                  for ner_out, i in zip(ner_output, pred_risk)]
        return output

    def load_model_params(self):
        #TODO: Change this 
        config_path = "/home/ubuntu/ML_cylynx_nlp/cfg.yaml"
        return yaml.load(open(config_path), Loader=yaml.Loader)["model_config"]


def predict(data):
    """
    General Predict Function that can be used to perform inference
    Parameters:
        data (str) or List[str]: data to be analysed 
    """
    predictor = Predictor()
    if isinstance(data, str):
        return predictor.predict_single(data)
    elif isinstance(data, list):
        return predictor.predict_batch(data)
    else:
        return
