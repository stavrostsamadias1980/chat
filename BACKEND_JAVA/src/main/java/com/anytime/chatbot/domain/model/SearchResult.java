package com.anytime.chatbot.domain.model;

import java.util.List;

/**
 * Domain Aggregate Result containing the retrieved and extracted answers.
 */
public record SearchResult(
        String status,
        String query,
        String categoryFilter,
        List<FaqMatch> faqs,
        List<PassageMatch> passages,
        int totalResults,
        long timestamp
) {
    public record FaqMatch(
            String question,
            String answer,
            String category,
            String sourceUrl,
            double score
    ) {}

    public record PassageMatch(
            String chunkId,
            String docTitle,
            String category,
            String subcategory,
            String docType,
            String sourceType,
            String sourceUrl,
            int chunkIndex,
            double vectorScore,
            double bm25Score,
            double rrfScore,
            String passageText
    ) {}

    public static SearchResult empty(String query, String categoryFilter) {
        return new SearchResult("no_results", query, categoryFilter, List.of(), List.of(), 0, System.currentTimeMillis() / 1000L);
    }
}
