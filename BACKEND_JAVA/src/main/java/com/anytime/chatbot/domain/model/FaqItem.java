package com.anytime.chatbot.domain.model;

/**
 * Domain Entity representing an official Verified FAQ Question & Answer pair.
 * Follows Uncle Bob's Clean Architecture (Zero framework dependencies).
 */
public record FaqItem(
        String question,
        String answer,
        String category,
        String sourceUrl,
        String source
) {
    public FaqItem {
        if (question == null || question.isBlank()) {
            throw new IllegalArgumentException("FAQ question cannot be null or blank");
        }
        if (answer == null || answer.isBlank()) {
            throw new IllegalArgumentException("FAQ answer cannot be null or blank");
        }
    }
}
