package com.anytime.chatbot.usecase.port.out;

import com.anytime.chatbot.domain.model.FaqItem;
import com.anytime.chatbot.domain.model.PassageChunk;

import java.util.List;

/**
 * Outbound Port (Repository Interface) for data loading.
 * Follows Dependency Inversion Principle (DIP).
 */
public interface KnowledgeRepositoryPort {

    /**
     * Retrieves all verified FAQ items.
     */
    List<FaqItem> getAllFaqs();

    /**
     * Retrieves all contract passage chunks.
     */
    List<PassageChunk> getAllPassages();
}
