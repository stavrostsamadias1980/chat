package com.anytime.chatbot.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class PassageDto {
    @JsonProperty("chunk_id")
    private String chunkId;

    @JsonProperty("doc_title")
    private String docTitle;

    @JsonProperty("category")
    private String category;

    @JsonProperty("subcategory")
    private String subcategory;

    @JsonProperty("doc_type")
    private String docType;

    @JsonProperty("source_type")
    private String sourceType;

    @JsonProperty("source_url")
    private String sourceUrl;

    @JsonProperty("chunk_index")
    private int chunkIndex;

    @JsonProperty("vector_score")
    private double vectorScore;

    @JsonProperty("bm25_score")
    private double bm25Score;

    @JsonProperty("rrf_score")
    private double rrfScore;

    @JsonProperty("passage_text")
    private String passageText;

    // Getters and Setters
    public String getChunkId() { return chunkId; }
    public void setChunkId(String chunkId) { this.chunkId = chunkId; }

    public String getDocTitle() { return docTitle; }
    public void setDocTitle(String docTitle) { this.docTitle = docTitle; }

    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }

    public String getSubcategory() { return subcategory; }
    public void setSubcategory(String subcategory) { this.subcategory = subcategory; }

    public String getDocType() { return docType; }
    public void setDocType(String docType) { this.docType = docType; }

    public String getSourceType() { return sourceType; }
    public void setSourceType(String sourceType) { this.sourceType = sourceType; }

    public String getSourceUrl() { return sourceUrl; }
    public void setSourceUrl(String sourceUrl) { this.sourceUrl = sourceUrl; }

    public int getChunkIndex() { return chunkIndex; }
    public void setChunkIndex(int chunkIndex) { this.chunkIndex = chunkIndex; }

    public double getVectorScore() { return vectorScore; }
    public void setVectorScore(double vectorScore) { this.vectorScore = vectorScore; }

    public double getBm25Score() { return bm25Score; }
    public void setBm25Score(double bm25Score) { this.bm25Score = bm25Score; }

    public double getRrfScore() { return rrfScore; }
    public void setRrfScore(double rrfScore) { this.rrfScore = rrfScore; }

    public String getPassageText() { return passageText; }
    public void setPassageText(String passageText) { this.passageText = passageText; }
}
