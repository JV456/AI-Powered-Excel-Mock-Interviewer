"""
Groq AI Integration for Excel Mock Interviewer

Handles AI-powered question generation, interview conducting, and evaluation using Groq's LLM API.
"""

import json
import os
from typing import Dict, List, Optional

from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()


class GroqAIService:
    """
    Service class for integrating with Groq AI API.
    
    Handles question generation, interview conducting, and answer evaluation.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemma2-9b-it"):
        """
        Initialize the Groq AI service.
        
        Args:
            api_key (Optional[str]): Groq API key. If None, will try to load from environment.
            model (str): Groq model to use for completions.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable or pass api_key parameter.")
        
        self.client = Groq(api_key=self.api_key)
        
        # System prompts for different tasks
        self.interview_conductor_prompt = self._get_interview_conductor_prompt()
        self.question_generator_prompt = self._get_question_generator_prompt()
        self.evaluator_prompt = self._get_evaluator_prompt()
    
    def generate_question(self, difficulty_level: str, question_number: int, context: str = "") -> Dict:
        """
        Generate a dynamic Excel question using Groq AI.
        
        Args:
            difficulty_level (str): The difficulty level (intermediate, intermediate_advanced, advanced)
            question_number (int): The current question number (1-3)
            context (str): Additional context about previous questions
            
        Returns:
            Dict: Generated question with metadata
        """
        prompt = f"""
{self.question_generator_prompt}

GENERATE EXCEL QUESTION:
- Difficulty Level: {difficulty_level}
- Question Number: {question_number}/3
- Context: {context if context else "First question of the interview"}

Requirements:
1. Create a realistic, practical Excel scenario
2. Make it relevant to business/professional contexts
3. Ensure it tests the appropriate skill level
4. Include specific data structures or examples
5. Make it different from typical textbook questions

Return your response as JSON with this exact structure:
{{
    "question": "Your detailed Excel question here...",
    "ideal_solution": "The best Excel formula/approach to solve this",
    "explanation": "Why this solution is optimal",
    "key_concepts": ["concept1", "concept2", "concept3"],
    "alternatives": ["alternative1", "alternative2"],
    "difficulty_justification": "Why this question fits the {difficulty_level} level"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response (in case there's extra text)
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                question_data = json.loads(json_str)
                
                # Add metadata
                question_data['generated_by'] = 'groq_ai'
                question_data['difficulty_level'] = difficulty_level
                question_data['question_number'] = question_number
                
                return question_data
            else:
                raise ValueError("No valid JSON found in response")
                
        except Exception as e:
            # Fallback to a basic question if AI generation fails
            return self._get_fallback_question(difficulty_level, question_number)
    
    def conduct_interview_response(self, user_answer: str, question: Dict, conversation_history: List[Dict]) -> str:
        """
        Generate an interview response using AI.
        
        Args:
            user_answer (str): The user's answer to evaluate
            question (Dict): The question that was asked
            conversation_history (List[Dict]): Previous conversation context
            
        Returns:
            str: AI-generated interview response
        """
        history_context = self._format_conversation_history(conversation_history)
        
        prompt = f"""
{self.interview_conductor_prompt}

CURRENT SITUATION:
Question Asked: {question.get('question', 'N/A')}
Ideal Solution: {question.get('ideal_solution', 'N/A')}
User's Answer: "{user_answer}"

Conversation History:
{history_context}

TASK: Provide a professional, encouraging interview response that:
1. Acknowledges their answer
2. Provides constructive feedback
3. Mentions the ideal solution if needed
4. Encourages them for the next question
5. Maintains a supportive, professional tone

