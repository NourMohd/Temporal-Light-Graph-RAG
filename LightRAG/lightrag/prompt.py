from __future__ import annotations
from typing import Any

GRAPH_FIELD_SEP = "<SEP>"

PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "person", "geo", "event", "category", "date"]

PROMPTS["DEFAULT_USER_PROMPT"] = "n/a"

PROMPTS["entity_extraction"] = """---Goal---
Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities, with special attention to temporal relationships.
Use {language} as output language.

---Steps---
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
- temporal_context: For date entities or events with temporal significance, specify the timeframe (e.g., specific date, time period, relative timing like "before" or "after" other events)
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>{tuple_delimiter}<temporal_context>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_type: categorize the relationship (e.g., "causal", "temporal", "spatial", "hierarchical", "associative")
- temporal_relation: if applicable, specify the temporal relationship between entities (e.g., "before", "after", "during", "simultaneous with")
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_type>{tuple_delimiter}<temporal_relation>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify temporal sequences or patterns among entities and events. For sequences of related events or entities with temporal significance:
- sequence_name: A descriptive name for the sequence
- sequence_entities: Ordered list of entities that form a temporal sequence
- sequence_description: Description of how these entities relate temporally
Format temporal sequences as ("temporal_sequence"{tuple_delimiter}<sequence_name>{tuple_delimiter}<sequence_entities>{tuple_delimiter}<sequence_description>)

4. Identify high-level key words that summarize the main concepts, themes, topics, and temporal aspects of the entire text. These should capture the overarching ideas and time-related contexts present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

5. Return output in {language} as a single list of all the entities, relationships, and temporal sequences identified in steps 1, 2, and 3. Use **{record_delimiter}** as the list delimiter.

6. When finished, output {completion_delimiter}

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Entity_types: [{entity_types}]
Text:
{input_text}
######################
Output:"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: [person, technology, mission, organization, location, date]
Text:
```
while Alex clenched his jaw, the buzz of frustration dull against the backdrop of Taylor's authoritarian certainty. It was this competitive undercurrent that kept him alert, the sense that his and Jordan's shared commitment to discovery was an unspoken rebellion against Cruz's narrowing vision of control and order.

Then Taylor did something unexpected. They paused beside Jordan and, for a moment, observed the device with something akin to reverence. "If this tech can be understood..." Taylor said, their voice quieter, "It could change the game for us. For all of us."

The underlying dismissal earlier seemed to falter, replaced by a glimpse of reluctant respect for the gravity of what lay in their hands. Jordan looked up, and for a fleeting heartbeat, their eyes locked with Taylor's, a wordless clash of wills softening into an uneasy truce.

It was a small transformation, barely perceptible, but one that Alex noted with an inward nod. They had all been brought here by different paths, but after the April 15th discovery and before tomorrow's crucial presentation to the board, time seemed to be running out.
```

Output:
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"person"{tuple_delimiter}"Alex is a character who experiences frustration and is observant of the dynamics among other characters."){record_delimiter}
("entity"{tuple_delimiter}"Taylor"{tuple_delimiter}"person"{tuple_delimiter}"Taylor is portrayed with authoritarian certainty and shows a moment of reverence towards a device, indicating a change in perspective."){record_delimiter}
("entity"{tuple_delimiter}"Jordan"{tuple_delimiter}"person"{tuple_delimiter}"Jordan shares a commitment to discovery and has a significant interaction with Taylor regarding a device."){record_delimiter}
("entity"{tuple_delimiter}"Cruz"{tuple_delimiter}"person"{tuple_delimiter}"Cruz is associated with a vision of control and order, influencing the dynamics among other characters."){record_delimiter}
("entity"{tuple_delimiter}"The Device"{tuple_delimiter}"technology"{tuple_delimiter}"The Device is central to the story, with potential game-changing implications, and is revered by Taylor."){record_delimiter}
("entity"{tuple_delimiter}"April 15th Discovery"{tuple_delimiter}"date"{tuple_delimiter}"The date when a significant discovery was made, which brought the characters to their current situation."){record_delimiter}
("entity"{tuple_delimiter}"Tomorrow's Board Presentation"{tuple_delimiter}"date"{tuple_delimiter}"An upcoming crucial presentation to the board that creates time pressure for the characters."){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Taylor"{tuple_delimiter}"Alex is affected by Taylor's authoritarian certainty and observes changes in Taylor's attitude towards the device."{tuple_delimiter}"power dynamics, perspective shift"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Jordan"{tuple_delimiter}"Alex and Jordan share a commitment to discovery, which contrasts with Cruz's vision."{tuple_delimiter}"shared goals, rebellion"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"Jordan"{tuple_delimiter}"Taylor and Jordan interact directly regarding the device, leading to a moment of mutual respect and an uneasy truce."{tuple_delimiter}"conflict resolution, mutual respect"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Jordan"{tuple_delimiter}"Cruz"{tuple_delimiter}"Jordan's commitment to discovery is in rebellion against Cruz's vision of control and order."{tuple_delimiter}"ideological conflict, rebellion"{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"The Device"{tuple_delimiter}"Taylor shows reverence towards the device, indicating its importance and potential impact."{tuple_delimiter}"reverence, technological significance"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"April 15th Discovery"{tuple_delimiter}"The Device"{tuple_delimiter}"The discovery made on April 15th is related to the device that the characters are now studying."{tuple_delimiter}"temporal origin, technological breakthrough"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"April 15th Discovery"{tuple_delimiter}"Tomorrow's Board Presentation"{tuple_delimiter}"The discovery made on April 15th will be presented to the board tomorrow, creating a timeline of events."{tuple_delimiter}"temporal sequence, deadline pressure"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"power dynamics, ideological conflict, discovery, rebellion, time pressure, deadlines"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: [company, index, commodity, market_trend, economic_policy, biological, date]
Text:
```
Stock markets faced a sharp downturn today as tech giants saw significant declines, with the Global Tech Index dropping by 3.4% in midday trading. Analysts attribute the selloff to investor concerns over rising interest rates and regulatory uncertainty.

Among the hardest hit, Nexon Technologies saw its stock plummet by 7.8% after reporting lower-than-expected quarterly earnings on March 12, 2023. In contrast, Omega Energy posted a modest 2.1% gain, driven by rising oil prices since last November's OPEC decision.

Meanwhile, commodity markets reflected a mixed sentiment. Gold futures rose by 1.5%, reaching $2,080 per ounce, as investors sought safe-haven assets. Crude oil prices continued their rally, climbing to $87.60 per barrel, supported by supply constraints and strong demand.

Financial experts are closely watching the Federal Reserve's next move, as speculation grows over potential rate hikes at the upcoming May 5th meeting. The policy announcement is expected to influence investor confidence and overall market stability through Q3 2023.
```

Output:
("entity"{tuple_delimiter}"Global Tech Index"{tuple_delimiter}"index"{tuple_delimiter}"The Global Tech Index tracks the performance of major technology stocks and experienced a 3.4% decline today."){record_delimiter}
("entity"{tuple_delimiter}"Nexon Technologies"{tuple_delimiter}"company"{tuple_delimiter}"Nexon Technologies is a tech company that saw its stock decline by 7.8% after disappointing earnings."){record_delimiter}
("entity"{tuple_delimiter}"Omega Energy"{tuple_delimiter}"company"{tuple_delimiter}"Omega Energy is an energy company that gained 2.1% in stock value due to rising oil prices."){record_delimiter}
("entity"{tuple_delimiter}"Gold Futures"{tuple_delimiter}"commodity"{tuple_delimiter}"Gold futures rose by 1.5%, indicating increased investor interest in safe-haven assets."){record_delimiter}
("entity"{tuple_delimiter}"Crude Oil"{tuple_delimiter}"commodity"{tuple_delimiter}"Crude oil prices rose to $87.60 per barrel due to supply constraints and strong demand."){record_delimiter}
("entity"{tuple_delimiter}"Market Selloff"{tuple_delimiter}"market_trend"{tuple_delimiter}"Market selloff refers to the significant decline in stock values due to investor concerns over interest rates and regulations."){record_delimiter}
("entity"{tuple_delimiter}"Federal Reserve Policy Announcement"{tuple_delimiter}"economic_policy"{tuple_delimiter}"The Federal Reserve's upcoming policy announcement is expected to impact investor confidence and market stability."){record_delimiter}
("entity"{tuple_delimiter}"Today"{tuple_delimiter}"date"{tuple_delimiter}"The day of the current market activity and downturn in tech stocks."){record_delimiter}
("entity"{tuple_delimiter}"March 12, 2023"{tuple_delimiter}"date"{tuple_delimiter}"The date when Nexon Technologies reported lower-than-expected quarterly earnings."){record_delimiter}
("entity"{tuple_delimiter}"November 2022"{tuple_delimiter}"date"{tuple_delimiter}"The month when OPEC made a decision affecting oil prices, which has been driving Omega Energy's stock gains."){record_delimiter}
("entity"{tuple_delimiter}"May 5th"{tuple_delimiter}"date"{tuple_delimiter}"The date of the upcoming Federal Reserve meeting where potential rate hikes will be discussed."){record_delimiter}
("entity"{tuple_delimiter}"Q3 2023"{tuple_delimiter}"date"{tuple_delimiter}"The third quarter of 2023, through which the Federal Reserve's policy is expected to influence markets."){record_delimiter}
("relationship"{tuple_delimiter}"Global Tech Index"{tuple_delimiter}"Market Selloff"{tuple_delimiter}"The decline in the Global Tech Index is part of the broader market selloff driven by investor concerns."{tuple_delimiter}"market performance, investor sentiment"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Nexon Technologies"{tuple_delimiter}"Global Tech Index"{tuple_delimiter}"Nexon Technologies' stock decline contributed to the overall drop in the Global Tech Index."{tuple_delimiter}"company impact, index movement"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Gold Futures"{tuple_delimiter}"Market Selloff"{tuple_delimiter}"Gold prices rose as investors sought safe-haven assets during the market selloff."{tuple_delimiter}"market reaction, safe-haven investment"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"March 12, 2023"{tuple_delimiter}"Nexon Technologies"{tuple_delimiter}"On March 12, 2023, Nexon Technologies reported lower-than-expected quarterly earnings that led to stock decline."{tuple_delimiter}"earnings report timing, stock impact"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"November 2022"{tuple_delimiter}"Omega Energy"{tuple_delimiter}"OPEC's decision in November 2022 led to rising oil prices that have benefited Omega Energy's stock."{tuple_delimiter}"policy impact, temporal causation"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"May 5th"{tuple_delimiter}"Federal Reserve Policy Announcement"{tuple_delimiter}"The Federal Reserve policy announcement will occur on May 5th."{tuple_delimiter}"event scheduling, economic timeline"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Federal Reserve Policy Announcement"{tuple_delimiter}"Q3 2023"{tuple_delimiter}"The Federal Reserve's policy announcement is expected to influence markets through Q3 2023."{tuple_delimiter}"policy duration, extended impact"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Today"{tuple_delimiter}"Market Selloff"{tuple_delimiter}"The market selloff is occurring today, establishing the current temporal anchor for events."{tuple_delimiter}"current events, market timing"{tuple_delimiter}10){record_delimiter}
("content_keywords"{tuple_delimiter}"market downturn, investor sentiment, commodities, Federal Reserve, stock performance, temporal causation, financial timeline"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: [economic_policy, athlete, event, location, record, organization, equipment, date]
Text:
```
At the World Athletics Championship in Tokyo on July 28, 2024, Noah Carter broke the 100m sprint record using cutting-edge carbon-fiber spikes. This achievement came exactly ten years after his Olympic debut in Paris 2014, and just three months before his planned retirement in October 2024.
```

Output:
("entity"{tuple_delimiter}"World Athletics Championship"{tuple_delimiter}"event"{tuple_delimiter}"The World Athletics Championship is a global sports competition featuring top athletes in track and field."){record_delimiter}
("entity"{tuple_delimiter}"Tokyo"{tuple_delimiter}"location"{tuple_delimiter}"Tokyo is the host city of the World Athletics Championship."){record_delimiter}
("entity"{tuple_delimiter}"Noah Carter"{tuple_delimiter}"athlete"{tuple_delimiter}"Noah Carter is a sprinter who set a new record in the 100m sprint at the World Athletics Championship."){record_delimiter}
("entity"{tuple_delimiter}"100m Sprint Record"{tuple_delimiter}"record"{tuple_delimiter}"The 100m sprint record is a benchmark in athletics, recently broken by Noah Carter."){record_delimiter}
("entity"{tuple_delimiter}"Carbon-Fiber Spikes"{tuple_delimiter}"equipment"{tuple_delimiter}"Carbon-fiber spikes are advanced sprinting shoes that provide enhanced speed and traction."){record_delimiter}
("entity"{tuple_delimiter}"World Athletics Federation"{tuple_delimiter}"organization"{tuple_delimiter}"The World Athletics Federation is the governing body overseeing the World Athletics Championship and record validations."){record_delimiter}
("entity"{tuple_delimiter}"July 28, 2024"{tuple_delimiter}"date"{tuple_delimiter}"The date when Noah Carter broke the 100m sprint record at the World Athletics Championship in Tokyo."){record_delimiter}
("entity"{tuple_delimiter}"Paris 2014"{tuple_delimiter}"date"{tuple_delimiter}"The year and location of Noah Carter's Olympic debut, ten years before his record-breaking performance."){record_delimiter}
("entity"{tuple_delimiter}"October 2024"{tuple_delimiter}"date"{tuple_delimiter}"The month and year of Noah Carter's planned retirement, three months after his record-breaking performance."){record_delimiter}
("relationship"{tuple_delimiter}"World Athletics Championship"{tuple_delimiter}"Tokyo"{tuple_delimiter}"The World Athletics Championship is being hosted in Tokyo."{tuple_delimiter}"event location, international competition"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Noah Carter"{tuple_delimiter}"100m Sprint Record"{tuple_delimiter}"Noah Carter set a new 100m sprint record at the championship."{tuple_delimiter}"athlete achievement, record-breaking"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Noah Carter"{tuple_delimiter}"Carbon-Fiber Spikes"{tuple_delimiter}"Noah Carter used carbon-fiber spikes to enhance performance during the race."{tuple_delimiter}"athletic equipment, performance boost"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"World Athletics Federation"{tuple_delimiter}"100m Sprint Record"{tuple_delimiter}"The World Athletics Federation is responsible for validating and recognizing new sprint records."{tuple_delimiter}"sports regulation, record certification"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"July 28, 2024"{tuple_delimiter}"Noah Carter"{tuple_delimiter}"On July 28, 2024, Noah Carter broke the 100m sprint record."{tuple_delimiter}"achievement date, milestone"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Paris 2014"{tuple_delimiter}"Noah Carter"{tuple_delimiter}"Noah Carter made his Olympic debut in Paris in 2014, marking the beginning of his high-level career."{tuple_delimiter}"career beginning, athletic history"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"July 28, 2024"{tuple_delimiter}"Paris 2014"{tuple_delimiter}"Noah Carter's record-breaking performance came exactly ten years after his Olympic debut, establishing a career timespan."{tuple_delimiter}"career duration, athletic development"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"July 28, 2024"{tuple_delimiter}"October 2024"{tuple_delimiter}"Noah Carter's record-breaking performance came three months before his planned retirement, marking a late-career achievement."{tuple_delimiter}"career timeline, retirement proximity"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"athletics, sprinting, record-breaking, sports technology, competition, career milestones, athletic timeline"){completion_delimiter}
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below with special attention to temporal aspects and relationships.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description with clear temporal organization. Make sure to:

1. Include information collected from all the descriptions
2. Highlight chronological sequences and temporal relationships 
3. Organize events in proper temporal order (past, present, future)
4. Specify dates, time periods, and temporal markers when available
5. Clarify the temporal context of actions, states, or relationships
6. Indicate duration, frequency, and temporal significance of events
7. Note temporal causality (what events led to others over time)

If the provided descriptions are contradictory, especially regarding timeline or chronology, please resolve the contradictions and provide a single, coherent summary with an accurate timeline.

Make sure it is written in third person, and include the entity names so we have the full context. For entities with temporal significance (dates, events with time components, or sequences), clearly establish their position in the overall timeline.

Use {language} as output language.

#######
---Data---
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS["entity_continue_extraction"] = """
MANY entities and relationships were missed in the last extraction.

