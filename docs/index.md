# Query Engines

This document outlines the different types of query engines supported in our system and how they work.

## 1. Router Query Engine

The Router Query Engine is the engine that routes queries to specialized sub-engines. It uses a PydanticSingleSelector to choose the appropriate tool based on the query.

## 2. Query Engine (with HyDE)

This engine wraps the basic VectorStoreIndex query engine with a HyDEQueryTransform (Hypothetical Document Embeddings).

The benefit of HyDE is that it improves the relevance and accuracy of query results by generating hypothetical documents that closely match the user's query. This approach helps bridge the gap between the query language and the document content, allowing for more effective retrieval of relevant information. By creating synthetic documents that are tailored to the query, HyDE enhances the semantic understanding of the search intent and provides more contextually appropriate results.

## 3. Sub Question Query Engine

This engine breaks down complex queries into sub-questions and uses specialized tools to answer each part.

## 4. Chat Engine
This engine provides a chat interface for interacting with the index.

