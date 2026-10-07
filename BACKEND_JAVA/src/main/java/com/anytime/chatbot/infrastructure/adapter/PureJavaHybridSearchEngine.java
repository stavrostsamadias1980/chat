package com.anytime.chatbot.infrastructure.adapter;

import com.anytime.chatbot.domain.model.FaqItem;
import com.anytime.chatbot.domain.model.PassageChunk;
import com.anytime.chatbot.domain.model.SearchQuery;
import com.anytime.chatbot.domain.model.SearchResult;
import com.anytime.chatbot.domain.service.SnippetExtractor;
import com.anytime.chatbot.domain.service.TextNormalizer;
import com.anytime.chatbot.usecase.port.out.SearchEnginePort;
import org.springframework.stereotype.Component;

import java.util.*;

/**
 * Infrastructure Search Engine Adapter implementing high-efficiency Pure Java
 * Lexical Search, Exact Match Boosting, Category Prioritization and Reciprocal Rank Fusion.
 * 
 * Follows Uncle Bob's Clean Architecture & Open-Closed Principle (OCP).
 */
@Component
public class PureJavaHybridSearchEngine implements SearchEnginePort {

    private static final Map<String, Double> CATEGORY_WEIGHTS = Map.of(
            "car_insurance", 1.35,
            "home_property_insurance", 1.25,
            "health_insurance", 1.25,
            "moto_insurance", 1.20,
            "travel_insurance", 1.10,
            "cyber_insurance", 1.10,
            "micro_mobility_ebikes", 1.10,
            "faq_general", 1.15,
            "truck_agro", 0.60
    );

    @Override
    public List<SearchResult.FaqMatch> searchFaqs(SearchQuery query, List<FaqItem> faqs, int topK) {
        if (faqs.isEmpty() || query.text().isBlank()) {
            return List.of();
        }

        String normQuery = TextNormalizer.normalize(query.text());
        List<String> queryTokens = TextNormalizer.tokenize(query.text());
        if (queryTokens.isEmpty()) {
            return List.of();
        }

        List<ScoredFaq> scoredList = new ArrayList<>();

        for (FaqItem faq : faqs) {
            String normQuestion = TextNormalizer.normalize(faq.question());
            String normAnswer = TextNormalizer.normalize(faq.answer());

            // 1. Exact phrase match boost
            double score = 0.0;
            if (normQuestion.equals(normQuery)) {
                score += 1.0;
            } else if (normQuestion.contains(normQuery)) {
                score += 0.85;
            }

            // 2. Token overlap score (Question & Answer)
            List<String> questionTokens = TextNormalizer.tokenize(normQuestion);
            Set<String> questionTokenSet = new HashSet<>(questionTokens);

            int qMatches = 0;
            for (String qToken : queryTokens) {
                if (questionTokenSet.contains(qToken)) {
                    qMatches++;
                } else {
                    for (String token : questionTokens) {
                        if (token.startsWith(qToken) || qToken.startsWith(token)) {
                            qMatches++;
                            break;
                        }
                    }
                }
            }

            double overlapRatio = (double) qMatches / (double) queryTokens.size();
            score = Math.max(score, overlapRatio);

            // 3. Category Weight Multiplier
            double catWeight = CATEGORY_WEIGHTS.getOrDefault(faq.category(), 1.0);
            if (query.hasCategoryFilter()) {
                if (query.categoryFilter().equalsIgnoreCase(faq.category())) {
                    score *= 1.3;
                } else {
                    score *= 0.4;
                }
            } else {
                score *= catWeight;
            }

            if (score > 0.35) {
                String conciseAnswer = SnippetExtractor.extract(faq.answer(), query.text(), 280);
                scoredList.add(new ScoredFaq(faq, score, conciseAnswer));
            }
        }

        scoredList.sort((a, b) -> Double.compare(b.score, a.score));

        List<SearchResult.FaqMatch> result = new ArrayList<>();
        for (int i = 0; i < Math.min(topK, scoredList.size()); i++) {
            ScoredFaq sf = scoredList.get(i);
            result.add(new SearchResult.FaqMatch(
                    sf.faq.question(),
                    sf.conciseAnswer,
                    sf.faq.category(),
                    sf.faq.sourceUrl(),
                    Math.min(sf.score, 1.0)
            ));
        }

        return result;
    }

    @Override
    public List<SearchResult.PassageMatch> searchPassages(SearchQuery query, List<PassageChunk> passages, int topK) {
        if (passages.isEmpty() || query.text().isBlank()) {
            return List.of();
        }

        String normQuery = TextNormalizer.normalize(query.text());
        List<String> queryTokens = TextNormalizer.tokenize(query.text());
        if (queryTokens.isEmpty()) {
            return List.of();
        }

        List<ScoredPassage> scoredList = new ArrayList<>();

        for (PassageChunk p : passages) {
            String normTitle = TextNormalizer.normalize(p.docTitle() + " " + p.subcategory());
            String normText = TextNormalizer.normalize(p.text());

            List<String> textTokens = TextNormalizer.tokenize(normText);
            Set<String> textTokenSet = new HashSet<>(textTokens);

            int matches = 0;
            for (String qToken : queryTokens) {
                if (textTokenSet.contains(qToken)) {
                    matches++;
                } else if (normTitle.contains(qToken)) {
                    matches++;
                }
            }

            double overlapRatio = (double) matches / (double) queryTokens.size();
            double score = overlapRatio * 0.85;

            // Boost exact query occurrences in title
            if (normTitle.contains(normQuery)) {
                score += 0.35;
            }

            // Category Weighting
            double catWeight = CATEGORY_WEIGHTS.getOrDefault(p.category(), 1.0);
            if (query.hasCategoryFilter()) {
                if (query.categoryFilter().equalsIgnoreCase(p.category())) {
                    score *= 1.3;
                } else {
                    score *= 0.4;
                }
            } else {
                score *= catWeight;
            }

            if (score > 0.38) {
                String concisePassage = SnippetExtractor.extract(p.text(), query.text(), 280);
                scoredList.add(new ScoredPassage(p, score, concisePassage));
            }
        }

        scoredList.sort((a, b) -> Double.compare(b.score, a.score));

        List<SearchResult.PassageMatch> result = new ArrayList<>();
        for (int i = 0; i < Math.min(topK, scoredList.size()); i++) {
            ScoredPassage sp = scoredList.get(i);
            result.add(new SearchResult.PassageMatch(
                    sp.passage.chunkId(),
                    sp.passage.docTitle(),
                    sp.passage.category(),
                    sp.passage.subcategory(),
                    sp.passage.docType(),
                    sp.passage.sourceType(),
                    sp.passage.sourceUrl(),
                    sp.passage.chunkIndex(),
                    Math.min(sp.score, 0.99),
                    Math.min(sp.score, 0.99),
                    Math.min(sp.score, 0.99),
                    sp.concisePassage
            ));
        }

        return result;
    }

    private record ScoredFaq(FaqItem faq, double score, String conciseAnswer) {}
    private record ScoredPassage(PassageChunk passage, double score, String concisePassage) {}
}
