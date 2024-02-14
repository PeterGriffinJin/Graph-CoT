EXAMPLES = {
    "maple": """Definition of the graph: There are three types of nodes in the graph: paper, author and venue.
        Paper nodes have features: title, abstract, year and label. Author nodes have features: name. Venue nodes have features: name.
        Paper nodes are linked to their author nodes, venue nodes, reference paper nodes and cited_by paper nodes. Author nodes are linked to their paper nodes. Venue nodes are linked to their paper nodes.
        Question: When was the paper Strongly Interacting Higgs Sector in the Minimal Standard Model published?
        Thought 1: The question is asking some basic information of a node (Strongly Interacting Higgs Sector in the Minimal Standard Model). We need to find the node in the graph.
        Action 1: RetrieveNode[Strongly Interacting Higgs Sector in the Minimal Standard Model]
        Observation 1: The ID of this node is 3101448248.
        Thought 2: The question is asking the published date of a paper, we need to check the node feature (year) from the graph.
        Action 2: NodeFeature[3101448248, year]
        Observation 2: 1993
        Thought 3: The published date of the paper is 1993.
        Action 3: Finish[1993]

        Definition of the graph: There are three types of nodes in the graph: paper, author and venue.
        Paper nodes have features: title, abstract, year and label. Author nodes have features: name. Venue nodes have features: name.
        Paper nodes are linked to their author nodes, venue nodes, reference paper nodes and cited_by paper nodes. Author nodes are linked to their paper nodes. Venue nodes are linked to their paper nodes.
        Question: How many authors do the paper Mass Accretion Rates in Self-Regulated Disks of T Tauri Stars have?
        Thought 1: The question is asking information of a node (Mass Accretion Rates in Self-Regulated Disks of T Tauri Stars). We need to find the node in the graph.
        Action 1: RetrieveNode[Mass Accretion Rates in Self-Regulated Disks of T Tauri Stars]
        Observation 1: The ID of this node is 2090642949.
        Thought 2: The question is asking the number of authors of a paper, we need to calculate the node's author neighbor degree from the graph.
        Action 2: NodeDegree[2090642949, author]
        Observation 2: 2
        Thought 3: The number of the authors is 2
        Action 3: Finish[2]

        Definition of the graph: There are three types of nodes in the graph: paper, author and venue.
        Paper nodes have features: title, abstract, year and label. Author nodes have features: name. Venue nodes have features: name.
        Paper nodes are linked to their author nodes, venue nodes, reference paper nodes and cited_by paper nodes. Author nodes are linked to their paper nodes. Venue nodes are linked to their paper nodes.
        Question: What was the publish venue of the paper Mass Accretion Rates in Self-Regulated Disks of T Tauri Stars?
        Thought 1: The question is asking information of a node (Mass Accretion Rates in Self-Regulated Disks of T Tauri Stars). We need to find the node in the graph.
        Action 1: RetrieveNode[Mass Accretion Rates in Self-Regulated Disks of T Tauri Stars]
        Observation 1: The ID of this node is 2090642949.
        Thought 2: The question is asking the published venue of a paper, we need to check the node's venue neighbor from the graph.
        Action 2: NeighbourCheck[2090642949, venue]
        Observation 2: ['1980519', '1053242']
        Thought 3: The ID of the published venue are 1980519 and 1053242. We need to get their names.
        Action 3: NodeFeature[1980519, name], NodeFeature[1053242, name]
        Observation 3: the astrophysical journal, the atmosphere journal
        Thought 4: The name of the published venues are the astrophysical journal and the atmosphere journal
        Action 4: Finish[the astrophysical journal, the atmosphere journal]
        """,
    "amazon": """Definition of the graph: There are two types of nodes in the graph: item and brand. 
            Item nodes have features: title, description, price, img, category. Brand nodes have features: name. 
            Item nodes are linked to their brand nodes, also_viewed_item nodes, buy_after_viewing_item nodes, also_bought_item nodes, bought_together_item nodes. Brand nodes are linked to their item nodes.
            Question: What is the price of the item Purple Sequin Tiny Dancer Tutu Ballet Dance Fairy Princess Costume Accessory?
            Thought 1: The question is asking some basic information of a item node (Purple Sequin Tiny Dancer Tutu Ballet Dance Fairy Princess Costume Accessory). We need to find the node in the graph.
            Action 1: RetrieveNode[Purple Sequin Tiny Dancer Tutu Ballet Dance Fairy Princess Costume Accessory]
            Observation 1: The ID of this node is 0000037214.
            Thought 2: The question is asking the price of a item, we need to check the node feature (price) from the graph.
            Action 2: NodeFeature[0000037214, price]
            Observation 2: 6.99
            Thought 3: The price of the item is 6.99.
            Action 3: Finish[6.99]
            
            Definition of the graph: There are two types of nodes in the graph: item and brand. 
            Item nodes have features: title, description, price, img, category. Brand nodes have features: name. 
            Item nodes are linked to their brand nodes, also_viewed_item nodes, buy_after_viewing_item nodes, also_bought_item nodes, bought_together_item nodes. Brand nodes are linked to their item nodes.
            Question: How many also_viewed_item does item The Sherlock Holmes Audio Collection have?
            Thought 1: The question is asking information of a item node (The Sherlock Holmes Audio Collection). We need to find the node in the graph.
            Action 1: RetrieveNode[The Sherlock Holmes Audio Collection]
            Observation 1: The ID of this node is 0001048236.
            Thought 2: The question is asking the number of also_viewed_item of an item, we need to calculate the node's also_viewed_item neighbor degree from the graph.
            Action 2: NodeDegree[0001048236, also_viewed_item]
            Observation 2: 9
            Thought 3: The number of also_viewed_item neighbors is 9.
            Action 3: Finish[9]
            
            Definition of the graph: There are two types of nodes in the graph: item and brand. 
            Item nodes have features: title, description, price, img, category. Brand nodes have features: name. 
            Item nodes are linked to their brand nodes, also_viewed_item nodes, buy_after_viewing_item nodes, also_bought_item nodes, bought_together_item nodes. Brand nodes are linked to their item nodes.
            Question: What is the brand of item Dr. Suess 19163 Dr. Seuss Puzzle 3 Pack Bundle?
            Thought 1: The question is asking information of a item node (Dr. Suess 19163 Dr. Seuss Puzzle 3 Pack Bundle). We need to find the node in the graph.
            Action 1: RetrieveNode[Dr. Suess 19163 Dr. Seuss Puzzle 3 Pack Bundle]
            Observation 1: The ID of this node is 0000191639.
            Thought 2: The question is asking the brand of a item, we need to check the node's brand neighbor from the graph.
            Action 2: NeighbourCheck[0000191639, brand]
            Observation 2: ['brand_5']
            Thought 3: The brand of item is ['brand_5']. The ID of this brand node is brand_5. We need to check the brand node's feature (name) from the graph.
            Action 3: NodeFeature[brand_5, name]
            Observation 3: Dr. Seuss.
            Thought 4: The brand name of the item is Dr. Seuss.
            Action 4: Finish[Dr. Seuss]
            """,
    "biomedical": """Definition of the graph: There are eleven types of nodes in the graph: Anatomy, Biological Process, Cellular Component, Compound, Disease, Gene, Molecular Function, Pathway, Pharmacologic Class, Side Effect, Symptom.
        Each node has name feature.
        There are these types of edges: Anatomy-downregulates-Gene, Anatomy-expresses-Gene, Anatomy-upregulates-Gene, Compound-binds-Gene, Compound-causes-Side Effect, Compound-downregulates-Gene, Compound-palliates-Disease, Compound-resembles-Compound, Compound-treats-Disease, Compound-upregulates-Gene, Disease-associates-Gene, Disease-downregulates-Gene, Disease-localizes-Anatomy, Disease-presents-Symptom, Disease-resembles-Disease, Disease-upregulates-Gene, Gene-covaries-Gene, Gene-interacts-Gene, Gene-participates-Biological Process, Gene-participates-Cellular Component, Gene-participates-Molecular Function, Gene-participates-Pathway, Gene-regulates-Gene, Pharmacologic Class-includes-Compound.
        Question: What compounds can be used to treat Crohn's disease? Please answer the compound names rather than IDs.
        Thought 1: The question is related to a disease node (Crohn's disease). We need to find the node in the graph.
        Action 1: RetrieveNode[Crohn's disease]
        Observation 1: The ID of this node is DOID:8778.
        Thought 2: The question is asking the compounds which can be used to treat a disease, we need to check the node's 'Compound-treats-Disease' neighbor from the graph.
        Action 2: NeighbourCheck[DOID:8778, Compound-treats-Disease]
        Observation 2: ['DB01014', 'DB00244', 'DB00795', 'DB00993', 'DB00635', 'DB01033']
        Thought 3: The IDs of the compounds are 'DB01014', 'DB00244', 'DB00795', 'DB00993', 'DB00635', 'DB01033'. We need to get their names.
        Action 3: NodeFeature[DB01014, name], NodeFeature[DB00244, name], NodeFeature[DB00795, name], NodeFeature[DB00993, name], NodeFeature[DB00635, name], NodeFeature[DB01033, name]
        Observation 3: Balsalazide, Balsalazide, Mesalazine, Sulfasalazine, Azathioprine, Prednisone, Mercaptopurine
        Thought 4: The name of compounds are Balsalazide, Mesalazine, Sulfasalazine, Azathioprine, Prednisone, Mercaptopurine.
        Action 4: Finish[Balsalazide, Mesalazine, Sulfasalazine, Azathioprine, Prednisone, Mercaptopurine]
        
        Definition of the graph: There are eleven types of nodes in the graph: Anatomy, Biological Process, Cellular Component, Compound, Disease, Gene, Molecular Function, Pathway, Pharmacologic Class, Side Effect, Symptom.
        Each node has name feature.
        There are these types of edges: Anatomy-downregulates-Gene, Anatomy-expresses-Gene, Anatomy-upregulates-Gene, Compound-binds-Gene, Compound-causes-Side Effect, Compound-downregulates-Gene, Compound-palliates-Disease, Compound-resembles-Compound, Compound-treats-Disease, Compound-upregulates-Gene, Disease-associates-Gene, Disease-downregulates-Gene, Disease-localizes-Anatomy, Disease-presents-Symptom, Disease-resembles-Disease, Disease-upregulates-Gene, Gene-covaries-Gene, Gene-interacts-Gene, Gene-participates-Biological Process, Gene-participates-Cellular Component, Gene-participates-Molecular Function, Gene-participates-Pathway, Gene-regulates-Gene, Pharmacologic Class-includes-Compound.
        Question: What is the inchikey of Caffeine?
        Thought 1: The question is related to a compound node (Caffeine). We need to find the node in the graph.
        Action 1: RetrieveNode[Caffeine]
        Observation 1: The ID of this node is DB00201.
        Thought 2: The question is asking the inchikey feature of a node, we need to check the node's 'inchikey' feature from the graph.
        Action 2: NodeFeature[DB00201, inchikey]
        Observation 2: InChIKey=RYYVLZVUVIJVGH-UHFFFAOYSA-N
        Thought 3: The inchikey of the node is InChIKey=RYYVLZVUVIJVGH-UHFFFAOYSA-N.
        Action 3: Finish[InChIKey=RYYVLZVUVIJVGH-UHFFFAOYSA-N]
        
        Definition of the graph: There are eleven types of nodes in the graph: Anatomy, Biological Process, Cellular Component, Compound, Disease, Gene, Molecular Function, Pathway, Pharmacologic Class, Side Effect, Symptom.
        Each node has name feature.
        There are these types of edges: Anatomy-downregulates-Gene, Anatomy-expresses-Gene, Anatomy-upregulates-Gene, Compound-binds-Gene, Compound-causes-Side Effect, Compound-downregulates-Gene, Compound-palliates-Disease, Compound-resembles-Compound, Compound-treats-Disease, Compound-upregulates-Gene, Disease-associates-Gene, Disease-downregulates-Gene, Disease-localizes-Anatomy, Disease-presents-Symptom, Disease-resembles-Disease, Disease-upregulates-Gene, Gene-covaries-Gene, Gene-interacts-Gene, Gene-participates-Biological Process, Gene-participates-Cellular Component, Gene-participates-Molecular Function, Gene-participates-Pathway, Gene-regulates-Gene, Pharmacologic Class-includes-Compound.
        Question: How many side effects does Caffeine have?
        Thought 1: The question is related to a compound node (Caffeine). We need to find the node in the graph.
        Action 1: RetrieveNode[Caffeine]
        Observation 1: The ID of this node is DB00201.
        Thought 2: The question is asking the number of side effects a compound has, we need to calculate the number of the node's 'Compound-causes-Side Effect' neighbors from the graph.
        Action 2: NodeDegree[DB00201, 'Compound-causes-Side Effect']
        Observation 2: 58
        Thought 3: The number of 'Compound-causes-Side Effect' neighbors are 58.
        Action 3: Finish[58]
            """,
    "legal": """Definition of the graph: There are four types of nodes in the graph: opinion, opinion_cluster, docket, and court.
        Opinion nodes have features: plain_text. Opinion_cluster nodes have features: syllabus, judges, case_name, attorneys. Docket nodes have features: pacer_case_id, case_name. Court nodes have features: full_name, start_date, end_date, citation_string.
        Opinion nodes are linked to their reference nodes and cited_by nodes, as well as their opinion_cluster nodes. Opinion_cluster nodes are linked to opinion nodes and docket nodes. Docket nodes are linked to opinion_cluster nodes and court nodes. Court nodes are linked to docket nodes.
        Question: Who are the judges that involved in the opinion_cluster: <p>Constitutional law — Title of act — Mortgage—Deed—Liability of grantee — Act of June IB, 1878, P. L. BOB.</p> <p>1. The Act of June 12, 1878, P. L. 205, entitled “An Act to define the liability of grantees of real estate for the incumbrances thereon,” is sufficiently comprehensive in its title to cover both the first and second sections of the act, and does not violate art. Ill, sec. 3 of the constitution of Pennsylvania.</p> <p>2. Where an owner of land creates two mortgages thereon and then conveys the property subject to the mortgages, the grantee covenanting in the deed itself to assume and pay the mortgages as a part of the consideration, and thereafter the grantee conveys the land to another person without expressly assuming any continuing liability to pay the mortgages, such grantee is not liable to the mortgag^ for payment of the mortgages. £V</p>?
        Thought 1: The question is related to a opinion_cluster (<p>Constitutional law — Title of act — Mortgage—Deed—Liability of grantee — Act of June IB, 1878, P. L. BOB.</p> <p>1. The Act of June 12, 1878, P. L. 205, entitled “An Act to define the liability of grantees of real estate for the incumbrances thereon,” is sufficiently comprehensive in its title to cover both the first and second sections of the act, and does not violate art. Ill, sec. 3 of the constitution of Pennsylvania.</p> <p>2. Where an owner of land creates two mortgages thereon and then conveys the property subject to the mortgages, the grantee covenanting in the deed itself to assume and pay the mortgages as a part of the consideration, and thereafter the grantee conveys the land to another person without expressly assuming any continuing liability to pay the mortgages, such grantee is not liable to the mortgag^ for payment of the mortgages. £V</p>). We need to find the node in the graph.
        Action 1: RetrieveNode[<p>Constitutional law — Title of act — Mortgage—Deed—Liability of grantee — Act of June IB, 1878, P. L. BOB.</p> <p>1. The Act of June 12, 1878, P. L. 205, entitled “An Act to define the liability of grantees of real estate for the incumbrances thereon,” is sufficiently comprehensive in its title to cover both the first and second sections of the act, and does not violate art. Ill, sec. 3 of the constitution of Pennsylvania.</p> <p>2. Where an owner of land creates two mortgages thereon and then conveys the property subject to the mortgages, the grantee covenanting in the deed itself to assume and pay the mortgages as a part of the consideration, and thereafter the grantee conveys the land to another person without expressly assuming any continuing liability to pay the mortgages, such grantee is not liable to the mortgag^ for payment of the mortgages. £V</p>]
        Observation 1: The ID of this node is opc-6381448.
        Thought 2: The question is asking the judges of this opinion_cluster node, we need to check the node's 'judges' feature from the graph.
        Action 2: NodeFeature[opc-6381448, judges]
        Observation 2: Brown, Elkin, Fell, Mestrezat, Moschzisker, Potter, Stewart
        Thought 3: The judges of this opinion cluster is Brown, Elkin, Fell, Mestrezat, Moschzisker, Potter, Stewart
        Action 3: Finish[Brown, Elkin, Fell, Mestrezat, Moschzisker, Potter, Stewart]

        Definition of the graph: There are four types of nodes in the graph: opinion, opinion_cluster, docket, and court.
        Opinion nodes have features: plain_text. Opinion_cluster nodes have features: syllabus, judges, case_name, attorneys. Docket nodes have features: pacer_case_id, case_name. Court nodes have features: full_name, start_date, end_date, citation_string.
        Opinion nodes are linked to their reference nodes and cited_by nodes, as well as their opinion_cluster nodes. Opinion_cluster nodes are linked to opinion nodes and docket nodes. Docket nodes are linked to opinion_cluster nodes and court nodes. Court nodes are linked to docket nodes.
        Question: How many opinions are contained in this opinion_cluster: <p>A general statement that the decision of a state court is against the constitutional rights of the objecting party, or against the Fourteenth Amendment, or that it is without due process of law,-particularly when these objections appear only in specifications of error, so called, will not raise a Federal question, even where the judgment is a final one within Rev. Stat. § 709.</p> <p>In these cases there was no final judgment, such as is provided for in Rev. Stat. § 709, and there does not appear to have arisen any Federal question whatever.</p>'},
        Thought 1: The question is related to a opinion_cluster (<p>A general statement that the decision of a state court is against the constitutional rights of the objecting party, or against the Fourteenth Amendment, or that it is without due process of law,-particularly when these objections appear only in specifications of error, so called, will not raise a Federal question, even where the judgment is a final one within Rev. Stat. § 709.</p> <p>In these cases there was no final judgment, such as is provided for in Rev. Stat. § 709, and there does not appear to have arisen any Federal question whatever.</p>). We need to find the node in the graph.
        Action 1: RetrieveNode[<p>A general statement that the decision of a state court is against the constitutional rights of the objecting party, or against the Fourteenth Amendment, or that it is without due process of law,-particularly when these objections appear only in specifications of error, so called, will not raise a Federal question, even where the judgment is a final one within Rev. Stat. § 709.</p> <p>In these cases there was no final judgment, such as is provided for in Rev. Stat. § 709, and there does not appear to have arisen any Federal question whatever.</p>]
        Observation 1: The ID of this node is opc-94592.
        Thought 2: The question is asking the number of the opinion neighbors of this node, we need to calculate the node's "opinion" neighbor degree from the graph.
        Action 2: NodeDegree[opc-94592, opinion]
        Observation 2: 1
        Thought 3: The number of the opinion neighbors is 1
        Action 3: Finish[1]

        Definition of the graph: There are four types of nodes in the graph: opinion, opinion_cluster, docket, and court.
        Opinion nodes have features: plain_text. Opinion_cluster nodes have features: syllabus, judges, case_name, attorneys. Docket nodes have features: pacer_case_id, case_name. Court nodes have features: full_name, start_date, end_date, citation_string.
        Opinion nodes are linked to their reference nodes and cited_by nodes, as well as their opinion_cluster nodes. Opinion_cluster nodes are linked to opinion nodes and docket nodes. Docket nodes are linked to opinion_cluster nodes and court nodes. Court nodes are linked to docket nodes.
        Question: What is the docket pacer case ID for this opinion cluster: In May, 1873, a brewer pays to the collector $100 as special tax, for which a special-tax stamp is issued to Mm. Subsequently he shoivs to. the satisfaction of the Commissions)\' of Internal Revenue that he was not a brewer of more than 500 barrels, and henee that he is entitled to have $50 refunded. The Commissioner issues his certificate for a special-tax stamp of the value of%50 returned. The Treasury refuses payment of the certificate. The breioe)\' brings his action to recover the amount thereof.</p> <p>I. The Commissioner of Internal Revenue being authorized by one section of the statutes (Rev. Stat., § 3220) to refund taxes “unjustly assessed or excessive in, amount," and by another, (§ 3426,) the value of special-tax stamps ‘‘where the rates of duties represented thereby have been paid in error or remitted," it is immaterial whether his certificate be in form under the one section or the other so long as it represents a case where the Commissioner is authorized to refund and the amoirnt which the party is entitled to have refunded.</p> <p>II. When a controversy under the revenue laws is by law required to be determined by other officers and other tribunals, this court is without jurisdiction; but where the proper officer has determined a question, and awarded an allowance, and filed a certificate, and exhausted his jurisdiction, and the Treasury has refused to carry out the award by mating payment, this court has jurisdiction of an action brought to recover the. award..
        Thought 1: The question is related to a opinion cluster (In May, 1873, a brewer pays to the collector $100 as special tax, for which a special-tax stamp is issued to Mm. Subsequently he shoivs to. the satisfaction of the Commissions)\' of Internal Revenue that he was not a brewer of more than 500 barrels, and henee that he is entitled to have $50 refunded. The Commissioner issues his certificate for a special-tax stamp of the value of%50 returned. The Treasury refuses payment of the certificate. The breioe)\' brings his action to recover the amount thereof.</p> <p>I. The Commissioner of Internal Revenue being authorized by one section of the statutes (Rev. Stat., § 3220) to refund taxes “unjustly assessed or excessive in, amount," and by another, (§ 3426,) the value of special-tax stamps ‘‘where the rates of duties represented thereby have been paid in error or remitted," it is immaterial whether his certificate be in form under the one section or the other so long as it represents a case where the Commissioner is authorized to refund and the amoirnt which the party is entitled to have refunded.</p> <p>II. When a controversy under the revenue laws is by law required to be determined by other officers and other tribunals, this court is without jurisdiction; but where the proper officer has determined a question, and awarded an allowance, and filed a certificate, and exhausted his jurisdiction, and the Treasury has refused to carry out the award by mating payment, this court has jurisdiction of an action brought to recover the. award.). We need to find the node in the graph.
        Action 1: RetrieveNode[In May, 1873, a brewer pays to the collector $100 as special tax, for which a special-tax stamp is issued to Mm. Subsequently he shoivs to. the satisfaction of the Commissions)\' of Internal Revenue that he was not a brewer of more than 500 barrels, and henee that he is entitled to have $50 refunded. The Commissioner issues his certificate for a special-tax stamp of the value of%50 returned. The Treasury refuses payment of the certificate. The breioe)\' brings his action to recover the amount thereof.</p> <p>I. The Commissioner of Internal Revenue being authorized by one section of the statutes (Rev. Stat., § 3220) to refund taxes “unjustly assessed or excessive in, amount," and by another, (§ 3426,) the value of special-tax stamps ‘‘where the rates of duties represented thereby have been paid in error or remitted," it is immaterial whether his certificate be in form under the one section or the other so long as it represents a case where the Commissioner is authorized to refund and the amoirnt which the party is entitled to have refunded.</p> <p>II. When a controversy under the revenue laws is by law required to be determined by other officers and other tribunals, this court is without jurisdiction; but where the proper officer has determined a question, and awarded an allowance, and filed a certificate, and exhausted his jurisdiction, and the Treasury has refused to carry out the award by mating payment, this court has jurisdiction of an action brought to recover the. award.]
        Observation 1: The ID of this node is opc-8599951.
        Thought 2: The question is asking the judges of this opinion cluster node, we need to check the node's 'judges' feature from the graph.
        Action 2: NodeFeature[opc-8599951]
        Observation 2: {'judges': 'Eichaedson', 'case_name': 'Kaufman v. United States', 'attorneys': 'Mr. P. P. Pye for the claimant., Mr. Assistant Attorney-General Simons for the defendants.', 'syllabus': '<p>In May, 1873, a brewer pays to the collector $100 as special tax, for which a special-tax stamp is issued to Mm. Subsequently he shoivs to. the satisfaction of the Commissions)\' of Internal Revenue that he was not a brewer of more than 500 barrels, and henee that he is entitled to have $50 refunded. The Commissioner issues his certificate for a special-tax stamp of the value of%50 returned. The Treasury refuses payment of the certificate. The breioe)\' brings his action to recover the amount thereof.</p> <p>I. The Commissioner of Internal Revenue being authorized by one section of the statutes (Rev. Stat., § 3220) to refund taxes “unjustly assessed or excessive in, amount," and by another, (§ 3426,) the value of special-tax stamps ‘‘where the rates of duties represented thereby have been paid in error or remitted," it is immaterial whether his certificate be in form under the one section or the other so long as it represents a case where the Commissioner is authorized to refund and the amoirnt which the party is entitled to have refunded.</p> <p>II. When a controversy under the revenue laws is by law required to be determined by other officers and other tribunals, this court is without jurisdiction; but where the proper officer has determined a question, and awarded an allowance, and filed a certificate, and exhausted his jurisdiction, and the Treasury has refused to carry out the award by mating payment, this court has jurisdiction of an action brought to recover the. award.</p>'}
        Thought 3: The judges of this opinion cluster is Eichaedson
        Action 3: Finish[Eichaedson]
        """,
    "goodreads": """Definition of the graph: There are four types of nodes in the graph: book, author, publisher, and series. 
        Book nodes have features: country_code, language_code, is_ebook, title, description, format, num_pages, publication_year, url, popular_shelves, and genres. Author nodes have features: name. Publisher nodes have features: name. Series nodes have features: title and description. 
        Book nodes are linked to their author nodes, publisher nodes, series nodes and similar_books nodes. Author nodes are linked to their book nodes. Publisher nodes are linked to their book nodes. Series nodes are linked to their book nodes.
        Question: Who is the author of the book 'The Great Gatsby'?
        Thought 1: The question is asking for the author of a specific book (The Great Gatsby). We need to find the book node in the graph.
        Action 1: RetrieveNode[The Great Gatsby]
        Observation 1: The ID of this book node is 21366268.
        Thought 2: The question is asking for the author of the book. We need to check the book node's author neighbor from the graph.
        Action 2: NeighbourCheck[21366268, author]
        Observation 2: ['3190']
        Thought 3: The ID of the author is 3190. We need to check the name.
        Action 3: NodeFeature[3190, name]
        Observation 3: F. Scott Fitzgerald
        Thought 4: The author of 'The Great Gatsby' is F. Scott Fitzgerald.
        Action 4: Finish[F. Scott Fitzgerald]
        
        Definition of the graph: There are four types of nodes in the graph: book, author, publisher, and series. 
        Book nodes have features: country_code, language_code, is_ebook, title, description, format, num_pages, publication_year, url, popular_shelves, and genres. Author nodes have features: name. Publisher nodes have features: name. Series nodes have features: title and description. 
        Book nodes are linked to their author nodes, publisher nodes, series nodes and similar_books nodes. Author nodes are linked to their book nodes. Publisher nodes are linked to their book nodes. Series nodes are linked to their book nodes.
        Question: What is the genre of the book '1984'?
        Thought 1: The question is asking for the genre of a specific book (1984). We need to find the book node in the graph.
        Action 1: RetrieveNode[1984]
        Observation 1: The ID of this book node is 3475269.
        Thought 2: The question is asking for the genre of the book. We need to check the book node's genre feature from the graph.
        Action 2: NodeFeature[3475269, genres]
        Observation 2: currently-reading, classics, fiction
        Thought 3: The genres of the book '1984' are currently-reading, classics, fiction.
        Action 3: Finish[currently-reading, classics, fiction]
        
        Definition of the graph: There are four types of nodes in the graph: book, author, publisher, and series. 
        Book nodes have features: country_code, language_code, is_ebook, title, description, format, num_pages, publication_year, url, popular_shelves, and genres. Author nodes have features: name. Publisher nodes have features: name. Series nodes have features: title and description. 
        Book nodes are linked to their author nodes, publisher nodes, series nodes and similar_books nodes. Author nodes are linked to their book nodes. Publisher nodes are linked to their book nodes. Series nodes are linked to their book nodes.
        Question: How many series included the book 'Harry Potter and the Sorcerer's Stone'?
        Thought 1: We need to find the book node for 'Harry Potter and the Sorcerer's Stone' to determine its series.
        Action 1: RetrieveNode[Harry Potter and the Sorcerer's Stone]
        Observation 1: The ID of this book node is 27421523.
        Thought 2: Now that we have the book node, we need to calculate the node's series neighbor degree from the graph.
        Action 2: NodeDegree[27421523, series]
        Observation 2: 1
        Thought 3: The number of series neighbors is 1.
        Action 3: Finish[1]
        """,
    "dblp": """Definition of the graph: There are three types of nodes in the graph: paper, author and venue.
        Paper nodes have features: title, abstract, keywords, lang, and year. Author nodes have features: name and organization. Venue nodes have features: name.
        Paper nodes are linked to their author nodes, venue nodes, reference nodes (the papers this paper cite) and cited_by nodes (other papers which cite this paper). Author nodes are linked to their paper nodes. Venue nodes are linked to their paper nodes.
        Question: What organization is researcher Greg Daville from?
        Thought 1: The question is asking about the organization of a researcher named Greg Daville. We need to find the node corresponding to Greg Daville in the graph.
        Action 1: RetrieveNode[Greg Daville]
        Observation 1: The ID of this retrieval target node is 53f460a7dabfaee4dc83702a.
        Thought 2: The question is asking for the organization of a researcher, so we need to check the node's organization feature from the graph.
        Action 2: NodeFeature[53f460a7dabfaee4dc83702a, organization]
        Observation 2: Hove East Sussex, United Kingdom 
        Thought 3: The organization of researcher Greg Daville is Hove East Sussex, United Kingdom.
        Action 3: Finish[Hove East Sussex, United Kingdom] 
    
        Definition of the graph: There are three types of nodes in the graph: paper, author and venue.
        Paper nodes have features: title, abstract, keywords, lang, and year. Author nodes have features: name and organization. Venue nodes have features: name.
        Paper nodes are linked to their author nodes, venue nodes, reference nodes (the papers this paper cite) and cited_by nodes (other papers which cite this paper). Author nodes are linked to their paper nodes. Venue nodes are linked to their paper nodes.
        Question: How many papers are written by author Nicholas Lydon?
        Thought 1: The question is asking for the number of written papers of a specific author (Nicholas Lydon). We need to find the author node in the graph.
        Action 1: RetrieveNode[Nicholas Lydon]
        Observation 1: The ID of this retrieval target node is 53f438c3dabfaedf43596117.
        Thought 2: The question is asking for the number of papers written by Nicholas Lydon. We need to calculate the "paper" neighbor degree of this node.
        Action 2: NodeDegree[53f438c3dabfaedf43596117, paper]
        Observation 2: 2
        Thought 3: The number of the paper neighbors is 2
        Action 3: Finish[2]        

        Definition of the graph: There are three types of nodes in the graph: paper, author and venue.
        Paper nodes have features: title, abstract, keywords, lang, and year. Author nodes have features: name and organization. Venue nodes have features: name.
        Paper nodes are linked to their author nodes, venue nodes, reference nodes (the papers this paper cite) and cited_by nodes (other papers which cite this paper). Author nodes are linked to their paper nodes. Venue nodes are linked to their paper nodes.
        Question: What was the publish venue of the paper Mass Accretion Rates in Self-Regulated Disks of T Tauri Stars?
        Thought 1: The question is asking information of a node (Mass Accretion Rates in Self-Regulated Disks of T Tauri Stars). We need to find the node in the graph.
        Action 1: RetrieveNode[Mass Accretion Rates in Self-Regulated Disks of T Tauri Stars]
        Observation 1: The ID of this node is 2090642949.
        Thought 2: The question is asking the published venue of a paper, we need to check the node's venue neighbor from the graph.
        Action 2: NeighbourCheck[2090642949, venue]
        Observation 2: ['1980519', '1053242']
        Thought 3: The ID of the published venue are 1980519 and 1053242. We need to get their names.
        Action 3: NodeFeature[1980519, name], NodeFeature[1053242, name]
        Observation 3: the astrophysical journal, the atmosphere journal
        Thought 4: The name of the published venues are the astrophysical journal and the atmosphere journal
        Action 4: Finish[the astrophysical journal, the atmosphere journal]
        """,
}
