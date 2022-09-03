# Aspect-Based-Sentiment-Analysis-For-Turkish 
## T.C. Maltepe University Faculty of Engineering and Natural Sciences Software Engineering Department Capstone Project  


<br>


### 170706007 Mustafa Tayyip BAYRAM   
### 170706003 Furkan ÖCALAN  
#### Project Advisor: Assist. Prof. Dr. Volkan TUNALI  

<br>

![image](https://user-images.githubusercontent.com/60510780/188274717-44c00e19-b611-41d4-bdc5-86fc912c109d.png)
<hr>



## Specification about what we used and achieved.

***************
### Data

- Semaval16 Turkish data is used as a data.

***************

### Preprocessing

- Zemberek
- NLTK

***************

### Model Training

- Architecture
    - Multi-label Classification with pretrained model BERT.

- Inference Results
    - Accuracy: 0.69
    - Recall: 0.65

***************

### Application 

| Idx | Tool-Framework |
| ------ | ------ |
| Web | Flask |
| DBMS | MySQL |
| Visualization | Plotly |
| Template Management | Blueprint |

- Authentication
    - Login-register implementations.
- File
    - Processes from file uploading to analyze.
- Home
    - Processes from analyze to end of the application.
- Templates
    - Files required for rendering purpose.
- config
    - Database connection credentials.

***************
### Helper Tools 

| Idx | Tool-Framework |
| ------ | ------ |
| VCS | Github |
| Scrum Tool | Trello |
| Model Training | Google Collab & CUDA |

***************
### Project Reports

Under the Documents folder, all reports are accessible.

***************

Notebooks used to train the model for this application can be found [here](mutabay/credit-card-fraud-detection).

Size of the model prevents uploading itself.


<hr>

## Steps followed to setup the project

1. Initialise the application by downloading dependencies  by entering the following command in terminal, after getting into the project directory:

```(bash)
pip install -r requirements.txt
```

2. Get the model and put it Analyze/Models directory. [You can get it from notebook or contact us.]
3. Change database credentials according to your database. [apps/config.py line:13]
4. Start the application
```(bash)
$env:FLASK_ENV="development"    # [Use it only during the development stage.]
$env:FLASK_DEBUG=1              # [Use it only during the development stage.]
$env:FLASK_APP = ".\run.py"
flask run
```

<hr>

<br>

 
## Screenshots of the application

![image](https://user-images.githubusercontent.com/60510780/188276481-b07d8e3c-d8b5-4ec8-b15e-0ed2b543b5de.png)

![image](https://user-images.githubusercontent.com/60510780/188276482-e19940f0-a9c0-419b-9e65-e0bddb93bbd9.png)
![image](https://user-images.githubusercontent.com/60510780/188276486-cf87c5e4-c9a2-441b-8f7b-923551b88f8c.png)
![image](https://user-images.githubusercontent.com/60510780/188276489-dcc05015-741e-4013-b83e-0c6e0d99c13e.png)
![image](https://user-images.githubusercontent.com/60510780/188276497-18cef6a1-9bfe-4bd5-893a-6ec0929e775b.png)
![image](https://user-images.githubusercontent.com/60510780/188276508-fb256ae4-46fc-47c8-b088-a5bf8882a788.png)
![image](https://user-images.githubusercontent.com/60510780/188276510-5f834646-8eee-4487-a804-76ec0405346f.png)
![image](https://user-images.githubusercontent.com/60510780/188276502-43f2ceaa-b048-4f88-bafc-a48978c18611.png)
![image](https://user-images.githubusercontent.com/60510780/188276513-753a0d5e-4bdf-433b-940d-eeb67098ca1b.png)
![image](https://user-images.githubusercontent.com/60510780/188276515-5c6e62d2-cdea-455a-94be-bdd5cf41c4a7.png)
![image](https://user-images.githubusercontent.com/60510780/188276519-bf5ad25e-40a3-4f1d-a13f-c619e67a5d7f.png)

<hr>


To Contact Us::
- Mustafa Tayyip BAYRAM
    - [LinkedIn](https://www.linkedin.com/in/mutabay/)
- Furkan ÖCALAN
    - [LinkedIn](https://www.linkedin.com/in/furkan-ocalan-16186a174/)



