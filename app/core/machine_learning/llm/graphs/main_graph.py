from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from app.core.machine_learning.llm.nodes.basic_node import basic_node
from app.core.machine_learning.llm.states.state import GraphState

workflow: StateGraph = StateGraph(GraphState)

workflow.add_node(node="basic_node", action=basic_node)

workflow.add_edge(start_key=START, end_key="basic_node")
workflow.add_edge(start_key="basic_node", end_key=END)

graph: CompiledStateGraph = workflow.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
print(graph.get_graph().draw_mermaid())