Keep response concise but informative (2-3 paragraphs max).
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Thank you for your answer. {self._get_basic_feedback(user_answer, question)}"
    
    def evaluate_answer(self, question: Dict, user_answer: str) -> Dict:
        """
        Evaluate a user's answer using AI.
        
        Args:
            question (Dict): The question data
            user_answer (str): User's response
            
        Returns:
            Dict: Evaluation results with scores and feedback
        """
        prompt = f"""
{self.evaluator_prompt}

EVALUATION TASK:
Question: {question.get('question', 'N/A')}
Ideal Solution: {question.get('ideal_solution', 'N/A')}
User Answer: "{user_answer}"

Evaluate the answer on these criteria:
1. CORRECTNESS (0-10): Technical accuracy, will it work?
2. EFFICIENCY (0-10): Is there a better/more modern approach?
3. CLARITY (0-10): How well did they explain their reasoning?

Return your evaluation as JSON:
{{
    "correctness_score": 0-10,
    "efficiency_score": 0-10,
    "clarity_score": 0-10,
    "overall_score": 0-10,
    "feedback": "Specific feedback about their answer",
    "strengths": ["strength1", "strength2"],
    "areas_for_improvement": ["area1", "area2"],
    "recommendation": "Specific recommendation for improvement"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                evaluation = json.loads(json_str)
                
                # Ensure all required fields exist with defaults
                evaluation.setdefault('correctness_score', 5.0)
                evaluation.setdefault('efficiency_score', 5.0)
                evaluation.setdefault('clarity_score', 5.0)
                evaluation.setdefault('overall_score', 5.0)
                evaluation.setdefault('feedback', 'Thank you for your response.')
                evaluation.setdefault('strengths', [])
                evaluation.setdefault('areas_for_improvement', [])
                evaluation.setdefault('recommendation', 'Continue practicing Excel skills.')
                
                return evaluation
            else:
                raise ValueError("No valid JSON found in evaluation response")
                
        except Exception as e:
            # Return basic evaluation if AI fails
            return self._get_basic_evaluation(user_answer)
    
    def generate_final_report(self, questions: List[Dict], answers: List[str], evaluations: List[Dict]) -> str:
        """
        Generate a comprehensive final report using AI.
        
        Args:
            questions (List[Dict]): All questions asked
            answers (List[str]): All user answers
            evaluations (List[Dict]): All evaluations
            
        Returns:
            str: Comprehensive report
        """
        # Calculate overall metrics
        avg_correctness = sum(eval['correctness_score'] for eval in evaluations) / len(evaluations)
        avg_efficiency = sum(eval['efficiency_score'] for eval in evaluations) / len(evaluations)
        avg_clarity = sum(eval['clarity_score'] for eval in evaluations) / len(evaluations)
        overall_score = sum(eval['overall_score'] for eval in evaluations) / len(evaluations)
        
        # Format questions and answers for context
        qa_context = ""
        for i, (q, a, e) in enumerate(zip(questions, answers, evaluations), 1):
            qa_context += f"\nQ{i}: {q.get('question', 'N/A')[:100]}...\nA{i}: {a[:100]}...\nScore: {e['overall_score']}/10\n"
        
        prompt = f"""
You are generating a comprehensive Excel proficiency assessment report. Be professional, encouraging, and specific.

PERFORMANCE DATA:
Overall Score: {overall_score:.1f}/10
Correctness Average: {avg_correctness:.1f}/10
Efficiency Average: {avg_efficiency:.1f}/10
Clarity Average: {avg_clarity:.1f}/10

QUESTIONS AND ANSWERS:
{qa_context}

Generate a detailed report with these sections:

1. EXECUTIVE SUMMARY (2-3 sentences about overall performance)
2. PROFICIENCY LEVEL (Beginner/Intermediate/Advanced based on score)
3. STRENGTHS (What they did well)
4. AREAS FOR IMPROVEMENT (Specific skills to develop)
5. DETAILED QUESTION BREAKDOWN (Brief analysis of each question)
6. RECOMMENDATIONS (Specific next steps and study suggestions)
7. ENCOURAGEMENT (Motivational closing)

