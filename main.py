from crewai import Agent,Task,LLM,Crew
import yaml
import sqlalchemy
from sqlalchemy import text
import db_setup
from sqlalchemy import create_engine


def agent_execution(query):

   
    agent=LLM(model="ollama/llama3.2-vision:latest")
    f1,f2="",""
    with open("configcrewai/sqlagent.yaml") as f1:
        f1=yaml.safe_load(f1)

    with open("configcrewai/sqlagenttask.yaml") as f2:
        f2=yaml.safe_load(f2)

    # print(f2)
    agent1=Agent(role=f1["sqlagent"]["role"],goal=f1["sqlagent"]["goal"],backstory=f1["sqlagent"]["backstory"],llm=agent)
    task1=Task(description=f2["sqlagenttask"]["description"],expected_output=f2["sqlagenttask"]["expected_output"],agent=agent1)

    crew=Crew(agents=[agent1],tasks=[task1])
    resp=crew.kickoff(inputs={"query":query})
    return resp.raw


def execute_query(query:str,conn):

    resp=conn.execute(text(query))
    rows=resp.fetchall()
    result_strings = [", ".join(map(str, row)) for row in rows]
    return result_strings
    # return rows


def interpret_agent(query,resp):
    agent=LLM(model="ollama/llama3.2-vision:latest")
    f1,f2="",""
    with open("configcrewai/interpretagent.yaml") as f1:
        f1=yaml.safe_load(f1)

    with open("configcrewai/interpretagenttask.yaml") as f2:
        f2=yaml.safe_load(f2)

    # print(f2)
    agent1=Agent(role=f1["interpretagent"]["role"],goal=f1["interpretagent"]["goal"],backstory=f1["interpretagent"]["backstory"],llm=agent)
    task1=Task(description=f2["interpretagenttask"]["description"],expected_output=f2["interpretagenttask"]["expected_output"],agent=agent1)

    crew=Crew(agents=[agent1],tasks=[task1])
    resp=crew.kickoff(inputs={"query":query,"response":resp})
    return resp.raw



if __name__=="__main__":

    # try:
    query=input("ask query?\n")
    result=db_setup.set_connection()
    agent=agent_execution(query)
    if ";" not in agent:
        agent+=";"
    

    # query=agent
    print(agent)
    sql_resp=""
    with result.connect() as conn:
        sql_resp=execute_query(agent,conn)
    print(sql_resp)

    
    agent2=interpret_agent(query,sql_resp)
    print(agent2)
    # except Exception as e:
    #     print(f"something went wrong {str(e)}")




