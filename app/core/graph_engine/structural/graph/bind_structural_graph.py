from langgraph.graph import StateGraph, START, END

from app.core.graph_engine.structural.conditionals.guardrails_conditionals import guardrails_conditionals
from app.core.graph_engine.structural.conditionals.supervisor_conditionals import supervisor_conditionals
from app.core.graph_engine.structural.nodes.guardrails_end_node import guardrails_end_node
from app.core.graph_engine.structural.nodes.guardrails_node import guardrails_node
from app.core.graph_engine.structural.nodes.memory_saver_node import memory_saver_node
from app.core.graph_engine.structural.nodes.supervisor_end_node import supervisor_end_node
from app.core.graph_engine.structural.nodes.supervisor_node import supervisor_node
from app.core.graph_engine.structural.nodes.update_messages_node import update_messages_node


def bind_structural_graph(
        graph: StateGraph
):
    graph.add_node(node="guardrails_node", action=guardrails_node)
    graph.add_node(node="guardrails_end_node", action=guardrails_end_node)
    graph.add_node(node="supervisor_node", action=supervisor_node)
    graph.add_node(node="supervisor_end_node", action=supervisor_end_node)
    graph.add_node(node="update_messages_node", action=update_messages_node)
    graph.add_node(node="memory_saver_node", action=memory_saver_node)

    graph.add_edge(start_key=START, end_key="guardrails_node")
    graph.add_conditional_edges(source="guardrails_node", path=guardrails_conditionals)
    graph.add_conditional_edges(source="supervisor_node", path=supervisor_conditionals)
    graph.add_edge(start_key="supervisor_end_node", end_key="update_messages_node")
    graph.add_edge(start_key="guardrails_end_node", end_key="update_messages_node")
    graph.add_edge(start_key="update_messages_node", end_key="memory_saver_node")
    graph.add_edge(start_key="memory_saver_node", end_key=END)
