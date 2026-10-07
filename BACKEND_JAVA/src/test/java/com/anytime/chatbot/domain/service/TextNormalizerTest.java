package com.anytime.chatbot.domain.service;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit Tests for TextNormalizer domain service.
 * Validates Greek accent stripping, lowercasing, sigma normalization and tokenization.
 */
class TextNormalizerTest {

    @Test
    @DisplayName("Should normalize Greek text by stripping accents and lowercasing")
    void testNormalizeGreekAccents() {
        String input = "Οδική Βοήθεια & Ατυχήματα";
        String normalized = TextNormalizer.normalize(input);
        assertEquals("οδικη βοηθεια ατυχηματα", normalized);
    }

    @Test
    @DisplayName("Should normalize final sigma 'ς' to 'σ'")
    void testNormalizeSigma() {
        String input = "Όρος Συμβολαίου και καλύψεις";
        String normalized = TextNormalizer.normalize(input);
        assertEquals("οροσ συμβολαιου και καλυψεισ", normalized);
    }

    @Test
    @DisplayName("Should tokenize and strip Greek stopwords")
    void testTokenizeAndRemoveStopwords() {
        String input = "Ποιες είναι οι καλύψεις για το αυτοκίνητο και το σπίτι;";
        List<String> tokens = TextNormalizer.tokenize(input);
        
        assertFalse(tokens.contains("και"));
        assertFalse(tokens.contains("το"));
        assertFalse(tokens.contains("για"));
        assertTrue(tokens.contains("καλυψεισ"));
        assertTrue(tokens.contains("αυτοκινητο"));
        assertTrue(tokens.contains("σπιτι"));
    }
}
