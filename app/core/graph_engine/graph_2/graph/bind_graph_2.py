from langgraph.graph import StateGraph

from app.core.graph_engine.graph_2.nodes.graph_2_end_node import graph_2_end_node
from app.core.graph_engine.graph_2.nodes.graph_2_node import graph_2_node


def bind_graph_2(
        graph: StateGraph
) -> None:
    graph.add_node(node="graph_2_node", action=graph_2_node)
    graph.add_node(node="graph_2_end_node", action=graph_2_end_node)

    graph.add_edge(start_key="graph_2_node", end_key="graph_2_end_node")
    graph.add_edge(start_key="graph_2_end_node", end_key="update_messages_node")
