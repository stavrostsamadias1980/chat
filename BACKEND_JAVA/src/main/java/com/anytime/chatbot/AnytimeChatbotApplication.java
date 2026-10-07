package com.anytime.chatbot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class AnytimeChatbotApplication {

    public static void main(String[] args) {
        SpringApplication.run(AnytimeChatbotApplication.class, args);
        System.out.println("==================================================================");
        System.out.println("☕ Anytime.gr Spring Boot 3 WebSocket Backend & MCP Client Ready!");
        System.out.println("🌐 Server running on: http://localhost:8080");
        System.out.println("⚡ WebSocket Endpoint: ws://localhost:8080/ws/chat");
        System.out.println("==================================================================");
    }
}
