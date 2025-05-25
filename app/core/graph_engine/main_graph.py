from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.core.graph_engine.graph_1.graph.bind_graph_1 import bind_graph_1
from app.core.graph_engine.graph_2.graph.bind_graph_2 import bind_graph_2
from app.core.graph_engine.structural.graph.bind_structural_graph import bind_structural_graph
from app.core.graph_engine.structural.states.state import GraphState


def mount_graph() -> StateGraph:
    current_graph: StateGraph = StateGraph(
        state_schema=GraphState
    )

    bind_structural_graph(graph=current_graph)
    bind_graph_1(graph=current_graph)
    bind_graph_2(graph=current_graph)

    return current_graph


main_graph: CompiledStateGraph = mount_graph().compile()
print(main_graph.get_graph().draw_mermaid())
