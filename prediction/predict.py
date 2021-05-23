from flair.data import Sentence
from flair.models import SequenceTagger
from simpletransformers.classification import ClassificationModel
from scipy.special import softmax
import yaml

class Predictor(object):

    def __init__(self,):

        config = self.load_model_params()

        ner_model_path = config.get("ner_model_path","")
        sent_model_path = config.get("sent_model_path","")
        self.ner_model = self.load_ner_model(ner_model_path)
        self.sent_model = self.load_sent_model(sent_model_path)


    def load_ner_model(self,path):
        model = SequenceTagger.load(path)
        return model

    def load_sent_model(self,path):
        model = ClassificationModel(model_type="roberta",model_name = path, 
                                    use_cuda=False)
        return model
        
    def predict(self,data):
        if data.isinstance(str) or len(data) == 1:
            return predict_single(data)
        else:
            return predict_batch(data)
            

    def predict_single(self,text):
        output = {}
        
        #NER Inference
        sentence = Sentence(text)
        self.ner_model.predict(sentence)
        output["ner"] = sentence.to_dict(tag_type="ner")

        #Risk Analysis Inference
        pred,output = self.sent_model.predict(text)
        prob = softmax(output,axis=1)
        prob_risk =[x[1] for x in prob]
        pred_risk = [100*i for i in prob_risk]
        output["risk"] = pred_risk[0] #Assume single entry
        
        return output 

    def predict_batch(self,docs):
        outputs = []
        for doc in docs:
            outputs.append(self.predict_single(doc))
        return outputs
        
    def load_model_params(self):
        config_path = "./cfg.yaml"
        return yaml.load(open(config_path))["model_config"]



