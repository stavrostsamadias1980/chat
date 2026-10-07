package com.anytime.chatbot.domain.service;

import java.text.Normalizer;
import java.util.*;
import java.util.regex.Pattern;

/**
 * Domain Service responsible solely for Greek text normalization, accent stripping,
 * sigma unification, and tokenization.
 * 
 * Follows Single Responsibility Principle (SRP).
 */
public final class TextNormalizer {

    private static final Pattern DIACRITICS_PATTERN = Pattern.compile("\\p{InCombiningDiacriticalMarks}+");
    private static final Pattern PUNCTUATION_PATTERN = Pattern.compile("[^\\p{L}\\p{Nd}\\s]");
    private static final Pattern WHITESPACE_PATTERN = Pattern.compile("\\s+");

    private static final Set<String> GREEK_STOPWORDS = Set.of(
            "και", "το", "τα", "του", "των", "τη", "την", "της", "τον", "τους", "ο", "η", "οι",
            "σε", "στο", "στη", "στην", "στα", "στους", "στις", "με", "για", "απο", "ειναι", "να",
            "πως", "τι", "ποιο", "ποια", "ποιες", "ποιοι", "ποιος", "εχει", "εχω", "μου", "σου", "μας"
    );

    private TextNormalizer() {}

    /**
     * Normalizes Greek text: lowercases, strips accents/tonous, normalizes sigma.
     */
    public static String normalize(String text) {
        if (text == null || text.isBlank()) {
            return "";
        }

        String lower = text.toLowerCase(Locale.forLanguageTag("el-GR"));

        // Replace Greek accented vowels
        lower = lower.replace('ά', 'α')
                     .replace('έ', 'ε')
                     .replace('ή', 'η')
                     .replace('ί', 'ι')
                     .replace('ϊ', 'ι')
                     .replace('ΐ', 'ι')
                     .replace('ό', 'ο')
                     .replace('ύ', 'υ')
                     .replace('ϋ', 'υ')
                     .replace('ΰ', 'υ')
                     .replace('ώ', 'ω')
                     .replace('ς', 'σ');

        // Unicode NFD normalization to remove any remaining combining accents
        String normalized = Normalizer.normalize(lower, Normalizer.Form.NFD);
        normalized = DIACRITICS_PATTERN.matcher(normalized).replaceAll("");

        // Strip punctuation and normalize whitespace
        normalized = PUNCTUATION_PATTERN.matcher(normalized).replaceAll(" ");
        return WHITESPACE_PATTERN.matcher(normalized).replaceAll(" ").trim();
    }

    /**
     * Tokenizes normalized text into a list of meaningful tokens (excluding short stopwords).
     */
    public static List<String> tokenize(String text) {
        String normalized = normalize(text);
        if (normalized.isEmpty()) {
            return List.of();
        }

        String[] parts = normalized.split("\\s+");
        List<String> tokens = new ArrayList<>(parts.length);
        for (String part : parts) {
            if (part.length() >= 2 && !GREEK_STOPWORDS.contains(part)) {
                tokens.add(part);
            }
        }
        return tokens;
    }
}
