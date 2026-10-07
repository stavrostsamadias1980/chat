package com.anytime.chatbot.usecase.port.in;

import com.anytime.chatbot.domain.model.SearchQuery;
import com.anytime.chatbot.domain.model.SearchResult;

/**
 * Inbound Port (Use Case Interface) for Knowledge Retrieval.
 * Follows Uncle Bob's Clean Architecture & Interface Segregation Principle (ISP).
 */
public interface SearchKnowledgeUseCase {

    /**
     * Executes purely extractive knowledge retrieval for the given search query.
     *
     * @param query Search query and category filter.
     * @return Extracted and ranked SearchResult containing top FAQ and top Passage.
     */
    SearchResult execute(SearchQuery query);
}
