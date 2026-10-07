package com.anytime.chatbot.usecase.impl;

import com.anytime.chatbot.domain.model.FaqItem;
import com.anytime.chatbot.domain.model.PassageChunk;
import com.anytime.chatbot.domain.model.SearchQuery;
import com.anytime.chatbot.domain.model.SearchResult;
import com.anytime.chatbot.usecase.port.out.KnowledgeRepositoryPort;
import com.anytime.chatbot.usecase.port.out.SearchEnginePort;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.Mockito.when;

/**
 * Unit Tests for SearchKnowledgeService Clean Architecture Use Case.
 */
class SearchKnowledgeServiceTest {

    private KnowledgeRepositoryPort repositoryPort;
    private SearchEnginePort searchEnginePort;
    private SearchKnowledgeService service;

    @BeforeEach
    void setUp() {
        repositoryPort = Mockito.mock(KnowledgeRepositoryPort.class);
        searchEnginePort = Mockito.mock(SearchEnginePort.class);
        service = new SearchKnowledgeService(repositoryPort, searchEnginePort);
    }

    @Test
    @DisplayName("Should execute search and filter by threshold")
    void testExecuteSuccessfulSearch() {
        FaqItem faq = new FaqItem("Πώς καλώ οδική;", "Καλέστε στο 1158.", "car_insurance", "http://anytime.gr", "faq");
        when(repositoryPort.getAllFaqs()).thenReturn(List.of(faq));
        when(repositoryPort.getAllPassages()).thenReturn(List.of());

        SearchResult.FaqMatch match = new SearchResult.FaqMatch("Πώς καλώ οδική;", "Καλέστε στο 1158.", "car_insurance", "http://anytime.gr", 0.95);
        when(searchEnginePort.searchFaqs(any(), any(), anyInt())).thenReturn(List.of(match));
        when(searchEnginePort.searchPassages(any(), any(), anyInt())).thenReturn(List.of());

        SearchQuery query = new SearchQuery("οδική βοήθεια", "car_insurance");
        SearchResult result = service.execute(query);

        assertEquals("success", result.status());
        assertEquals(1, result.totalResults());
        assertEquals(1, result.faqs().size());
        assertEquals("Πώς καλώ οδική;", result.faqs().get(0).question());
    }

    @Test
    @DisplayName("Should return no_results when below threshold")
    void testExecuteBelowThreshold() {
        when(repositoryPort.getAllFaqs()).thenReturn(List.of());
        when(repositoryPort.getAllPassages()).thenReturn(List.of());

        SearchResult.FaqMatch lowMatch = new SearchResult.FaqMatch("Άσχετη ερώτηση", "Απάντηση", "all", "http://anytime.gr", 0.20);
        when(searchEnginePort.searchFaqs(any(), any(), anyInt())).thenReturn(List.of(lowMatch));
        when(searchEnginePort.searchPassages(any(), any(), anyInt())).thenReturn(List.of());

        SearchQuery query = new SearchQuery("άσχετο κείμενο", "all");
        SearchResult result = service.execute(query);

        assertEquals("no_results", result.status());
        assertEquals(0, result.totalResults());
    }
}