Make it professional but encouraging. Use specific Excel terminology and be actionable.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=2000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return self._get_basic_report(overall_score, evaluations)
    
    def _get_interview_conductor_prompt(self) -> str:
        """Get the system prompt for interview conducting"""
        return """
You are a professional, experienced Excel trainer and interviewer conducting a mock Excel proficiency assessment. Your role is to:

1. Be encouraging and supportive while maintaining professionalism
2. Provide constructive feedback on Excel solutions
3. Acknowledge correct approaches while suggesting improvements
4. Help candidates learn through your feedback
5. Use proper Excel terminology and concepts
6. Be specific about Excel functions and formulas

Your tone should be:
- Professional but warm
- Encouraging and supportive
- Constructive in feedback
- Specific about Excel concepts
- Educational and helpful

Always maintain the persona of a seasoned Excel expert who wants to help the candidate succeed.
"""
    
    def _get_question_generator_prompt(self) -> str:
        """Get the system prompt for question generation"""
        return """
You are an expert Excel trainer creating realistic, practical Excel assessment questions. Your questions should:

1. Be based on real-world business scenarios
2. Test practical Excel skills, not theoretical knowledge
3. Require specific Excel functions or approaches
4. Be appropriate for the specified difficulty level
5. Have clear, achievable solutions
6. Test different aspects of Excel proficiency

Difficulty Guidelines:
- INTERMEDIATE: Basic functions (VLOOKUP, SUMIF, PivotTables, basic formulas)
- INTERMEDIATE_ADVANCED: Complex formulas, array functions, dynamic ranges, advanced features
- ADVANCED: Complex business scenarios, financial modeling, advanced analysis, multiple function combinations

Always include realistic data examples and business context.
"""
    
    def _get_evaluator_prompt(self) -> str:
        """Get the system prompt for answer evaluation"""
        return """
You are an expert Excel assessor evaluating answers for correctness, efficiency, and clarity.

SCORING GUIDELINES:
CORRECTNESS (0-10):
- 9-10: Perfect solution, works flawlessly
- 7-8: Good solution with minor issues
- 5-6: Partially correct, needs refinement
- 3-4: Some understanding but significant errors
- 0-2: Incorrect or no understanding

EFFICIENCY (0-10):
- 9-10: Optimal modern approach
- 7-8: Good approach, minor optimizations possible
- 5-6: Acceptable but better alternatives exist
- 3-4: Inefficient or outdated approach
- 0-2: Very poor approach

CLARITY (0-10):
- 9-10: Excellent explanation with reasoning
- 7-8: Good explanation, mostly clear
- 5-6: Adequate explanation, some gaps
- 3-4: Poor explanation, hard to follow
- 0-2: No explanation or very unclear

Be fair, constructive, and educational in your feedback.
"""
    
    def _get_fallback_question(self, difficulty_level: str, question_number: int) -> Dict:
        """Fallback question if AI generation fails"""
        fallback_questions = {
            "intermediate": {
                "question": "You have a sales dataset with Product_ID in column A and Sales_Amount in column B. How would you calculate the total sales for Product_ID 'PROD001'?",
                "ideal_solution": "=SUMIF(A:A,\"PROD001\",B:B)",
                "explanation": "SUMIF function sums values based on criteria",
                "key_concepts": ["SUMIF", "criteria-based calculations"],
                "alternatives": ["SUMIFS", "PivotTable"]
            },
            "intermediate_advanced": {
                "question": "You need to create a dynamic range that automatically expands when new data is added. How would you accomplish this?",
                "ideal_solution": "=OFFSET($A$1,0,0,COUNTA($A:$A),1) or Excel Tables",
                "explanation": "OFFSET with COUNTA creates dynamic ranges",
                "key_concepts": ["OFFSET", "COUNTA", "dynamic ranges"],
                "alternatives": ["Excel Tables", "INDIRECT"]
            },
            "advanced": {
                "question": "You need to perform a lookup with multiple criteria. How would you find a value where Column A = 'Category1' AND Column B = 'Product1'?",
                "ideal_solution": "=INDEX(C:C,MATCH(1,(A:A=\"Category1\")*(B:B=\"Product1\"),0))",
                "explanation": "Array formula with multiple criteria matching",
                "key_concepts": ["INDEX/MATCH", "array formulas", "multiple criteria"],
                "alternatives": ["FILTER function", "Helper columns"]
            }
        }
        
        return fallback_questions.get(difficulty_level, fallback_questions["intermediate"])
    
    def _get_basic_feedback(self, user_answer: str, question: Dict) -> str:
        """Basic feedback fallback"""
        if len(user_answer.strip()) < 10:
            return "Please provide more detailed explanations of your Excel approach."
        return f"Thank you for your answer. The ideal solution would be: {question.get('ideal_solution', 'N/A')}"
    
    def _get_basic_evaluation(self, user_answer: str) -> Dict:
        """Basic evaluation fallback"""
        score = 5.0 if len(user_answer.strip()) > 20 else 3.0
        return {
            "correctness_score": score,
            "efficiency_score": score,
            "clarity_score": score,
            "overall_score": score,
            "feedback": "Thank you for your response.",
            "strengths": [],
            "areas_for_improvement": ["Provide more detailed explanations"],
            "recommendation": "Practice explaining Excel solutions step-by-step."
        }
    
    def _get_basic_report(self, overall_score: float, evaluations: List[Dict]) -> str:
        """Basic report fallback"""
        level = "Intermediate" if overall_score >= 6 else "Beginner"
        return f"""
EXCEL PROFICIENCY ASSESSMENT REPORT

Overall Score: {overall_score:.1f}/10
Proficiency Level: {level}

You completed {len(evaluations)} questions. Continue practicing Excel skills to improve your proficiency.

Recommendations:
- Practice Excel functions and formulas
- Study real-world Excel scenarios
- Focus on explaining your reasoning clearly

Keep up the good work!
"""
    
    def _format_conversation_history(self, history: List[Dict]) -> str:
        """Format conversation history for context"""
        if not history:
            return "No previous conversation."
        
        formatted = ""
        for i, item in enumerate(history[-3:], 1):  # Last 3 items
            formatted += f"Q{i}: {item.get('question', 'N/A')[:50]}...\n"
            formatted += f"A{i}: {item.get('answer', 'N/A')[:50]}...\n\n"
        
        return formatted