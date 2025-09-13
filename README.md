# 🤖 AI-Powered Excel Mock Interviewer

An intelligent Excel skill assessment system powered by **Groq AI** that conducts personalized interviews, generates dynamic questions, and provides comprehensive performance analysis.

## ✨ Key Features

### 🧠 **AI-Powered Intelligence**
- **Dynamic Question Generation**: No pre-made questions - AI creates unique, contextual Excel problems
- **Intelligent Interview Conduct**: AI adapts to your responses and provides real-time feedback  
- **Comprehensive Analysis**: Detailed performance reports with personalized recommendations

### 🎯 **Smart Assessment**
- **Progressive Difficulty**: Questions scale from Intermediate → Intermediate-Advanced → Advanced
- **Contextual Awareness**: Each question builds on previous responses
- **Multi-Criteria Evaluation**: Assesses correctness, efficiency, and approach clarity

### 🌐 **Modern Web Interface**
- **Streamlit UI**: Clean, interactive web application
- **Real-Time Progress**: Live tracking of interview phases
- **Visual Analytics**: Charts and graphs for performance insights
- **Session Management**: Persistent state throughout the interview

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Edit .env and add your Groq API key
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Launch Application
```bash
# Easy launcher
python run_app.py

# Or directly
streamlit run streamlit_app.py
```

The application will automatically open in your web browser! 🌟

## 📋 Requirements

- **Python 3.8+**
- **Groq API Key** (Get free key at [console.groq.com](https://console.groq.com))
- **Internet Connection** (for AI services)

### Dependencies
- `groq==0.4.1` - AI service integration
- `streamlit==1.28.1` - Web interface  
- `python-dotenv==1.0.0` - Environment management
- `pandas==2.1.3` - Data handling
- `plotly==5.17.0` - Interactive visualizations

## 🎯 How It Works

### Interview Flow
1. **🚀 Introduction**: AI welcomes you and explains the assessment process
2. **❓ Dynamic Questions**: AI generates 3 progressive Excel questions based on:
   - Your skill level indicators
   - Previous responses
   - Real-world Excel scenarios
3. **💬 Interactive Dialogue**: AI provides immediate feedback and conducts follow-up
4. **📊 Comprehensive Report**: Final analysis with scores, strengths, and improvement areas

### AI Model Configuration
The system uses **gemma2-9b-it** by default for optimal performance. You can change this in `.env`:
```bash
GROQ_MODEL=gemma2-9b-it  # Fast, efficient model
```

## 📁 Project Structure

```
ExcelInterview/
├── .env                 # Your API configuration
├── .env.example        # Template for environment setup
├── requirements.txt    # Python dependencies
├── run_app.py         # Application launcher
├── streamlit_app.py   # Main Streamlit web interface
└── src/
    ├── groq_ai_service.py  # Groq AI integration
    ├── interviewer.py      # Core interview logic
    └── __init__.py
```

## 🔧 Configuration Options

### Environment Variables (.env)
```bash
# Required: Your Groq API key
GROQ_API_KEY=your_groq_api_key_here

# Optional: AI model selection
GROQ_MODEL=gemma2-9b-it

# Optional: Interview settings
MAX_QUESTIONS=3
DIFFICULTY_LEVELS=intermediate,intermediate_advanced,advanced
```

## 🎓 Assessment Criteria

The AI evaluates your responses based on:

- **🎯 Correctness** (40%): Does the solution work and achieve the goal?
- **⚡ Efficiency** (30%): Is this the most optimal approach?
- **💡 Clarity** (20%): How well do you explain your reasoning?
- **🔧 Excel Mastery** (10%): Depth of Excel knowledge demonstrated

## 🚀 Development

### Running in Development Mode
```bash
# Activate virtual environment (recommended)
python -m venv venv
venv\\Scripts\\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

## 🎯 Output

<img width="1919" height="864" alt="Screenshot 2025-09-13 213721" src="https://github.com/user-attachments/assets/041e271f-4878-4ea6-af06-ee24dc829da0" />
<img width="1919" height="866" alt="Screenshot 2025-09-13 213909" src="https://github.com/user-attachments/assets/2634d9ec-64bd-4f89-b154-c9dd190e277f" />
<img width="1919" height="853" alt="Screenshot 2025-09-13 214217" src="https://github.com/user-attachments/assets/f15d11ba-86ba-4164-a2bb-54b3f4377dc4" />
<img width="1919" height="867" alt="Screenshot 2025-09-13 214316" src="https://github.com/user-attachments/assets/ba8b9ea0-3e55-4798-9b38-00bdc10349f4" />
<img width="1919" height="873" alt="Screenshot 2025-09-13 214435" src="https://github.com/user-attachments/assets/9b8b4f7d-c3c7-4396-b31d-f74b271c82dd" />
<img width="1919" height="866" alt="Screenshot 2025-09-13 214442" src="https://github.com/user-attachments/assets/943385f5-f4db-4a37-8372-98e6b0ab6920" />


## 📄 License


This project is open source. Feel free to use, modify, and distribute according to your needs.

---

**🎯 Ready to test your Excel skills with AI?** 

Get your free Groq API key and launch the application to begin your personalized Excel assessment experience!
