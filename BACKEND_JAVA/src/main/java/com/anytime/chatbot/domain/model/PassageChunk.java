package com.anytime.chatbot.domain.model;

/**
 * Domain Entity representing an authentic clause/chunk from Anytime insurance contracts.
 * Adheres to Domain-Driven Design and Clean Architecture principles.
 */
public record PassageChunk(
        String chunkId,
        String docTitle,
        String category,
        String subcategory,
        String docType,
        String sourceType,
        String sourceUrl,
        int chunkIndex,
        String text
) {
    public PassageChunk {
        if (chunkId == null || chunkId.isBlank()) {
            throw new IllegalArgumentException("Chunk ID cannot be null or blank");
        }
        if (text == null || text.isBlank()) {
            throw new IllegalArgumentException("Passage text cannot be null or blank");
        }
    }
}
