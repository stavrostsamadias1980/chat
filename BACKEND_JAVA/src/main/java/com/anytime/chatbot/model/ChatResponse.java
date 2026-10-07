package com.anytime.chatbot.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class ChatResponse {
    @JsonProperty("status")
    private String status;

    @JsonProperty("query")
    private String query;

    @JsonProperty("category_filter")
    private String categoryFilter;

    @JsonProperty("faqs")
    private List<FaqDto> faqs;

    @JsonProperty("passages")
    private List<PassageDto> passages;

    @JsonProperty("total_results")
    private int totalResults;

    @JsonProperty("timestamp")
    private long timestamp = System.currentTimeMillis();

    public static ChatResponse fromDomain(com.anytime.chatbot.domain.model.SearchResult domainResult) {
        ChatResponse resp = new ChatResponse();
        resp.setStatus(domainResult.status());
        resp.setQuery(domainResult.query());
        resp.setCategoryFilter(domainResult.categoryFilter());

        if (domainResult.faqs() != null) {
            resp.setFaqs(domainResult.faqs().stream().map(f -> {
                FaqDto dto = new FaqDto();
                dto.setQuestion(f.question());
                dto.setAnswer(f.answer());
                dto.setSourceUrl(f.sourceUrl());
                return dto;
            }).toList());
        } else {
            resp.setFaqs(List.of());
        }

        if (domainResult.passages() != null) {
            resp.setPassages(domainResult.passages().stream().map(p -> {
                PassageDto dto = new PassageDto();
                dto.setChunkId(p.chunkId());
                dto.setDocTitle(p.docTitle());
                dto.setCategory(p.category());
                dto.setSubcategory(p.subcategory());
                dto.setDocType(p.docType());
                dto.setSourceType(p.sourceType());
                dto.setSourceUrl(p.sourceUrl());
                dto.setChunkIndex(p.chunkIndex());
                dto.setVectorScore(p.vectorScore());
                dto.setBm25Score(p.bm25Score());
                dto.setRrfScore(p.rrfScore());
                dto.setPassageText(p.passageText());
                return dto;
            }).toList());
        } else {
            resp.setPassages(List.of());
        }

        resp.setTotalResults(domainResult.totalResults());
        resp.setTimestamp(domainResult.timestamp());
        return resp;
    }

    public static ChatResponse of(String query, String category, List<FaqDto> faqs, List<PassageDto> passages) {
        ChatResponse resp = new ChatResponse();
        resp.setStatus("success");
        resp.setQuery(query);
        resp.setCategoryFilter(category);
        resp.setFaqs(faqs);
        resp.setPassages(passages);
        resp.setTotalResults((faqs != null ? faqs.size() : 0) + (passages != null ? passages.size() : 0));
        return resp;
    }

    public static ChatResponse error(String query, String message) {
        ChatResponse resp = new ChatResponse();
        resp.setStatus("error");
        resp.setQuery(query);
        return resp;
    }

    // Getters and Setters
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }

    public String getCategoryFilter() { return categoryFilter; }
    public void setCategoryFilter(String categoryFilter) { this.categoryFilter = categoryFilter; }

    public List<FaqDto> getFaqs() { return faqs; }
    public void setFaqs(List<FaqDto> faqs) { this.faqs = faqs; }

    public List<PassageDto> getPassages() { return passages; }
    public void setPassages(List<PassageDto> passages) { this.passages = passages; }

    public int getTotalResults() { return totalResults; }
    public void setTotalResults(int totalResults) { this.totalResults = totalResults; }

    public long getTimestamp() { return timestamp; }
    public void setTimestamp(long timestamp) { this.timestamp = timestamp; }
}
