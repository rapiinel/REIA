from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from reia.models import ReiaOutput
from reia.tools import (
    NormalizeAddressTool,
    SearchBusinessTool,
    InferNaicsTool,
    PropertyIntelTool,
)


@CrewBase
class Reia:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def address_validator(self) -> Agent:
        return Agent(
            config=self.agents_config["address_validator"],
            tools=[NormalizeAddressTool()],
            verbose=True,
        )

    @agent
    def business_finder(self) -> Agent:
        return Agent(
            config=self.agents_config["business_finder"],
            tools=[SearchBusinessTool()],
            verbose=True,
        )

    @agent
    def naics_classifier(self) -> Agent:
        return Agent(
            config=self.agents_config["naics_classifier"],
            tools=[InferNaicsTool()],
            verbose=True,
        )

    @agent
    def property_intel_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["property_intel_analyst"],
            tools=[PropertyIntelTool()],
            verbose=True,
        )

    @agent
    def report_compiler(self) -> Agent:
        return Agent(
            config=self.agents_config["report_compiler"],
            verbose=True,
        )

    @task
    def validate_address_task(self) -> Task:
        return Task(
            config=self.tasks_config["validate_address_task"],
        )

    @task
    def find_business_task(self) -> Task:
        return Task(
            config=self.tasks_config["find_business_task"],
        )

    @task
    def classify_naics_task(self) -> Task:
        return Task(
            config=self.tasks_config["classify_naics_task"],
        )

    @task
    def property_intel_task(self) -> Task:
        return Task(
            config=self.tasks_config["property_intel_task"],
        )

    @task
    def compile_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["compile_report_task"],
            output_pydantic=ReiaOutput,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
        )