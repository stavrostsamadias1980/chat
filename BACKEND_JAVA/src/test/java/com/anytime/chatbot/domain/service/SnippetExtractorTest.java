package com.anytime.chatbot.domain.service;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit Tests for SnippetExtractor domain service.
 */
class SnippetExtractorTest {

    @Test
    @DisplayName("Should extract concise sentence and prioritize emergency phone 1158")
    void testExtractWithPhoneIntent() {
        String fullText = "Η Anytime παρέχει ολοκληρωμένη φροντίδα. " +
                "Σε περίπτωση βλάβης ή ατυχήματος καλέστε άμεσα την Οδική Βοήθεια στο 1158 όλο το 24ωρο. " +
                "Τα προγράμματα έχουν διάρκεια 12 μηνών.";

        String query = "ποιο ειναι το τηλεφωνο για οδικη βοηθεια;";
        String snippet = SnippetExtractor.extract(fullText, query, 280);

        assertNotNull(snippet);
        assertTrue(snippet.contains("1158"));
        assertTrue(snippet.length() <= 280);
    }
}
