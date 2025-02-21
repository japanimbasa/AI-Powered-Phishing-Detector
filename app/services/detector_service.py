from openai import OpenAI
import json

class PhishingDetector:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)
        
    def analyze_email(self, email_content):
        """
        Analyze email content for phishing indicators using AI
        Returns a risk score and explanation
        """
        prompt = f"""
        Analyze this email for potential phishing indicators. Consider:
        1. Urgency or pressure tactics
        2. Grammar and spelling errors
        3. Mismatched or suspicious URLs
        4. Requests for sensitive information
        5. Impersonation attempts
        
        Email content:
        {email_content}
        
        Provide analysis in JSON format with:
        - risk_score (0-100)
        - indicators (list of suspicious elements)
        - explanation (detailed analysis)
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)