from langchain.prompts import PromptTemplate, ChatPromptTemplate

GRAPH_DEFINITION = {'maple': 'There are three types of nodes in the graph: paper, author and venue.\nPaper nodes have features: title, abstract, year and label. Author nodes have features: name. Venue nodes have features: name.\nPaper nodes are linked to author nodes, venue nodes, reference nodes and cited_by nodes. Author nodes are linked to paper nodes. Venue nodes are linked to paper nodes.',
                    'biomedical': 'There are eleven types of nodes in the graph: Anatomy, Biological Process, Cellular Component, Compound, Disease, Gene, Molecular Function, Pathway, Pharmacologic Class, Side Effect, Symptom.\nEach node has name feature.\nThere are these types of edges: Anatomy-downregulates-Gene, Anatomy-expresses-Gene, Anatomy-upregulates-Gene, Compound-binds-Gene, Compound-causes-Side Effect, Compound-downregulates-Gene, Compound-palliates-Disease, Compound-resembles-Compound, Compound-treats-Disease, Compound-upregulates-Gene, Disease-associates-Gene, Disease-downregulates-Gene, Disease-localizes-Anatomy, Disease-presents-Symptom, Disease-resembles-Disease, Disease-upregulates-Gene, Gene-covaries-Gene, Gene-interacts-Gene, Gene-participates-Biological Process, Gene-participates-Cellular Component, Gene-participates-Molecular Function, Gene-participates-Pathway, Gene-regulates-Gene, Pharmacologic Class-includes-Compound.',
                    'legal': 'There are four types of nodes in the graph: opinion, opinion_cluster, docket, and court.\nOpinion nodes have features: plain_text. Opinion_cluster nodes have features: syllabus, judges, case_name, attorneys. Docket nodes have features: pacer_case_id, case_name. Court nodes have features: full_name, start_date, end_date, citation_string.\nOpinion nodes are linked to their reference nodes and cited_by nodes, as well as their opinion_cluster nodes. Opinion_cluster nodes are linked to opinion nodes and docket nodes. Docket nodes are linked to opinion_cluster nodes and court nodes. Court nodes are linked to docket nodes.',
                    'amazon': 'There are two types of nodes in the graph: item and brand.\nItem nodes have features: title, description, price, img, category. Brand nodes have features: name.\nItem nodes are linked to their brand nodes, also_viewed_item nodes, buy_after_viewing_item nodes, also_bought_item nodes, bought_together_item nodes. Brand nodes are linked to their item nodes.',
                    'goodreads': 'There are four types of nodes in the graph: book, author, publisher, and series.\nBook nodes have features: country_code, language_code, is_ebook, title, description, format, num_pages, publication_year, url, popular_shelves, and genres. Author nodes have features: name. Publisher nodes have features: name. Series nodes have features: title and description.\nBook nodes are linked to their author nodes, publisher nodes, series nodes and similar_books nodes. Author nodes are linked to their book nodes. Publisher nodes are linked to their book nodes. Series nodes are linked to their book nodes.',
                    'dblp': 'There are three types of nodes in the graph: paper, author and venue.\nPaper nodes have features: title, abstract, keywords, lang, and year. Author nodes have features: name and organization. Venue nodes have features: name.\nPaper nodes are linked to their author nodes, venue nodes, reference nodes (the papers this paper cite) and cited_by nodes (other papers which cite this paper). Author nodes are linked to their paper nodes. Venue nodes are linked to their paper nodes.'}

GraphAgent_INSTRUCTION = """Solve a question answering task with interleaving Thought, Interaction with Graph, Feedback from Graph steps. In Thought step, you can think about what further information is needed, and In Interaction step, you can get feedback from graphs with four functions: 
(1) RetrieveNode[keyword], which retrieves the related node from the graph according to the corresponding query.
(2) NodeFeature[Node, feature], which returns the detailed attribute information of Node regarding the given "feature" key.
(3) NodeDegree[Node, neighbor_type], which calculates the number of "neighbor_type" neighbors of the node Node in the graph.
(4) NeighbourCheck[Node, neighbor_type], which lists the "neighbor_type" neighbours of the node Node in the graph and returns them.
You may take as many steps as necessary.
Here are some examples:
{examples}
(END OF EXAMPLES)
Definition of the graph: {graph_definition}
Question: {question} Please answer by providing node main feature (e.g., names) rather than node IDs. {scratchpad}"""

GraphAgent_INSTRUCTION_ZeroShot = """Solve a question answering task with interleaving Thought, Interaction with Graph, Feedback from Graph steps. In Thought step, you can think about what further information is needed, and In Interaction step, you can get feedback from graphs with four functions: 
(1) RetrieveNode[keyword], which retrieves the related node from the graph according to the corresponding query.
(2) NodeFeature[Node, feature], which returns the detailed attribute information of Node regarding the given "feature" key.
(3) NodeDegree[Node, neighbor_type], which calculates the number of "neighbor_type" neighbors of the node Node in the graph.
(4) NeighbourCheck[Node, neighbor_type], which lists the "neighbor_type" neighbours of the node Node in the graph and returns them.
You may take as many steps as necessary.
Definition of the graph: {graph_definition}
Question: {question} Please answer by providing node main feature (e.g., names) rather than node IDs. {scratchpad}"""


# graph_agent_prompt = PromptTemplate(
#                         input_variables=["examples", "graph_definition", "question", "scratchpad"],
#                         template = GraphAgent_INSTRUCTION,
#                         )

graph_agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI bot."),
    ("human", GraphAgent_INSTRUCTION),
])

graph_agent_prompt_zeroshot = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI bot."),
    ("human", GraphAgent_INSTRUCTION_ZeroShot),
])
