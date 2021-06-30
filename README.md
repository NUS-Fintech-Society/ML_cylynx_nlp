# Cryptonews

This project was conducted by NUS Fintech Society and Cylynx to create a dashboard to predict the risk scores of entities in the cryptocurrency space. This can help organisations to at a glance view the history of security threats that exchanges/cryptocurrencies have experienced

## Quickstart

To run the application, use 
`streamlit run app.py` 
![](https://user-images.githubusercontent.com/52419450/121855110-927bc100-cd25-11eb-8d92-ca915b1ab585.png)

## Folder Structure
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

`main.py` - Main script which will run at a scheduled daily interval by airflow

## Running apps using Docker

The app is able to work using Docker-compose to access both the streamlit app and the neo4j instance. The `ML_Cylynx_NLP` directory is mounted as a volume to the docker container

`docker-compose up -d`

`localhost:8501` - Streamlit App
`localhost:7474` - Neo4J Browser 
`localhost:7687` - Cypher Shell - To Connect to Graph Database