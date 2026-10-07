package com.anytime.chatbot.domain.service;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Domain Service responsible for extracting the most relevant, concise sentence snippet
 * from large text blocks with emergency phone number prioritization.
 * 
 * Follows Single Responsibility Principle (SRP).
 */
public final class SnippetExtractor {

    private static final Pattern SENTENCE_SPLIT_PATTERN = Pattern.compile("(?<=[.!?;\\n])\\s+");
    private static final Pattern PHONE_PATTERN = Pattern.compile("\\b(1158|210\\s*94\\d{5}|801\\s*11\\d{5})\\b");
    private static final Set<String> CONTACT_INTENTS = Set.of(
            "τηλεφωνο", "τηλεφωνα", "τηλ", "επικοινωνια", "καλεσω", "καλω", "βοηθεια", "οδικη", "ατυχημα", "αναγγελια"
    );

    private SnippetExtractor() {}

    /**
     * Extracts the single most informative snippet matching the query.
     *
     * @param text      Full text chunk or answer block.
     * @param query     User search query.
     * @param maxChars  Maximum characters limit (e.g. 280).
     * @return Concise, formatted extractive snippet.
     */
    public static String extract(String text, String query, int maxChars) {
        if (text == null || text.isBlank()) {
            return "";
        }
        text = text.trim();
        if (text.length() <= maxChars) {
            return text;
        }

        List<String> queryTokens = TextNormalizer.tokenize(query);
        boolean isContactIntent = queryTokens.stream().anyMatch(CONTACT_INTENTS::contains);

        String[] rawSentences = SENTENCE_SPLIT_PATTERN.split(text);
        List<String> sentences = new ArrayList<>();
        for (String s : rawSentences) {
            String trimmed = s.trim();
            if (trimmed.length() >= 15) {
                sentences.add(trimmed);
            }
        }

        if (sentences.isEmpty()) {
            return text.substring(0, Math.min(text.length(), maxChars)).trim() + "...";
        }

        double bestScore = -1.0;
        String bestSentence = sentences.get(0);

        for (String sentence : sentences) {
            String normSentence = TextNormalizer.normalize(sentence);
            List<String> sentenceTokens = TextNormalizer.tokenize(normSentence);
            Set<String> sentenceTokenSet = new HashSet<>(sentenceTokens);

            int matchCount = 0;
            for (String qToken : queryTokens) {
                if (sentenceTokenSet.contains(qToken)) {
                    matchCount++;
                } else {
                    for (String sToken : sentenceTokens) {
                        if (sToken.startsWith(qToken) || qToken.startsWith(sToken)) {
                            matchCount++;
                            break;
                        }
                    }
                }
            }

            double score = (double) matchCount;

            // Prioritize phone numbers if user asked for contact/road assistance
            if (isContactIntent) {
                Matcher phoneMatcher = PHONE_PATTERN.matcher(sentence);
                if (phoneMatcher.find()) {
                    score += 5.0;
                }
            }

            // Penalize very long single sentences that exceed max limit
            if (sentence.length() > maxChars) {
                score *= 0.8;
            }

            if (score > bestScore) {
                bestScore = score;
                bestSentence = sentence;
            }
        }

        if (bestSentence.length() > maxChars) {
            return bestSentence.substring(0, maxChars - 3).trim() + "...";
        }

        return bestSentence;
    }
}