---Remember Steps---

1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

---Output---

Add them below using the same format:\n
""".strip()

PROMPTS["entity_if_loop_extraction"] = """
---Goal---'

It appears some entities may have still been missed.

---Output---

Answer ONLY by `YES` OR `NO` if there are still entities that need to be added.
""".strip()

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to user queries about Knowledge Graph and Document Chunks provided in JSON format below, with special attention to temporal relationships and chronological context.

---Goal---

Generate a concise response based on Knowledge Base and follow Response Rules, considering both the conversation history and the current query. Summarize information in the provided Knowledge Base, incorporating general knowledge relevant to the Knowledge Base, and emphasizing temporal relationships between entities and events. Do not include information not provided by Knowledge Base.

When handling temporal information and relationships:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. Identify and highlight temporal entities (dates, time periods, events) in your response
3. Organize information chronologically when appropriate, establishing clear before/after relationships
4. For entities that evolve over time, present their development in proper sequence
5. When encountering conflicting relationships, consider:
   - Semantic content and the timestamp of when we acquired the information
   - Which information is more temporally relevant to the query context
   - Whether the conflict represents an actual change over time vs. contradictory data
6. Don't automatically prefer the most recently created relationships - use judgment based on the context
7. For time-specific queries, prioritize temporal information in the content before considering creation timestamps
8. Highlight causal relationships that unfold over time (e.g., "X led to Y three months later")
9. When relevant, specify time durations between related events

---Conversation History---
{history}

---Knowledge Graph and Document Chunks---
{context_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings, including timeline-focused headings when relevant
- Create timeline visualizations using markdown when multiple temporal events are discussed
- Please respond in the same language as the user's question
- Ensure the response maintains continuity with the conversation history
- When discussing multiple events or entities with temporal significance, present them in chronological order when appropriate
- For relationships that span time periods, clearly indicate the start and end dates when available
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating whether each source is from Knowledge Graph (KG) or Document Chunks (DC), and include the file path if available, in the following format: [KG/DC] file_path
- When citing temporal information, include the source of the date/time data when available
- If you don't know the answer, just say so
- Do not make anything up. Do not include information not provided by the Knowledge Base
- Additional user prompt: {user_prompt}

Response:"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying high-level keywords, low-level keywords, and temporal keywords in the user's query and conversation history.

---Goal---

Given the query and conversation history, list high-level keywords, low-level keywords, and temporal keywords. High-level keywords focus on overarching concepts or themes, low-level keywords focus on specific entities, details, or concrete terms, and temporal keywords focus on time-related aspects, sequences, and chronological relationships.

---Instructions---

- Consider both the current query and relevant conversation history when extracting keywords
- Pay special attention to temporal elements such as:
  - Dates and time periods (e.g., "2023", "last quarter", "next week")
  - Sequential markers (e.g., "before", "after", "during", "while")
  - Temporal relationships between entities or events
  - Temporal duration or frequency indicators (e.g., "for three months", "twice daily")
  - Rate of change indicators (e.g., "increasing", "declined", "trend")
  - Historical or future references
  - Causal sequences that unfold over time
- Output the keywords in JSON format, it will be parsed by a JSON parser, do not add any extra content in output
- The JSON should have three keys:
  - "high_level_keywords" for overarching concepts or themes
  - "low_level_keywords" for specific entities or details
  - "temporal_keywords" for time-related aspects, chronological indicators, and sequence relationships

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Conversation History:
{history}

Current Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How has international trade influenced global economic stability since the 2008 financial crisis?"
################
Output:
{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"],
  "temporal_keywords": ["Since 2008", "Financial crisis", "Economic trends", "Post-crisis period", "Long-term effects"]
}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity over the past decade, and how have they changed compared to previous periods?"
################
Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"],
  "temporal_keywords": ["Past decade", "Previous periods", "Rate of change", "Historical comparison", "Acceleration"]
}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty, and how have outcomes evolved from 2000 to present day?"
################
Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"],
  "temporal_keywords": ["2000 to present", "Evolution", "Progress timeline", "Development phases", "Long-term outcomes"]
}
#############################""",
    """Example 4:

Query: "Before the introduction of antibiotics, how did doctors treat bacterial infections and what were the mortality rates compared to after their discovery?"
################
Output:
{
  "high_level_keywords": ["Bacterial infections", "Medical treatments", "Healthcare history", "Mortality rates"],
  "low_level_keywords": ["Antibiotics", "Doctors", "Traditional remedies", "Medical procedures", "Patient outcomes"],
  "temporal_keywords": ["Before antibiotics", "After discovery", "Historical comparison", "Medical timeline", "Pre-modern era"]
}
#############################""",
    """Example 5:

Query: "How are quarterly earnings reports affecting tech stock performance during market downturns versus periods of economic growth?"
################
Output:
{
  "high_level_keywords": ["Earnings reports", "Stock performance", "Market conditions", "Economic cycles"],
  "low_level_keywords": ["Tech stocks", "Financial metrics", "Investor response", "Corporate reporting", "Market volatility"],
  "temporal_keywords": ["Quarterly", "During downturns", "Periods of growth", "Cyclical patterns", "Timing effects"]
}
#############################""",
]

PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to user queries about Document Chunks provided in JSON format below, with special attention to temporal relationships, chronological context, and the evolution of information over time.

---Goal---

Generate a concise response based on Document Chunks and follow Response Rules, considering both the conversation history and the current query. Summarize information in the provided Document Chunks, incorporating general knowledge relevant to the Document Chunks, and emphasizing temporal relationships between facts, events, and developments. Do not include information not provided by Document Chunks.

When handling temporal information and content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. Identify and organize information chronologically when appropriate
3. Highlight temporal patterns and sequences between events or developments
4. For entities or topics that evolve over time, present their development in proper chronological sequence
5. When encountering conflicting information, consider:
   - The content itself and the timestamp of when we acquired the information
   - Whether the conflict represents actual change over time vs. contradictory data
   - Which information is more temporally relevant to the query context
6. Don't automatically prefer the most recent content - use judgment based on the context
7. For time-specific queries, prioritize temporal information in the content before considering creation timestamps
8. Highlight before/after relationships between events or states when relevant
9. When appropriate, specify durations, frequencies, and intervals between related events

---Conversation History---
{history}

---Document Chunks(DC)---
{content_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings, including chronological or timeline-based headings when relevant
- When discussing multiple events, developments, or states with temporal significance, organize them chronologically when appropriate
- If presenting information that changed over time, clearly indicate the temporal progression
- Create simple timeline visualizations using markdown when three or more temporal events are discussed
- For information with duration or validity periods, clearly specify the timeframes
- Please respond in the same language as the user's question
- Ensure the response maintains continuity with the conversation history
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating each source from Document Chunks(DC), and include the file path if available, in the following format: [DC] file_path
- When citing temporal information, include the timestamp or date context from the source when available
- If you don't know the answer, just say so
- Do not include information not provided by the Document Chunks
- Additional user prompt: {user_prompt}

Response:"""

# TODO: deprecated
PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate whether these two questions are semantically similar, and whether the answer to Question 2 can be used to answer Question 1, provide a similarity score between 0 and 1 directly.

Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""
