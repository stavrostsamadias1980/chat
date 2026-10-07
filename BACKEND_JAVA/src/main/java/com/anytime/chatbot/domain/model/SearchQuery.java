package com.anytime.chatbot.domain.model;

/**
 * Value Object encapsulating a user's search query and optional category filter.
 */
public record SearchQuery(
        String text,
        String categoryFilter
) {
    public SearchQuery {
        if (text == null) {
            text = "";
        }
        text = text.trim();
    }

    public boolean hasCategoryFilter() {
        return categoryFilter != null && !categoryFilter.isBlank() && !"all".equalsIgnoreCase(categoryFilter);
    }
}
