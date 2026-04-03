# src/finops_agent.py
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.config import CONFIG
from src.mock_data import BAD_PYSPARK_CODE, SPARK_EXECUTION_METRICS

class FinOpsOptimizer:
    def __init__(self, temperature=0.0):
        print("[System] Initializing FinOpsOptimizer...")
        self.llm = ChatGroq(
            groq_api_key=CONFIG["GROQ_API_KEY"],
            model_name="llama-3.1-8b-instant", 
            temperature=temperature
        )
        self.prompt = self._build_prompt()

    def _build_prompt(self) -> ChatPromptTemplate:
        system_template = """You are an Elite Databricks FinOps Architect. Your job is to rewrite inefficient PySpark code to eliminate data spills and network shuffle bottlenecks.

        STRICT CONSTRAINTS:
        1. You must use the PySpark DataFrame API. NEVER use RDDs. NEVER use Pandas.
        2. The final DataFrame schema must remain identical to the input script. Do not drop or rename columns.
        3. You must add inline comments explaining exactly WHICH optimization technique you applied and WHY, referencing the provided metrics.
        4. OUTPUT FORMAT: You must return ONLY the raw Python code wrapped in standard markdown python blocks. Do not output any conversational text.
        """

        human_template = """Please optimize the following PySpark script based on the execution metrics provided.

        SPARK EXECUTION METRICS:
        {metrics}

        UNOPTIMIZED PYSPARK CODE:
        {code}
        """

        return ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", human_template)
        ])

    def _extract_code(self, raw_llm_output: str) -> str:
        # Workaround for UI rendering bugs: build the backticks dynamically using ASCII
        ticks = chr(96) * 3  
        pattern = rf"{ticks}(?:python)?\n?(.*?)\n?{ticks}"
        
        match = re.search(pattern, raw_llm_output, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        else:
            print("[WARNING] Regex parser failed to find markdown blocks. Returning raw output.")
            return raw_llm_output.strip()

    def optimize_pipeline(self, code: str, metrics: dict) -> str:
        print("[System] Routing payload to Llama-3.1 FinOps Architect...")
        chain = self.prompt | self.llm
        response = chain.invoke({
            "metrics": str(metrics),
            "code": code
        })
        print("[System] Payload received. Parsing optimized code...")
        clean_code = self._extract_code(response.content)
        return clean_code

# --- THIS BLOCK MUST BE FLUSH LEFT ---
if __name__ == "__main__":
    agent = FinOpsOptimizer()
    
    print("\n[System] Beginning Optimization Run...")
    optimized_script = agent.optimize_pipeline(
        code=BAD_PYSPARK_CODE,
        metrics=SPARK_EXECUTION_METRICS
    )
    
    print("\n" + "="*60)
    print("🚀 OPTIMIZED PYSPARK CODE (READY FOR DATABRICKS)")
    print("="*60)
    print(optimized_script)
    print("="*60)