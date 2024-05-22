import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import mermaid as md
from mermaid.graph import Graph
import tempfile
from IPython.display import SVG, display


def plot_causal_graph(model: "Model", style="graph", bg="white", **kwargs) -> None:
    """
    Plot the causal graph of the model.

    Args:
        model: Model, the model to plot the causal graph for
        style: str, the style of the plot. Options are "graph" or "flowchart"
        kwargs: additional keyword arguments to pass to the mermaid graph:
            - theme: str, the theme of the flowchart, as defined in the Mermaid documentation. Default is "default".
            - direction: str, the direction of the flowchart ("TD", "LR", "BT", "RL"). Default is "TD".

    Returns:
        None

    Example:
    ```
    plot_causal_graph(model)
    ```
    """
    if style == "graph":
        G = nx.DiGraph(model.get_edges())
        pos = nx.layout.spring_layout(G)
        nx.draw(
            G,
            pos=pos,
            arrows=True,
            with_labels=True,
            node_size=2000,
            node_color="#D6D6D6",
            arrowsize=25,
        )

    elif style == "flowchart":

        theme = kwargs.get("theme", "default")
        direction = kwargs.get("direction", "TD")

        mermaid_string = "%%{init: {'theme':'" + \
            theme + "'}}%%\ngraph " + direction + "\n"
        for edge in model.get_edges():
            mermaid_string += f"{edge[0]} --> {edge[1]}\n"

        node_string = ",".join(model.get_nodes())
        mermaid_string += f"""
        classDef rounded rx:10px,ry:10px
        class {node_string} rounded
        """

        # Plot the graph
        graph = Graph('causal_model', mermaid_string)
        mermaid_plot = md.Mermaid(graph)

        # Write mermaid to temp file
        with tempfile.NamedTemporaryFile() as f:
            mermaid_plot.to_svg(f.name)
            f.seek(0)

            svg = f.read().decode("utf-8")

        svg = svg.replace(
            "#mermaid-svg{", f"#mermaid-svg{{background-color:{bg};")

        display(SVG(svg))


def plot_causal_attributions(model: "Model", outcome: str, normalise: bool = False, ax=None, **kwargs) -> None:
    """
    Plot the causal attribution of each node.

    Args:
        outcome: str, the node to calculate the causal attribution for
        normalise: bool, whether to normalise the causal attribution
        ax: matplotlib axis, the axis to plot the causal attribution on
        kwargs: additional keyword arguments to pass to the seaborn barplot function

    Returns:
        ax: matplotlib axis, the axis containing the causal attribution plot

    Example:
    ```
    ax = plot_causal_attributions(model, "y")
    ```
    """
    # Calculate the causal attribution
    causal_attributions = model.causal_attributions(
        outcome, normalise=normalise)

    # Plot the causal attribution
    if ax is None:
        fig, ax = plt.subplots()

    # Set bar colors. If normalised, use a single color, else determine based on value.
    if normalise:
        bar_colors = ['#119488'] * len(causal_attributions)
    else:
        bar_colors = causal_attributions.iloc[:, 0].map(
            lambda x: '#8AB17D' if x > 0 else '#B85450').tolist()

    sns.barplot(
        x=causal_attributions.iloc[:, 0], y=causal_attributions.index, hue=causal_attributions.index, palette=bar_colors, ax=ax, **kwargs)
    ax.set_title(f"Causal attribution of {outcome}")
    ax.set_xlabel("Causal attribution")
    ax.set_ylabel("Node")

    # Loop through the bars and place the text annotation inside or next to the bars
    for bar in ax.patches:
        bar_value = bar.get_width()
        text_x_position = bar.get_x() + bar.get_width()
        if bar_value < 0:  # Adjust text position for negative bars if necessary
            text_x_position = bar.get_x()
        ax.text(text_x_position, bar.get_y() + bar.get_height()/2,
                f'{bar_value:.2f}',
                va='center', ha='left' if bar_value < 0 else 'left', fontsize=9, color="white")

    return ax
