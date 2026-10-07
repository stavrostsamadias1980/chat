package com.anytime.chatbot.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class UserMessage {
    @JsonProperty("query")
    private String query;

    @JsonProperty("category")
    private String category;

    @JsonProperty("top_k")
    private Integer topK = 5;

    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }

    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }

    public Integer getTopK() { return topK != null ? topK : 5; }
    public void setTopK(Integer topK) { this.topK = topK; }
}
