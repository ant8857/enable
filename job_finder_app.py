import streamlit as st
from enum import Enum
import tempfile
import requests 


CHATBOT_API_URL = "http://localhost:11434/api/generate"  
CHATBOT_MODEL = "RashedAlrushod/Job_Advisory"


class DisabilityType(Enum):
    PHYSICAL = "Physical"
    MENTAL = "Mental"

class PhysicalDisability(Enum):
    MOBILITY = "Mobility Issues"
    HAND_AMPUTATION = "Hand Amputation"
    FEET_AMPUTATION = "Feet Amputation"
    VISUAL_IMPAIRMENT = "Visual Impairment"

class MentalHealth(Enum):
    ANXIETY = "Anxiety"
    DEPRESSION = "Depression"
    ADHD = "ADHD"


JOB_MAP = {
    (DisabilityType.PHYSICAL, PhysicalDisability.MOBILITY): [
        {"title": "Remote Software Developer", "salary_range": "$60k-$120k"},
        {"title": "Data Entry Specialist", "salary_range": "$30k-$50k"},
        {"title": "Technical Writer", "salary_range": "$50k-$80k"},
        {"title": "Customer Support Specialist", "salary_range": "$35k-$55k"},
        {"title": "Accessibility Tester", "salary_range": "$45k-$85k"}
    ],
    (DisabilityType.PHYSICAL, PhysicalDisability.HAND_AMPUTATION): [
        {"title": "Voice Acting", "salary_range": "$40k-$150k"},
        {"title": "Audio Editing", "salary_range": "$35k-$75k"},
        {"title": "Podcast Producer", "salary_range": "$50k-$100k"},
        {"title": "Accessibility Consultant", "salary_range": "$60k-$110k"}
    ],
    (DisabilityType.PHYSICAL, PhysicalDisability.FEET_AMPUTATION): [
        {"title": "Remote Software Developer", "salary_range": "$60k-$120k"},
        {"title": "Data Entry Specialist", "salary_range": "$30k-$50k"},
        {"title": "Technical Writer", "salary_range": "$50k-$80k"},
        {"title": "Customer Support Specialist", "salary_range": "$35k-$55k"}
    ],
    (DisabilityType.PHYSICAL, PhysicalDisability.VISUAL_IMPAIRMENT): [
        {"title": "Braille Transcriber", "salary_range": "$30k-$60k"},
        {"title": "Accessibility Consultant", "salary_range": "$60k-$110k"},
        {"title": "Voice Acting", "salary_range": "$40k-$150k"}
    ],
    (DisabilityType.MENTAL, MentalHealth.ANXIETY): [
        {"title": "Freelance Writing", "salary_range": "$30k-$70k"},
        {"title": "Data Analysis", "salary_range": "$50k-$90k"},
        {"title": "Research Assistant", "salary_range": "$40k-$70k"},
        {"title": "Content Moderator", "salary_range": "$35k-$60k"},
        {"title": "Online Counseling", "salary_range": "$50k-$100k"}
    ],
    (DisabilityType.MENTAL, MentalHealth.DEPRESSION): [
        {"title": "Virtual Assistant", "salary_range": "$30k-$50k"},
        {"title": "Online Tutoring", "salary_range": "$35k-$60k"},
        {"title": "Graphic Design", "salary_range": "$40k-$80k"},
        {"title": "Social Media Management", "salary_range": "$40k-$70k"},
        {"title": "Mental Health Advocate", "salary_range": "$35k-$65k"}
    ],
}

def ai_job_suggestion(disability_type, condition):
    key = (disability_type, condition)
    return JOB_MAP.get(key, [])

def generate_linkedin_url(job_title):
    return f"https://www.linkedin.com/jobs/search/?keywords={job_title.replace(' ', '%20')}"

def chatbot_response(prompt):
    """Send a prompt to the chatbot and get its response."""
    payload = {
        'model': CHATBOT_MODEL,
        'prompt': prompt,
        'stream': False
    }
    
    try:
        response = requests.post(CHATBOT_API_URL, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result.get('response', 'Sorry, I could not process your request.')
    except requests.RequestException as e:
        return f"Error communicating with the chatbot: {e}"

def main():
    st.title("ENABLE")  
    tab1, tab2 = st.tabs(["Job Finder", "Chatbot"])

   
    with tab1:
        disability_type = st.selectbox("Type of Disability", [e.value for e in DisabilityType])
        condition = None

        if disability_type == DisabilityType.PHYSICAL.value:
            condition = st.selectbox("Specific Physical Issue", [e.value for e in PhysicalDisability])
        elif disability_type == DisabilityType.MENTAL.value:
            condition = st.selectbox("Specific Mental Health Condition", [e.value for e in MentalHealth])

        if st.button("Suggest Jobs"):
            if not disability_type or not condition:
                warning_message = (
                    f"Please select both a type of disability and a specific condition."
                )
                st.warning(warning_message)
                st.audio(text_to_speech(warning_message))
            else:
                dtype = DisabilityType(disability_type)
                selected_condition = (
                    PhysicalDisability(condition) if dtype == DisabilityType.PHYSICAL else MentalHealth(condition)
                )
                
                suggestions = ai_job_suggestion(dtype, selected_condition)
                
                if suggestions:
                    st.subheader("Job Suggestions with Salary Ranges and LinkedIn Search Links")
                   
                    
                    for job in suggestions:
                        linkedin_url = generate_linkedin_url(job["title"])
                        job_details = (
                            f"{job['title']} with a salary range of {job['salary_range']}. "
                            f"You can apply using the provided link."
                        )
                        st.markdown(f"""
                        - **{job['title']}**  
                          **Salary Range**: {job['salary_range']}  
                          [🔍 Search LinkedIn Jobs]({linkedin_url})
                        """)
                else:
                    no_job_message = (
                        f"No job suggestions available for the selected criteria."
                    )
                    st.info(no_job_message)
                    
    
    with tab2:
        st.header("Chatbot Assistance")
        
        user_input = st.text_input("Ask me anything about jobs or accessibility:")
        
        if user_input:
            response = chatbot_response(user_input)
            st.write(f"**Chatbot:** {response}")
            
            
            audio_response = text_to_speech(response)

if __name__ == "__main__":
    main()
