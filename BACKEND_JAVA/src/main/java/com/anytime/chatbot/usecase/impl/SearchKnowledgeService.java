package com.anytime.chatbot.usecase.impl;

import com.anytime.chatbot.domain.model.FaqItem;
import com.anytime.chatbot.domain.model.PassageChunk;
import com.anytime.chatbot.domain.model.SearchQuery;
import com.anytime.chatbot.domain.model.SearchResult;
import com.anytime.chatbot.usecase.port.in.SearchKnowledgeUseCase;
import com.anytime.chatbot.usecase.port.out.KnowledgeRepositoryPort;
import com.anytime.chatbot.usecase.port.out.SearchEnginePort;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Clean Architecture Use Case Implementation for Knowledge Retrieval.
 * 
 * Adheres to SOLID:
 * - SRP: Coordinates retrieval and applies domain business policies.
 * - OCP: Extensible via ports without modifying orchestration logic.
 * - DIP: Depends purely on outbound abstractions (KnowledgeRepositoryPort & SearchEnginePort).
 */
@Service
public class SearchKnowledgeService implements SearchKnowledgeUseCase {

    private static final double FAQ_THRESHOLD = 0.45;
    private static final double PASSAGE_THRESHOLD = 0.42;

    private final KnowledgeRepositoryPort repositoryPort;
    private final SearchEnginePort searchEnginePort;

    public SearchKnowledgeService(KnowledgeRepositoryPort repositoryPort, SearchEnginePort searchEnginePort) {
        this.repositoryPort = repositoryPort;
        this.searchEnginePort = searchEnginePort;
    }

    @Override
    public SearchResult execute(SearchQuery query) {
        if (query == null || query.text().isBlank()) {
            return SearchResult.empty("", "");
        }

        List<FaqItem> allFaqs = repositoryPort.getAllFaqs();
        List<PassageChunk> allPassages = repositoryPort.getAllPassages();

        // Retrieve top candidates
        List<SearchResult.FaqMatch> topFaqs = searchEnginePort.searchFaqs(query, allFaqs, 1);
        List<SearchResult.PassageMatch> topPassages = searchEnginePort.searchPassages(query, allPassages, 1);

        // Filter by strict threshold
        List<SearchResult.FaqMatch> filteredFaqs = topFaqs.stream()
                .filter(f -> f.score() >= FAQ_THRESHOLD)
                .toList();

        List<SearchResult.PassageMatch> filteredPassages = topPassages.stream()
                .filter(p -> p.vectorScore() >= PASSAGE_THRESHOLD || p.bm25Score() >= PASSAGE_THRESHOLD)
                .toList();

        int totalResults = filteredFaqs.size() + filteredPassages.size();
        String status = totalResults > 0 ? "success" : "no_results";

        return new SearchResult(
                status,
                query.text(),
                query.categoryFilter(),
                filteredFaqs,
                filteredPassages,
                totalResults,
                System.currentTimeMillis() / 1000L
        );
    }
}
