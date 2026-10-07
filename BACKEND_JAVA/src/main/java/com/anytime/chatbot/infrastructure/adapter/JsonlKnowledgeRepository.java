package com.anytime.chatbot.infrastructure.adapter;

import com.anytime.chatbot.domain.model.FaqItem;
import com.anytime.chatbot.domain.model.PassageChunk;
import com.anytime.chatbot.usecase.port.out.KnowledgeRepositoryPort;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Repository;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Infrastructure Adapter loading JSONL knowledge datasets.
 * Implements KnowledgeRepositoryPort (Clean Architecture Dependency Inversion).
 */
@Repository
public class JsonlKnowledgeRepository implements KnowledgeRepositoryPort {

    private static final Logger log = LoggerFactory.getLogger(JsonlKnowledgeRepository.class);

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final List<FaqItem> cachedFaqs = new ArrayList<>();
    private final List<PassageChunk> cachedPassages = new ArrayList<>();

    @Value("${anytime.dataset.path:../anytime_rag_dataset/rag_ready_chunks}")
    private String datasetBasePath;

    @PostConstruct
    public void init() {
        loadFaqs();
        loadPassages();
    }

    private void loadFaqs() {
        File faqFile = resolveFile("faq_qa_pairs.jsonl");
        if (!faqFile.exists()) {
            log.warn("FAQ dataset file not found at: {}", faqFile.getAbsolutePath());
            return;
        }

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(new FileInputStream(faqFile), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.isBlank()) continue;
                JsonNode node = objectMapper.readTree(line);
                String question = node.path("question").asText("");
                String answer = node.path("answer").asText("");
                String category = node.path("category").asText("all");
                String sourceUrl = node.path("source_url").asText("https://www.anytime.gr/info/faq");
                String source = node.path("source").asText("faq");

                if (!question.isBlank() && !answer.isBlank()) {
                    cachedFaqs.add(new FaqItem(question, answer, category, sourceUrl, source));
                }
            }
            log.info("Successfully loaded {} verified FAQ items into Pure Java Memory Cache.", cachedFaqs.size());
        } catch (Exception e) {
            log.error("Failed to load FAQ dataset", e);
        }
    }

    private void loadPassages() {
        File passageFile = resolveFile("chunks.jsonl");
        if (!passageFile.exists()) {
            passageFile = resolveFile("terms_conditions_chunks.jsonl");
        }
        if (!passageFile.exists()) {
            log.warn("Passages dataset file not found at: {}", passageFile.getAbsolutePath());
            return;
        }

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(new FileInputStream(passageFile), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.isBlank()) continue;
                JsonNode node = objectMapper.readTree(line);
                String chunkId = node.path("chunk_id").asText("chunk_" + cachedPassages.size());
                String docTitle = node.path("doc_title").asText("Όροι Συμβολαίου Anytime");
                String category = node.path("category").asText("all");
                String subcategory = node.path("subcategory").asText("general");
                String docType = node.path("doc_type").asText("terms");
                String sourceType = node.path("source_type").asText("pdf");
                String sourceUrl = node.path("source_url").asText("https://www.anytime.gr");
                int chunkIndex = node.path("chunk_index").asInt(0);
                String text = node.path("text").asText(node.path("chunk_text").asText(""));

                if (!chunkId.isBlank() && !text.isBlank()) {
                    cachedPassages.add(new PassageChunk(
                            chunkId, docTitle, category, subcategory, docType, sourceType, sourceUrl, chunkIndex, text
                    ));
                }
            }
            log.info("Successfully loaded {} contract passage chunks into Pure Java Memory Cache.", cachedPassages.size());
        } catch (Exception e) {
            log.error("Failed to load Passages dataset", e);
        }
    }

    private File resolveFile(String filename) {
        Path path = Paths.get(datasetBasePath, filename);
        File file = path.toFile();
        if (!file.exists()) {
            // Try fallback paths
            File alt = new File("anytime_rag_dataset/rag_ready_chunks", filename);
            if (alt.exists()) return alt;
            File alt2 = new File("../anytime_rag_dataset/rag_ready_chunks", filename);
            if (alt2.exists()) return alt2;
            File alt3 = new File("g:/WIDGET-UI/anytime_rag_dataset/rag_ready_chunks", filename);
            if (alt3.exists()) return alt3;
        }
        return file;
    }

    @Override
    public List<FaqItem> getAllFaqs() {
        return Collections.unmodifiableList(cachedFaqs);
    }

    @Override
    public List<PassageChunk> getAllPassages() {
        return Collections.unmodifiableList(cachedPassages);
    }
}
