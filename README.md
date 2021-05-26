# ML_cylynx_nlp

This project was conducted by NUS Fintech Society and Cylynx to create a dashboard to predict the risk scores of entities in the cryptocurrency space. This can help organisations to at a glance view the history of security threats that exchanges/cryptocurrencies have experienced

```bash
Code Structure
├── Dockerfile
├── README.md
├── app.py - Run the Application
├── cfg.yaml
├── database
├── prediction
│   ├── models #Models used 
│   │   ├── ner-model.pt
│   │   └── sent-model.bin
│   └── predict.py - # Function to perform inference on the dataset 
├── requirements.txt
├── scraping - # Scripts for Scraping
├── test - # Unit tests
└── training - # Training Notebooks and experimentation steps during model training 
```