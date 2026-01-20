# Aspect-Based Sentiment Analysis for Turkish

Capstone project developing a multi-label sentiment analysis system for Turkish language using BERT

## 📋 Project Information

**Institution**: T.C. Maltepe University  
**Faculty**: Engineering and Natural Sciences  
**Department**: Software Engineering  
**Type**: Capstone Project

**Team Members:**
- Mustafa Tayyip BAYRAM - [LinkedIn](https://www.linkedin.com/in/mutabay/)
- Furkan ÖCALAN - [LinkedIn](https://www.linkedin.com/in/furkan-ocalan-16186a174/)

**Advisor**: Assist. Prof. Dr. Volkan TUNALI

![Project Overview](https://user-images.githubusercontent.com/60510780/188274717-44c00e19-b611-41d4-bdc5-86fc912c109d.png)

## 📂 Structure

- **[Analyze/](Analyze/)** - Core analysis engine and model integration
- **[Models/](Models/)** - Classification models
- **[Documents/](Documents/)** - Project reports and documentation
- **[Semeval-Analysis/](Semeval-Analysis/)** - Dataset analysis scripts
- **[apps/](apps/)** - Flask application modules
- **[migrations/](migrations/)** - Database migrations
- **[uploads/](uploads/)** - User file uploads directory

## 🎯 Project Overview

A web-based application that performs aspect-based sentiment analysis on Turkish text using a fine-tuned BERT model. The system analyzes text to identify specific aspects and their associated sentiments.

## 🔬 Technical Implementation

### Dataset
- **Source**: SemEval 2016 Turkish dataset
- **Task**: Multi-label aspect-based sentiment classification

### Preprocessing Pipeline
- **Zemberek**: Turkish language processing
- **NLTK**: Natural language toolkit for text processing

### Model Architecture
- **Base Model**: Pre-trained BERT
- **Task**: Multi-label classification
- **Performance**:
  - Accuracy: 0.69
  - Recall: 0.65

### Web Application Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | Flask |
| Database | MySQL |
| Visualization | Plotly |
| Template System | Blueprint |
| Authentication | Login/Register system |

### Application Modules

- **Authentication**: User registration and login
- **File**: Upload and process text files
- **Home**: Main analysis interface
- **Templates**: Rendering components
- **Config**: Database configuration

## 🚀 Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Model Setup
Download the trained BERT model and place it in `Analyze/Models/` directory.  
*Note: Model size restrictions prevent direct upload. Contact team for access.*

### 3. Database Configuration
Update database credentials in `apps/config.py` (line 13)

### 4. Run Application
```bash
# Development mode
$env:FLASK_ENV="development"
$env:FLASK_DEBUG=1
$env:FLASK_APP=".\run.py"
flask run
```

## 📊 Application Screenshots

![Login Interface](https://user-images.githubusercontent.com/60510780/188276481-b07d8e3c-d8b5-4ec8-b15e-0ed2b543b5de.png)
![Registration](https://user-images.githubusercontent.com/60510780/188276482-e19940f0-a9c0-419b-9e65-e0bddb93bbd9.png)
![Dashboard](https://user-images.githubusercontent.com/60510780/188276486-cf87c5e4-c9a2-441b-8f7b-923551b88f8c.png)
![File Upload](https://user-images.githubusercontent.com/60510780/188276489-dcc05015-741e-4013-b83e-0c6e0d99c13e.png)
![Analysis View](https://user-images.githubusercontent.com/60510780/188276497-18cef6a1-9bfe-4bd5-893a-6ec0929e775b.png)
![Results Visualization](https://user-images.githubusercontent.com/60510780/188276508-fb256ae4-46fc-47c8-b088-a5bf8882a788.png)
![Sentiment Breakdown](https://user-images.githubusercontent.com/60510780/188276510-5f834646-8eee-4487-a804-76ec0405346f.png)
![Aspect Analysis](https://user-images.githubusercontent.com/60510780/188276502-43f2ceaa-b048-4f88-bafc-a48978c18611.png)
![Data Table](https://user-images.githubusercontent.com/60510780/188276513-753a0d5e-4bdf-433b-940d-eeb67098ca1b.png)
![Export Options](https https://user-images.githubusercontent.com/60510780/188276515-5c6e62d2-cdea-455a-94be-bdd5cf41c4a7.png)
![Statistics](https://user-images.githubusercontent.com/60510780/188276519-bf5ad25e-40a3-4f1d-a13f-c619e67a5d7f.png)

## 🛠️ Development Tools

| Purpose | Tool |
|---------|------|
| Version Control | GitHub |
| Project Management | Trello |
| Model Training | Google Colab with CUDA |

## 📚 Features

- Turkish language sentiment analysis
- Aspect-based opinion mining
- Multi-label classification
- Interactive data visualization
- File-based batch processing
- User authentication system
- Results export functionality

## 📖 Documentation

Complete project reports and documentation are available in the [Documents](Documents/) folder.

## 🔗 Related Resources

Similar app: [Credit Card Fraud Detection Repository](https://github.com/mutabay/credit-card-fraud-detection)

---

*Natural language processing application for Turkish sentiment analysis*
