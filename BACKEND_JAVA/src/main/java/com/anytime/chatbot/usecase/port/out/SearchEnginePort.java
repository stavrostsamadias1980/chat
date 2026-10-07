package com.anytime.chatbot.usecase.port.out;

import com.anytime.chatbot.domain.model.FaqItem;
import com.anytime.chatbot.domain.model.PassageChunk;
import com.anytime.chatbot.domain.model.SearchQuery;
import com.anytime.chatbot.domain.model.SearchResult;

import java.util.List;

/**
 * Outbound Port for indexing and scoring knowledge items.
 * Adheres to Dependency Inversion Principle (DIP).
 */
public interface SearchEnginePort {

    /**
     * Searches and ranks FAQ items.
     */
    List<SearchResult.FaqMatch> searchFaqs(SearchQuery query, List<FaqItem> faqs, int topK);

    /**
     * Searches and ranks contract passage chunks.
     */
    List<SearchResult.PassageMatch> searchPassages(SearchQuery query, List<PassageChunk> passages, int topK);
}
