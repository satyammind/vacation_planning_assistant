from crewai import LLM, Agent, Process, Task, Crew
from crewai.project import CrewBase, agent, task, crew
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

#load model config
gemini_model = os.getenv("GEMINI_MODEL")
gemini_api_key = os.getenv("GEMINI_API_KEY")

llm = LLM(
    model='gemini/gemini-1.5-flash',
    api_key=gemini_api_key
)

@CrewBase
class VacationPlanner:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    @agent
    def starting_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["starting_agent"],
            allow_delegation=False,
            llm=llm,
            verbose=True
        )

    @agent
    def destination_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["destination_agent"],
            allow_delegation=False,
            llm=llm,
            verbose=True
        )

    @agent
    def attraction_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["attraction_agent"],
            allow_delegation=False,
            llm=llm,
            verbose=True
        )

    @agent
    def itinerary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["itinerary_agent"],
            allow_delegation=False,
            llm=llm,
            verbose=True
        )

    @task
    def task_one(self) -> Task:
        return Task(
            config=self.tasks_config["task_one"],
            # agent=self.starting_agent,
        )

    @task
    def task_two(self) -> Task:
        return Task(
            config=self.tasks_config["task_two"],
        )

    @task
    def task_three(self) -> Task:
        return Task(
            config=self.tasks_config["task_three"],
        )

    @task
    def task_four(self) -> Task:
        return Task(
            config=self.tasks_config["task_four"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )



