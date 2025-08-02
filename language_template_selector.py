from jinja2 import Template
from langchain_aws import ChatBedrock
import boto3
from dotenv import load_dotenv 
import os 

load_dotenv()

def select_template(employee_name,employee_country,employee_role,today_date_str,start_date_str,language):
    if language.lower().strip()!='english':
        REGION_NAME = os.getenv("REGION_NAME", "us-east-1")
        AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        MODEL_NAME = os.getenv("MODEL_NAME")
        
        os.environ["AWS_REGION"] = REGION_NAME
        os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
        os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY        
        
        
        bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
        
        text_llm = ChatBedrock(
            model_id=MODEL_NAME,
            client=bedrock_client,
            model_kwargs=dict(temperature=0, top_k=0),
        )
        
        prompt_today = f"""Translate the following date from English to {language}:"
                            {today_date_str}
                            Return only the translated date. Do not include any explanation or reasoning.
                        """
        prompt_enroll = f"""Translate the following date from English to {language}:"
                            {start_date_str}
                            Return only the translated date. Do not include any explanation or reasoning.
                        """
        
        
        today_date_str = text_llm.invoke(prompt_today).content
        start_date_str = text_llm.invoke(prompt_enroll).content
    
    if language.lower().strip()=='spanish':
        with open("lang_templates/spanish_template.txt", "r") as file:
            template_str = file.read()
    elif language.lower().strip()=='english':
        with open("lang_templates/english_template.txt", "r") as file:
            template_str = file.read()
    elif language.lower().strip()=='ukrainian':
        
        with open("lang_templates/ukrainian_template.txt", "r") as file:
            template_str = file.read()
    else:
        with open("lang_templates/english_template.txt", "r") as file:
            template_str = file.read()
    
    template = Template(template_str)
    
    letter = template.render(
        employee_name=employee_name,
        employee_country=employee_country,
        employee_role=employee_role,
        start_date_str=start_date_str,
        today_date_str=today_date_str
    )
                        
    return letter