package com.anytime.chatbot.controller;

import com.anytime.chatbot.model.ChatResponse;
import com.anytime.chatbot.model.UserMessage;
import com.anytime.chatbot.usecase.port.in.SearchKnowledgeUseCase;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class ChatWebSocketHandler extends TextWebSocketHandler {

    private static final Logger log = LoggerFactory.getLogger(ChatWebSocketHandler.class);
    private final SearchKnowledgeUseCase searchKnowledgeUseCase;
    private final ObjectMapper objectMapper;
    private final ConcurrentHashMap<String, WebSocketSession> activeSessions = new ConcurrentHashMap<>();

    public ChatWebSocketHandler(SearchKnowledgeUseCase searchKnowledgeUseCase) {
        this.searchKnowledgeUseCase = searchKnowledgeUseCase;
        this.objectMapper = new ObjectMapper();
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        activeSessions.put(session.getId(), session);
        log.info("⚡ WebSocket Client Connected: Session ID={}", session.getId());
    }

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws IOException {
        String payload = message.getPayload();
        log.info("📩 Received message from session {}: {}", session.getId(), payload);

        try {
            UserMessage userMsg = objectMapper.readValue(payload, UserMessage.class);

            if (userMsg.getQuery() == null || userMsg.getQuery().trim().isEmpty()) {
                sendError(session, "Το ερώτημα δεν μπορεί να είναι κενό.");
                return;
            }

            // 1. Execute Pure Java Clean Architecture Search Knowledge Use Case
            com.anytime.chatbot.domain.model.SearchQuery query =
                    new com.anytime.chatbot.domain.model.SearchQuery(userMsg.getQuery().trim(), userMsg.getCategory());
            com.anytime.chatbot.domain.model.SearchResult domainResult = searchKnowledgeUseCase.execute(query);

            ChatResponse response = ChatResponse.fromDomain(domainResult);

            // 2. Return the pure extractive results & passages to the widget
            String responseJson = objectMapper.writeValueAsString(response);
            session.sendMessage(new TextMessage(responseJson));
            log.info("📤 Dispatched response to session {}: {} total items", session.getId(), response.getTotalResults());

        } catch (Exception e) {
            log.error("Error processing WebSocket message: {}", e.getMessage(), e);
            sendError(session, "Σφάλμα επεξεργασίας: " + e.getMessage());
        }
    }

    private void sendError(WebSocketSession session, String errorMsg) {
        try {
            ChatResponse err = ChatResponse.error("", errorMsg);
            session.sendMessage(new TextMessage(objectMapper.writeValueAsString(err)));
        } catch (IOException ex) {
            log.error("Failed to send error message: {}", ex.getMessage());
        }
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
        activeSessions.remove(session.getId());
        log.info("🔌 WebSocket Client Disconnected: Session ID={}, Status={}", session.getId(), status);
    }
}
