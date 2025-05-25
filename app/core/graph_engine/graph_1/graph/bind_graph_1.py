from langgraph.graph import StateGraph

from app.core.graph_engine.graph_1.nodes.graph_1_end_node import graph_1_end_node
from app.core.graph_engine.graph_1.nodes.graph_1_node import graph_1_node


def bind_graph_1(
        graph: StateGraph
) -> None:
    graph.add_node(node="graph_1_node", action=graph_1_node)
    graph.add_node(node="graph_1_end_node", action=graph_1_end_node)

    graph.add_edge(start_key="graph_1_node", end_key="graph_1_end_node")
    graph.add_edge(start_key="graph_1_end_node", end_key="update_messages_node")
