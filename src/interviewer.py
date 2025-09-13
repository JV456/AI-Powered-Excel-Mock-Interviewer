"""
AI-Powered Excel Mock Interviewer

Core interviewer class that manages the interview flow, state tracking, and question progression.
"""

import json
import random
from enum import Enum
from typing import Dict, List, Optional, Tuple


class InterviewPhase(Enum):
    """Enumeration of interview phases"""
    INTRODUCTION = "introduction"
    QUESTIONING = "questioning"
    CONCLUSION = "conclusion"


class QuestionDifficulty(Enum):
    """Enumeration of question difficulty levels"""
    INTERMEDIATE = "intermediate"
    INTERMEDIATE_ADVANCED = "intermediate_advanced"
    ADVANCED = "advanced"


class ExcelMockInterviewer:
    """
    Main class for conducting Excel proficiency interviews.
    
    Manages the three-phase interview process:
    1. Introduction Phase
    2. Question & Evaluation Phase (3 questions)
    3. Conclusion & Report Generation Phase
    """
    
    def __init__(self, groq_api_key: Optional[str] = None, total_questions: int = 3):
        """Initialize the interviewer with default state and Groq AI service"""
        self.phase = InterviewPhase.INTRODUCTION
        self.current_question_number = 0
        self.total_questions = total_questions
        self.user_responses = []
        self.evaluations = []
        self.questions_asked = []
        self.conversation_history = []
        self.is_ready = False
        
        # Initialize Groq AI service
        try:
            from .groq_ai_service import GroqAIService
            self.ai_service = GroqAIService(api_key=groq_api_key)
        except Exception as e:
            print(f"Error: Could not initialize Groq AI service: {e}")
            print("Please ensure your GROQ_API_KEY is set in the .env file")
            raise e
    
    def start_interview(self) -> str:
        """
        Start the interview with the introduction phase.
        
        Returns:
            str: Welcome message and interview explanation
        """
        self.phase = InterviewPhase.INTRODUCTION
        
        # Create dynamic question text and difficulty levels
        if self.total_questions == 3:
            question_text = "THREE"
            difficulty_text = """The questions will cover:
1. Intermediate level: Common data manipulation and lookup functions
2. Intermediate/Advanced level: More complex formulas and techniques  
3. Advanced level: Complex logical thinking and advanced scenarios"""
        elif self.total_questions == 4:
            question_text = "FOUR"
            difficulty_text = """The questions will cover:
1. Intermediate level: Basic functions and formulas
2. Intermediate level: Data manipulation and lookup functions  
3. Intermediate/Advanced level: More complex formulas and techniques
4. Advanced level: Complex logical thinking and advanced scenarios"""
        elif self.total_questions == 5:
            question_text = "FIVE"
            difficulty_text = """The questions will cover:
1. Intermediate level: Basic functions and formulas
2. Intermediate level: Data manipulation and lookup functions
3. Intermediate/Advanced level: Complex formulas and techniques
4. Intermediate/Advanced level: Advanced data analysis
5. Advanced level: Complex logical thinking and advanced scenarios"""
        else:
            question_text = f"{self.total_questions}"
            difficulty_text = f"The questions will progressively increase in difficulty across {self.total_questions} levels."
        
        introduction = f"""Hello! I'm your AI Excel Mock Interviewer. 

I'm a seasoned, professional senior analyst, and I'm here to assess your practical Excel skills through a structured interview process.

Here's how this will work:
• I will ask you {question_text} questions that progressively increase in difficulty
• For each question, please describe your approach and provide the specific formulas or functions you would use
• I'll evaluate your responses based on correctness, efficiency, and clarity of explanation
• At the end, I'll provide you with a comprehensive feedback report with actionable recommendations

{difficulty_text}"""
        
        return introduction
    
    def process_user_input(self, user_input: str) -> str:
        """
        Process user input based on current interview phase.
        
        Args:
            user_input (str): User's response
            
        Returns:
            str: Appropriate response based on current phase
        """
        user_input = user_input.strip().lower()
        
        if self.phase == InterviewPhase.INTRODUCTION:
            return self._handle_introduction_phase(user_input)
        elif self.phase == InterviewPhase.QUESTIONING:
            return self._handle_questioning_phase(user_input)
        elif self.phase == InterviewPhase.CONCLUSION:
            return self._handle_conclusion_phase()
        else:
            return "I'm sorry, there seems to be an error. Please restart the interview."
    
    def _handle_introduction_phase(self, user_input: str) -> str:
        """Handle user input during introduction phase"""
        ready_indicators = ['ready', 'yes', 'y', 'start', 'begin', 'go', 'sure', 'ok', 'okay']
        
        if any(indicator in user_input for indicator in ready_indicators):
            self.is_ready = True
            self.phase = InterviewPhase.QUESTIONING
            return self._ask_next_question()
        else:
            return """I understand you might need a moment. When you're ready to begin the Excel proficiency assessment, just let me know by typing 'ready' or 'yes'."""
    
    def _handle_questioning_phase(self, user_input: str) -> str:
        """Handle user input during questioning phase"""
        if self.current_question_number == 0:
            # This shouldn't happen, but handle gracefully
            return self._ask_next_question()
        
        # Store the user's response
        self.user_responses.append(user_input)
        
        # Add to conversation history
        current_question = self.questions_asked[self.current_question_number - 1]
        self.conversation_history.append({
            'question': current_question.get('question', ''),
            'answer': user_input,
            'question_number': self.current_question_number
        })
        
        # Evaluate the response using AI
        evaluation = self.ai_service.evaluate_answer(current_question, user_input)
        # Generate AI-powered feedback
        feedback = self.ai_service.conduct_interview_response(
            user_input, current_question, self.conversation_history
        )
        
        self.evaluations.append(evaluation)
        
        # Check if we need to ask the next question
        if self.current_question_number < self.total_questions:
            next_question = self._ask_next_question()
            return f"{feedback}\n\n{next_question}"
        else:
            # All questions answered, move to conclusion
            self.phase = InterviewPhase.CONCLUSION
            return f"{feedback}\n\nThank you for completing all {self.total_questions} questions! Let me generate your comprehensive feedback report..."
    
    def _handle_conclusion_phase(self) -> str:
        """Handle conclusion phase and generate report"""
        report = self.ai_service.generate_final_report(
            self.questions_asked,
            self.user_responses,
            self.evaluations
        )
        return report
    
    def _ask_next_question(self) -> str:
        """Generate and ask the next question based on difficulty progression"""
        self.current_question_number += 1
        
        # Determine difficulty level based on question number and total questions
        if self.total_questions == 3:
            # Original 3-question progression
            if self.current_question_number == 1:
                difficulty = QuestionDifficulty.INTERMEDIATE
            elif self.current_question_number == 2:
                difficulty = QuestionDifficulty.INTERMEDIATE_ADVANCED
            else:
                difficulty = QuestionDifficulty.ADVANCED
        elif self.total_questions == 4:
            # 4-question progression
            if self.current_question_number == 1:
                difficulty = QuestionDifficulty.INTERMEDIATE
            elif self.current_question_number == 2:
                difficulty = QuestionDifficulty.INTERMEDIATE
            elif self.current_question_number == 3:
                difficulty = QuestionDifficulty.INTERMEDIATE_ADVANCED
            else:
                difficulty = QuestionDifficulty.ADVANCED
        elif self.total_questions == 5:
            # 5-question progression
            if self.current_question_number == 1:
                difficulty = QuestionDifficulty.INTERMEDIATE
            elif self.current_question_number == 2:
                difficulty = QuestionDifficulty.INTERMEDIATE
            elif self.current_question_number in [3, 4]:
                difficulty = QuestionDifficulty.INTERMEDIATE_ADVANCED
            else:
                difficulty = QuestionDifficulty.ADVANCED
        else:
            # Fallback for any other number of questions
            third = self.total_questions // 3
            if self.current_question_number <= third:
                difficulty = QuestionDifficulty.INTERMEDIATE
            elif self.current_question_number <= 2 * third:
                difficulty = QuestionDifficulty.INTERMEDIATE_ADVANCED
            else:
                difficulty = QuestionDifficulty.ADVANCED
        
        # Generate context for AI-powered questions
        context = ""
        if self.conversation_history:
            prev_topics = [item.get('question', '')[:100] for item in self.conversation_history[-2:]]
            context = f"Previous questions covered: {'; '.join(prev_topics)}"
        
        # Generate the question using AI
        question = self.ai_service.generate_question(
            difficulty.value, 
            self.current_question_number,
            context
        )
        
        self.questions_asked.append(question)
        
        return f"**Question {self.current_question_number} ({difficulty.value.replace('_', '/').title()}):**\n\n{question['question']}"
    
    def get_interview_state(self) -> Dict:
        """
        Get current interview state for debugging or persistence.
        
        Returns:
            Dict: Current state information
        """
        return {
            'phase': self.phase.value,
            'current_question_number': self.current_question_number,
            'total_questions': self.total_questions,
            'questions_asked': len(self.questions_asked),
            'responses_received': len(self.user_responses),
            'is_ready': self.is_ready
        }
    
    def reset_interview(self):
        """Reset the interview to initial state"""
        self.phase = InterviewPhase.INTRODUCTION
        self.current_question_number = 0
        self.user_responses = []
        self.evaluations = []
        self.questions_asked = []
        self.conversation_history = []
        self.is_ready = False